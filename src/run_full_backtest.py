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
from src.backtesting.metrics import calculate_performance_metrics


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

    returns_data = processor.calculate_returns(price_data)
    cleaned_returns = processor.clean_data(returns_data)

    # The actual universe is the set of tickers for which we successfully loaded data
    UNIVERSE_TICKERS = [ticker for ticker in cleaned_returns.columns if ticker != BENCHMARK_TICKER]
    logging.info(f"Successfully loaded data for {len(UNIVERSE_TICKERS)} tickers. Using this list as the final universe.")

    asset_returns = cleaned_returns[UNIVERSE_TICKERS]
    benchmark_returns = cleaned_returns[BENCHMARK_TICKER]

    logging.info("Data loaded and processed successfully.")

    # --- Run Rolling Backtest ---
    cvar_optimizer = CVaROptimizer(
        alpha=0.95, 
        lasso_penalty=0.01,
        transaction_cost=0.001 # 10 bps transaction cost
    )
    rolling_optimizer = RollingCVaROptimizer(
        optimizer=cvar_optimizer,
        lookback_window=252,  # 1 year
        rebalance_frequency='Q'  # Quarterly
    )

    logging.info("Starting rolling backtest...")
    rebalance_results, portfolio_returns = rolling_optimizer.backtest(asset_returns, benchmark_returns)

    logging.info("Backtest completed.")

    if portfolio_returns.empty:
        logging.error("Backtest returned no portfolio returns. Exiting.")
        return

    # --- Calculate and Save Performance Metrics ---
    # Align benchmark returns to portfolio returns index
    aligned_benchmark = benchmark_returns.loc[portfolio_returns.index]
    performance_metrics = calculate_performance_metrics(portfolio_returns, aligned_benchmark)

    # --- Save Results ---
    results_path = Path("results")
    results_path.mkdir(exist_ok=True)

    weights_path = results_path / "cvar_rebalance_weights.csv"
    metrics_path = results_path / "cvar_performance_metrics.csv"

    try:
        logging.info(f"Attempting to save weights to {weights_path}...")
        # Convert weights array to a string representation for CSV compatibility
        rebalance_results_to_save = rebalance_results.copy()
        if 'weights' in rebalance_results_to_save.columns:
            rebalance_results_to_save['weights'] = rebalance_results_to_save['weights'].apply(
                lambda w: np.array2string(w, separator=',') if isinstance(w, np.ndarray) else w
            )
        rebalance_results_to_save.to_csv(weights_path)
        logging.info("Successfully saved weights.")

        logging.info(f"Attempting to save metrics to {metrics_path}...")
        performance_metrics.to_csv(metrics_path)
        logging.info("Successfully saved metrics.")

        # --- Save Daily Returns for Plotting ---
        equal_weighted_returns = asset_returns.mean(axis=1)
        all_returns = pd.DataFrame({
            'CVaR Portfolio': portfolio_returns,
            'SPY Benchmark': benchmark_returns,
            'Equal-Weighted Benchmark': equal_weighted_returns
        }).dropna()

        returns_path = results_path / "daily_returns.csv"
        logging.info(f"Attempting to save daily returns to {returns_path}...")
        try:
            all_returns.to_csv(returns_path)
            logging.info("Successfully saved daily returns.")
        except Exception as e:
            logging.error(f"Failed to save daily returns: {e}")

        logging.info(f"Results saved to {results_path.resolve()}")
    except Exception as e:
        logging.error(f"CRITICAL: Failed to save results to disk: {e}")
    logging.info("--- Full Backtest Script Finished ---")

    print("\n--- Performance Metrics ---")
    print(performance_metrics)


if __name__ == "__main__":
    asyncio.run(main())
