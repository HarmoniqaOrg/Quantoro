"""
Run Alpha-Aware CVaR Backtest

This script runs a backtest of the CVaR optimization strategy enhanced with
alternative data alpha signals.
"""

import os
import sys
import logging
import numpy as np
import pandas as pd
import asyncio
from dotenv import load_dotenv

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.data.loader import FmpDataLoader
from src.data.processor import DataProcessor
from src.optimization.cvar_optimizer import AlphaAwareCVaROptimizer, RollingCVaROptimizer
from src.backtesting.metrics import calculate_raw_metrics, format_metrics_for_display
from src.alpha.fmp_signals import FmpPremiumSignals
from src.alpha.signal_processor import SignalProcessor

# --- Configuration ---
LOG_LEVEL = logging.INFO
RESULTS_DIR = os.path.join(project_root, 'results')
DATA_FILE = os.path.join(RESULTS_DIR, 'sp500_prices_2010_2024.csv')
BENCHMARK_TICKER = 'SPY'
BACKTEST_START_DATE = '2020-01-01'
BACKTEST_END_DATE = '2024-12-31'

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
        lasso_penalty=0.8,      # Moderate - balance between signals and diversification
        max_weight=MAX_WEIGHT,
        alpha_factor=0.1,       # Increased from 0.05 to give more weight to alpha
        transaction_cost=0.001
    )

    logging.info("Running rolling backtest with alpha signals...")
    lookback = 252 # 1 year
    # Use quarterly rebalancing to match other strategies
    rebalance_dates = pd.date_range(start=BACKTEST_START_DATE, end=BACKTEST_END_DATE, freq='BQ').to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns.index)]

    all_weights = {}
    rebalance_results_list = []
    current_weights = pd.Series(1/len(tickers), index=tickers)

    for date in rebalance_dates:
        start_window = date - pd.DateOffset(days=lookback)
        hist_returns = asset_returns.loc[start_window:date]
        hist_benchmark = benchmark_returns.loc[start_window:date]
        # Get the alpha scores for the current rebalance date
        current_alpha_scores = alpha_scores_df.loc[date]

        try:
            opt_result = alpha_optimizer.optimize(
                returns=hist_returns,
                benchmark_returns=hist_benchmark,
                current_weights=current_weights.values,
                alpha_scores=current_alpha_scores
            )
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
    daily_returns = (weights_df * asset_returns).sum(axis=1).loc[BACKTEST_START_DATE:BACKTEST_END_DATE]

    if daily_returns.empty:
        logging.error("Backtest failed to produce returns. Exiting.")
        return

    # --- Calculate and Save Metrics ---
    logging.info("Calculating performance metrics...")
    raw_metrics = calculate_raw_metrics(daily_returns, benchmark_returns)
    display_metrics = format_metrics_for_display(raw_metrics, daily_returns)

    # Save results
    weights_path = os.path.join(RESULTS_DIR, 'alpha_aware_weights.csv')
    metrics_path = os.path.join(RESULTS_DIR, 'alpha_aware_cvar_performance.csv')
    consolidated_returns_path = os.path.join(RESULTS_DIR, 'daily_returns.csv')

    # Save strategy-specific files
    rebalance_results['weights'].apply(lambda w: pd.Series(w, index=asset_returns.columns)).to_csv(weights_path)
    raw_metrics.to_csv(metrics_path, header=True)

    # Update and save consolidated daily returns
    logging.info(f"Updating consolidated returns file: {consolidated_returns_path}")
    try:
        # Load existing returns
        consolidated_returns_df = pd.read_csv(consolidated_returns_path, index_col=0, parse_dates=True)
        
        # If the column already exists from a previous run, drop it to ensure idempotency
        if 'alpha_aware_cvar_index' in consolidated_returns_df.columns:
            consolidated_returns_df = consolidated_returns_df.drop(columns=['alpha_aware_cvar_index'])

        # Add the new strategy's returns
        daily_returns.name = 'alpha_aware_cvar_index'
        consolidated_returns_df = consolidated_returns_df.join(daily_returns, how='outer')
        
        # Save the updated dataframe
        consolidated_returns_df.to_csv(consolidated_returns_path)
        logging.info("Successfully updated consolidated returns.")

    except FileNotFoundError:
        logging.error(f"{consolidated_returns_path} not found. This script should run after baseline and enhanced backtests.")
        # As a fallback, save its own returns, but this indicates a pipeline issue.
        daily_returns.to_csv(os.path.join(RESULTS_DIR, 'alpha_aware_daily_returns.csv'))

    logging.info(f"Results saved to {RESULTS_DIR}")
    logging.info("--- Backtest Complete ---")
    print("\n--- Alpha-Aware Performance Metrics ---")
    print(display_metrics)

if __name__ == "__main__":
    main()
