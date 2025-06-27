import os
import logging
import pandas as pd
from dotenv import load_dotenv
import asyncio
from pathlib import Path
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Adjust path to import from src
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.loader import FmpDataLoader
from src.data.processor import DataProcessor
from src.optimization.cvar_optimizer import CVaROptimizer, RollingCVaROptimizer
from src.backtesting.metrics import calculate_raw_metrics, format_metrics_for_display


async def main():
    """Main function to run the full backtest."""
    logging.info("--- Starting Full Backtest Script ---")
    # --- Parameters ---
    FMP_API_KEY = os.getenv("FMP_API_KEY")
    if not FMP_API_KEY:
        logging.error("FMP_API_KEY not found. Please set it in your .env file.")
        return

    # Per assignment, use top 60 companies. We will use a fixed list of well-known S&P 100 companies.
    UNIVERSE_TICKERS = [
        'AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'GOOG', 'META', 'TSLA',
        'BRK-B', 'JPM', 'JNJ', 'V', 'UNH', 'PG', 'MA', 'HD',
        'BAC', 'CVX', 'LLY', 'XOM', 'AVGO', 'COST', 'ABBV', 'PFE',
        'MRK', 'PEP', 'KO', 'ADBE', 'CSCO', 'WMT', 'MCD', 'ACN',
        'CRM', 'TMO', 'DIS', 'LIN', 'NFLX', 'ABT', 'DHR', 'WFC',
        'CMCSA', 'VZ', 'NEE', 'NKE', 'PM', 'TXN', 'HON', 'UPS',
        'LOW', 'RTX', 'MS', 'INTC', 'GS', 'AMD', 'IBM', 'SBUX',
        'CAT', 'DE', 'UNP', 'BA'
    ]
    logging.info(f"Using a fixed list of {len(UNIVERSE_TICKERS)} tickers for the backtest.")

    START_DATE = "2010-01-01"
    END_DATE = "2024-12-31"
    BENCHMARK_TICKER = "SPY"

    # --- Data Loading and Processing ---
    loader = FmpDataLoader(api_key=FMP_API_KEY)
    processor = DataProcessor()

    all_tickers = UNIVERSE_TICKERS + [BENCHMARK_TICKER]
    logging.info(f"Fetching price data for {len(all_tickers)} tickers from {START_DATE} to {END_DATE}...")
    price_data = await loader.get_multiple_tickers_data(all_tickers, start_date=START_DATE, end_date=END_DATE)

    # --- Save Price Data --- 
    # This is needed by other scripts like the alpha backtest
    results_path = Path("results")
    results_path.mkdir(exist_ok=True)
    price_data_path = results_path / "sp500_prices_2010_2024.csv"
    try:
        logging.info(f"Saving raw price data to {price_data_path}...")
        price_data.to_csv(price_data_path)
        logging.info("Successfully saved raw price data.")
    except Exception as e:
        logging.error(f"Failed to save price data: {e}")


    returns_data = processor.calculate_returns(price_data)
    cleaned_returns = processor.clean_data(returns_data)

    # The actual universe is the set of tickers for which we successfully loaded data
    UNIVERSE_TICKERS = [ticker for ticker in cleaned_returns.columns if ticker != BENCHMARK_TICKER]
    logging.info(f"Successfully loaded data for {len(UNIVERSE_TICKERS)} tickers. Using this list as the final universe.")

    asset_returns = cleaned_returns[UNIVERSE_TICKERS]
    benchmark_returns = cleaned_returns[BENCHMARK_TICKER]

    logging.info("Data loaded and processed successfully.")

    # --- Run Rolling Backtest ---
    CVAR_ALPHA = 0.95
    TRANSACTION_COST = 0.001
    MAX_WEIGHT = 0.05
    cvar_optimizer = CVaROptimizer(
        alpha=CVAR_ALPHA,
        lasso_penalty=1.5,  # As per CLEIR paper - promotes sparsity
        transaction_cost=TRANSACTION_COST,
        max_weight=MAX_WEIGHT,
        solver='SCS'  # Explicitly set the solver to avoid ECOS error
    )
    rolling_optimizer = RollingCVaROptimizer(
        optimizer=cvar_optimizer,
        lookback_window=252,  # 1 year
        rebalance_frequency='Q'  # Quarterly
    )

    logging.info("Starting rolling backtest for the 2020-2024 period...")
    BACKTEST_START_DATE = "2020-01-01"
    BACKTEST_END_DATE = "2024-12-31"
    lookback = 252 # 1 year
    rebalance_dates = pd.date_range(start=BACKTEST_START_DATE, end=BACKTEST_END_DATE, freq='BQ').to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns.index)]

    all_weights = {}
    rebalance_results_list = []
    current_weights = pd.Series(1/len(UNIVERSE_TICKERS), index=UNIVERSE_TICKERS)

    for date in rebalance_dates:
        start_window = date - pd.DateOffset(days=lookback)
        hist_returns = asset_returns.loc[start_window:date]
        hist_benchmark = benchmark_returns.loc[start_window:date]

        try:
            opt_result = cvar_optimizer.optimize(hist_returns, hist_benchmark, current_weights.values)
            if opt_result and opt_result.status in ['optimal', 'optimal_inaccurate']:
                current_weights = pd.Series(opt_result.weights, index=hist_returns.columns)
                logging.info(f"Rebalanced on {date}: CVaR={opt_result.cvar:.4f}, Status={opt_result.status}")
                rebalance_results_list.append({'date': date, 'cvar': opt_result.cvar, 'status': opt_result.status, 'weights': opt_result.weights})
            else:
                status = opt_result.status if opt_result else 'unknown failure'
                logging.warning(f"Optimization non-optimal on {date} with status {status}. Holding weights.")
                rebalance_results_list.append({'date': date, 'cvar': np.nan, 'status': status, 'weights': current_weights.values})
        except Exception as e:
            logging.error(f"Optimization failed on {date}: {e}. Holding weights.")
            rebalance_results_list.append({'date': date, 'cvar': np.nan, 'status': 'failure', 'weights': current_weights.values})
        
        all_weights[date] = current_weights

    rebalance_results = pd.DataFrame(rebalance_results_list).set_index('date')
    weights_df = pd.DataFrame(all_weights).T.reindex(asset_returns.index, method='ffill').dropna()
    portfolio_returns = (weights_df * asset_returns).sum(axis=1).loc[BACKTEST_START_DATE:BACKTEST_END_DATE]

    logging.info("Backtest completed.")

    if portfolio_returns.empty:
        logging.error("Backtest returned no portfolio returns. Exiting.")
        return

    # --- Performance Analysis ---
    raw_metrics = calculate_raw_metrics(portfolio_returns, benchmark_returns)
    display_metrics = format_metrics_for_display(raw_metrics, portfolio_returns)

    # --- Save Results ---
    try:
        results_path = Path("results")
        results_path.mkdir(exist_ok=True)

        # Save weights
        weights_path = results_path / "baseline_cvar_rebalance_weights_2020-2024.csv"
        logging.info(f"Attempting to save weights to {weights_path}...")
        rebalance_results_to_save = rebalance_results.copy()
        if 'weights' in rebalance_results_to_save.columns:
            rebalance_results_to_save['weights'] = rebalance_results_to_save['weights'].apply(
                lambda w: np.array2string(w, separator=',') if isinstance(w, np.ndarray) else w
            )
        rebalance_results_to_save.to_csv(weights_path)
        logging.info("Successfully saved weights.")

        # Save metrics
        metrics_path = results_path / "baseline_cvar_performance_metrics.csv"
        logging.info(f"Attempting to save metrics to {metrics_path}...")
        raw_metrics.to_csv(metrics_path, header=True)
        logging.info("Successfully saved metrics.")

        # Save daily returns
        returns_path = results_path / "baseline_daily_returns.csv"
        logging.info(f"Attempting to save daily returns to {returns_path}...")
        aligned_benchmark = benchmark_returns.reindex(portfolio_returns.index).ffill()
        all_returns = pd.DataFrame({
            'Baseline_CVaR': portfolio_returns,
            'SPY': aligned_benchmark
        }).dropna()
        all_returns.to_csv(returns_path)
        logging.info("Successfully saved daily returns.")
        
        logging.info(f"Results saved to {results_path.resolve()}")

    except Exception as e:
        logging.error(f"CRITICAL: Failed to save results to disk: {e}")

    logging.info("--- Full Backtest Script Finished ---")
    print("\n--- Baseline Performance Metrics ---")
    print(display_metrics)


if __name__ == "__main__":
    asyncio.run(main())
