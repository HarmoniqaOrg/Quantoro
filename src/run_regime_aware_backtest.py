"""
Run Regime-Aware CVaR Backtest

This script runs a backtest of the CVaR optimization strategy enhanced with
a dynamic, regime-aware parameter model.
"""

import logging
import os
import sys

import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.backtesting.metrics import calculate_raw_metrics, format_metrics_for_display  # noqa: E402
from src.data.processor import DataProcessor  # noqa: E402
from src.optimization.cvar_optimizer import CVaROptimizer, RegimeAwareCVaROptimizer  # noqa: E402
from src.regime.ensemble_regime import EnsembleRegimeDetector  # noqa: E402

# --- Configuration ---
LOG_LEVEL = logging.INFO
RESULTS_DIR = os.path.join(project_root, "results")
DATA_FILE = os.path.join(RESULTS_DIR, "sp500_prices_2010_2024.csv")
BENCHMARK_TICKER = "SPY"
START_DATE = "2010-01-01"
END_DATE = "2024-12-31"
EVALUATION_START_DATE = "2020-01-01"

# Regime-Aware Optimizer Settings
RISK_ON_PARAMS = {
    "alpha": 0.95,  # Standard risk level
    "lasso_penalty": 0.01,  # Moderate diversification
    "max_weight": 0.07,  # Allow higher concentration
}
RISK_OFF_PARAMS = {
    "alpha": 0.99,  # High risk aversion
    "lasso_penalty": 0.05,  # Force high diversification
    "max_weight": 0.03,  # Strict concentration limits
}

# --- Setup ---
os.makedirs(RESULTS_DIR, exist_ok=True)
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
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
    benchmark_returns_full = returns_df[BENCHMARK_TICKER]
    asset_returns_full = returns_df.drop(columns=[BENCHMARK_TICKER])
    tickers = asset_returns_full.columns.tolist()

    # --- Generate Regime Probabilities on Full History ---
    logging.info("Generating market regime probabilities using Ensemble detector on full history...")
    regime_detector = EnsembleRegimeDetector(sma_weight=0.7, mrs_weight=0.3)
    spy_prices = price_df[BENCHMARK_TICKER]
    regime_probs = regime_detector.detect_regime(spy_prices)
    smoothing_window = 10
    regime_probs['risk_off_probability'] = regime_probs['risk_off_probability'].rolling(window=smoothing_window, min_periods=1).mean()
    logging.info("Regime probabilities generated and smoothed.")

    # --- Run Regime-Aware Backtest on Full History for Warm-up ---
    logging.info("Setting up and running regime-aware backtest on full 2010-2024 period...")
    optimizer = RegimeAwareCVaROptimizer(
        risk_on_params=RISK_ON_PARAMS, risk_off_params=RISK_OFF_PARAMS, transaction_cost=0.001, solver="SCS"
    )
    lookback = 252
    rebalance_dates = pd.date_range(start=START_DATE, end=END_DATE, freq="BQ").to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns_full.index)]

    all_weights = {}
    rebalance_results_list = []
    current_weights = pd.Series(1 / len(tickers), index=tickers)

    for date in rebalance_dates:
        start_window = date - pd.DateOffset(days=lookback)
        hist_returns = asset_returns_full.loc[start_window:date]
        if hist_returns.empty:
            continue
        current_regime_prob = regime_probs.loc[date, "risk_off_probability"]
        try:
            opt_result = optimizer.optimize(
                returns=hist_returns, current_weights=current_weights.values, regime_prob=current_regime_prob
            )
            if opt_result and opt_result.status in ["optimal", "optimal_inaccurate"]:
                current_weights = pd.Series(opt_result.weights, index=hist_returns.columns)
                rebalance_results_list.append({"date": date, "status": opt_result.status, "weights": opt_result.weights})
        except Exception as e:
            logging.error(f"Optimization failed on {date}: {e}. Holding weights.")
        all_weights[date] = current_weights

    if not rebalance_results_list:
        logging.error("Backtest failed to produce any rebalance results. Exiting.")
        return

    weights_df_full = pd.DataFrame(all_weights).T.reindex(asset_returns_full.index, method="ffill").dropna()
    daily_returns_raw_full = (weights_df_full * asset_returns_full).sum(axis=1)

    # --- Slice to Evaluation Period and Apply Costs ---
    logging.info(f"Slicing results to evaluation period: {EVALUATION_START_DATE} - {END_DATE}")
    weights_df = weights_df_full.loc[EVALUATION_START_DATE:]
    asset_returns = asset_returns_full.loc[EVALUATION_START_DATE:]
    benchmark_returns = benchmark_returns_full.loc[EVALUATION_START_DATE:]
    daily_returns_raw = daily_returns_raw_full.loc[EVALUATION_START_DATE:]

    weights_df, asset_returns = weights_df.align(asset_returns, join='inner', axis=0)
    daily_returns_raw = daily_returns_raw.reindex(asset_returns.index)
    benchmark_returns = benchmark_returns.reindex(asset_returns.index)

    logging.info("Applying transaction costs for the evaluation period...")
    drifted_weights = weights_df.shift(1) * (1 + asset_returns.shift(1))
    drifted_weights = drifted_weights.div(drifted_weights.sum(axis=1), axis=0).fillna(0)
    turnover = (weights_df - drifted_weights).abs().sum(axis=1)
    transaction_costs = turnover * 0.001
    daily_returns_net = (daily_returns_raw - transaction_costs).dropna()
    daily_returns_net.name = "Regime_Aware_CVaR"

    # --- Calculate and Save Metrics for Evaluation Period ---
    logging.info("Calculating final performance metrics for the evaluation period...")
    raw_metrics = calculate_raw_metrics(daily_returns_net, benchmark_returns, daily_weights=weights_df)
    
    metrics_path = os.path.join(RESULTS_DIR, "task_b_regime_aware_cvar_performance.csv")
    raw_metrics.to_csv(metrics_path, header=True)
    logging.info(f"Saved regime-aware metrics to {metrics_path}")

    weights_path = os.path.join(RESULTS_DIR, "task_b_regime_aware_rebalance_weights.csv")
    weights_df.to_csv(weights_path)
    logging.info(f"Saved evaluation period weights to {weights_path}")

    returns_path = os.path.join(RESULTS_DIR, "task_b_regime_aware_daily_returns.csv")
    daily_returns_net.to_csv(returns_path, header=True)
    logging.info(f"Saved daily returns to {returns_path}")

    regime_probs_path = os.path.join(RESULTS_DIR, "task_b_regime_probabilities.csv")
    regime_probs.loc[EVALUATION_START_DATE:].to_csv(regime_probs_path)
    logging.info(f"Saved regime probabilities for evaluation period to {regime_probs_path}")

    logging.info("--- Backtest Complete ---")
    print("\n--- Regime-Aware Performance Metrics (2020-2024) ---")
    print(format_metrics_for_display(raw_metrics, daily_returns_net))


if __name__ == "__main__":
    main()
