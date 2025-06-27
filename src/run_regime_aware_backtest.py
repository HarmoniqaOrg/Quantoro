"""
Run Regime-Aware CVaR Backtest

This script runs a backtest of the CVaR optimization strategy enhanced with
a dynamic, regime-aware parameter model.
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
from src.optimization.cvar_optimizer import RegimeAwareCVaROptimizer
from src.backtesting.metrics import calculate_raw_metrics, format_metrics_for_display
from src.regime.ensemble_regime import EnsembleRegimeDetector

# --- Configuration ---
LOG_LEVEL = logging.INFO
RESULTS_DIR = os.path.join(project_root, 'results')
DATA_FILE = os.path.join(RESULTS_DIR, 'sp500_prices_2010_2024.csv')
BENCHMARK_TICKER = 'SPY'
BACKTEST_START_DATE = '2020-01-01'
BACKTEST_END_DATE = '2024-12-31'

# Regime-Aware Optimizer Settings
RISK_ON_PARAMS = {
    'alpha': 0.95,          # Standard risk level
    'lasso_penalty': 0.01,  # Moderate diversification
    'max_weight': 0.07       # Allow higher concentration
}
RISK_OFF_PARAMS = {
    'alpha': 0.99,          # High risk aversion
    'lasso_penalty': 0.05,  # Force high diversification
    'max_weight': 0.03       # Strict concentration limits
}

# --- Setup ---
os.makedirs(RESULTS_DIR, exist_ok=True)
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()



def main():
    """Main function to run the regime-aware backtest."""
    logging.info("--- Starting Regime-Aware CVaR Backtest ---")

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
    tickers = asset_returns.columns.tolist()

    # --- Generate Regime Probabilities ---
    logging.info("Generating market regime probabilities using Ensemble detector...")
    regime_detector = EnsembleRegimeDetector(sma_weight=0.7, mrs_weight=0.3)
    spy_prices = price_df[BENCHMARK_TICKER]
    regime_probs = regime_detector.detect_regime(spy_prices)
    logging.info("Regime probabilities generated.")


    
    # --- Run Backtest ---
    logging.info("Setting up regime-aware optimizer...")
    optimizer = RegimeAwareCVaROptimizer(
        risk_on_params=RISK_ON_PARAMS,
        risk_off_params=RISK_OFF_PARAMS,
        transaction_cost=0.001
    )

    logging.info("Running rolling backtest with dynamic regime parameters...")
    lookback = 252 # 1 year
    rebalance_dates = pd.date_range(start=BACKTEST_START_DATE, end=BACKTEST_END_DATE, freq='BQ').to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns.index)]
    logging.info(f"Found {len(rebalance_dates)} rebalancing dates between {BACKTEST_START_DATE} and {BACKTEST_END_DATE}.")

    all_weights = {}
    rebalance_results_list = []
    current_weights = pd.Series(1/len(tickers), index=tickers)

    for date in rebalance_dates:
        start_window = date - pd.DateOffset(days=lookback)
        hist_returns = asset_returns.loc[start_window:date]
        hist_benchmark = benchmark_returns.loc[start_window:date]

        if hist_returns.empty:
            logging.warning(f"Not enough historical data for {date}. Skipping rebalance.")
            continue

        # Get the regime probability for the current rebalance date
        # Select the specific 'risk_on_probability' to pass a single float to the optimizer
        # Pass the 'risk_off_probability' to the optimizer, as its logic is scaled by risk-off.
        current_regime_prob = regime_probs['risk_off_probability'].loc[date]

        try:
            opt_result = optimizer.optimize(
                returns=hist_returns,
                benchmark_returns=hist_benchmark,
                current_weights=current_weights.values,
                regime_prob=current_regime_prob
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
    logging.info(f"Weights DataFrame created with shape: {weights_df.shape}")
    if weights_df.empty:
        logging.warning("Weights DataFrame is empty after processing. This will result in no returns.")

    daily_returns = (weights_df * asset_returns).sum(axis=1).loc[BACKTEST_START_DATE:BACKTEST_END_DATE]
    logging.info(f"Daily returns series generated with {len(daily_returns)} entries.")

    if daily_returns.empty:
        logging.error("Backtest failed to produce returns. Exiting.")
        return

    # --- Calculate and Save Metrics ---
    logging.info("Calculating performance metrics...")
    raw_metrics = calculate_raw_metrics(daily_returns, benchmark_returns)
    display_metrics = format_metrics_for_display(raw_metrics, daily_returns)

    # Save results
    weights_path = os.path.join(RESULTS_DIR, 'regime_aware_weights.csv')
    metrics_path = os.path.join(RESULTS_DIR, 'regime_aware_cvar_performance.csv')
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
        if 'regime_aware_cvar_index' in consolidated_returns_df.columns:
            consolidated_returns_df = consolidated_returns_df.drop(columns=['regime_aware_cvar_index'])

        # Add the new strategy's returns
        daily_returns.name = 'regime_aware_cvar_index'
        consolidated_returns_df = consolidated_returns_df.join(daily_returns, how='outer')
        
        # Save the updated dataframe
        consolidated_returns_df.to_csv(consolidated_returns_path)
        logging.info("Successfully updated consolidated returns.")

    except FileNotFoundError:
        logging.error(f"{consolidated_returns_path} not found. This script should run after baseline and enhanced backtests.")
        # As a fallback, save its own returns, but this indicates a pipeline issue.
        daily_returns.to_csv(os.path.join(RESULTS_DIR, 'regime_aware_daily_returns.csv'))

    logging.info(f"Results saved to {RESULTS_DIR}")
    logging.info("--- Backtest Complete ---")
    print("\n--- Regime-Aware Performance Metrics ---")
    print(display_metrics)


if __name__ == "__main__":
    main()
