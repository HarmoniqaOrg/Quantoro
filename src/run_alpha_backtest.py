"""
Run Alpha-Aware CVaR Backtest

This script runs a backtest of the CVaR optimization strategy enhanced with
alternative data alpha signals.
"""

import os
import sys
import logging
import pandas as pd
import asyncio
from dotenv import load_dotenv

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.data.loader import FmpDataLoader
from src.data.processor import DataProcessor
from src.optimization.cvar_optimizer import AlphaAwareCVaROptimizer, RollingCVaROptimizer
from src.backtesting.metrics import calculate_performance_metrics
from src.alpha.fmp_signals import FmpPremiumSignals
from src.alpha.signal_processor import SignalProcessor

# --- Configuration ---
LOG_LEVEL = logging.INFO
RESULTS_DIR = os.path.join(project_root, 'results')
DATA_FILE = os.path.join(RESULTS_DIR, 'sp500_prices_2010_2024.csv')
BENCHMARK_TICKER = 'SPY'
BACKTEST_START_DATE = '2020-01-01'
BACKTEST_END_DATE = '2024-01-01'

# Optimizer settings
CVAR_ALPHA = 0.95
MAX_WEIGHT = 0.05
LASSO_PENALTY = 0.01
ALPHA_FACTOR = 0.05 # Weight of the alpha signal in the objective

# --- Setup ---
os.makedirs(RESULTS_DIR, exist_ok=True)
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

async def generate_alpha_scores(tickers: list, api_key: str) -> pd.DataFrame:
    """Fetches and processes FMP signals to generate composite alpha scores."""
    logging.info("Generating alpha scores from FMP signals...")
    signal_fetcher = FmpPremiumSignals(api_key=api_key)
    all_signals = await signal_fetcher.get_all_signals_for_universe(tickers)

    processor = SignalProcessor(signals_data=all_signals)
    alpha_scores = processor.generate_composite_alpha_scores()
    
    # We need to create a timeseries of alpha scores. For this test, we assume
    # the scores are constant over the backtest period. In a real system,
    # these would be updated daily.
    backtest_dates = pd.date_range(start=BACKTEST_START_DATE, end=BACKTEST_END_DATE)
    alpha_scores_df = pd.DataFrame(index=backtest_dates, columns=tickers)
    
    for ticker in tickers:
        if ticker in alpha_scores.index:
            alpha_scores_df[ticker] = alpha_scores.loc[ticker, 'alpha_score']

    logging.info("Alpha scores generated.")
    return alpha_scores_df.fillna(0)

def main():
    """Main function to run the alpha-aware backtest."""
    logging.info("--- Starting Alpha-Aware CVaR Backtest ---")

    # --- Load Data ---
    logging.info(f"Loading data from {DATA_FILE}")
    try:
        price_df = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    except FileNotFoundError:
        logging.error(f"Data file not found at {DATA_FILE}. Please run the data loader first.")
        return

    processor = DataProcessor()
    returns_df = processor.calculate_returns(price_df).dropna()
    benchmark_returns = returns_df[BENCHMARK_TICKER]
    asset_returns = returns_df.drop(columns=[BENCHMARK_TICKER])
    
    # --- Generate Alpha Scores ---
    fmp_api_key = os.getenv('FMP_API_KEY')
    if not fmp_api_key:
        logging.error("FMP_API_KEY not found in environment variables.")
        return
    
    tickers = asset_returns.columns.tolist()
    alpha_scores_df = asyncio.run(generate_alpha_scores(tickers, fmp_api_key))
    
    # --- Run Backtest ---
    logging.info("Setting up alpha-aware optimizer...")
    alpha_optimizer = AlphaAwareCVaROptimizer(
        alpha=CVAR_ALPHA,
        lasso_penalty=LASSO_PENALTY,
        max_weight=MAX_WEIGHT,
        alpha_factor=ALPHA_FACTOR
    )

    rolling_optimizer = RollingCVaROptimizer(
        optimizer=alpha_optimizer,
        lookback_window=252,
        rebalance_frequency='M' # Monthly rebalancing
    )

    logging.info("Running rolling backtest with alpha signals...")
    rebalance_results, daily_returns = rolling_optimizer.backtest(
        returns=asset_returns,
        benchmark_returns=benchmark_returns,
        start_date=BACKTEST_START_DATE,
        end_date=BACKTEST_END_DATE,
        alpha_scores=alpha_scores_df
    )

    if daily_returns.empty:
        logging.error("Backtest failed to produce returns. Exiting.")
        return

    # --- Calculate and Save Metrics ---
    logging.info("Calculating performance metrics...")
    performance_metrics = calculate_performance_metrics(daily_returns, benchmark_returns)

    # Save results
    weights_path = os.path.join(RESULTS_DIR, 'alpha_aware_weights.csv')
    metrics_path = os.path.join(RESULTS_DIR, 'alpha_aware_performance.csv')
    returns_path = os.path.join(RESULTS_DIR, 'alpha_aware_daily_returns.csv')

    rebalance_results['weights'].apply(lambda w: pd.Series(w, index=asset_returns.columns)).to_csv(weights_path)
    pd.DataFrame([performance_metrics]).to_csv(metrics_path, index=False)
    daily_returns.to_csv(returns_path)

    logging.info(f"Results saved to {RESULTS_DIR}")
    logging.info("--- Backtest Complete ---")
    print("\n--- Alpha-Aware Performance Metrics ---")
    for metric, value in performance_metrics.items():
        print(f"{metric}: {value}")

if __name__ == "__main__":
    main()
