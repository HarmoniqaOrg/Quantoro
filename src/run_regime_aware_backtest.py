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
BACKTEST_START_DATE = "2020-01-01"
BACKTEST_END_DATE = "2024-12-31"

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


def run_baseline_for_comparison(asset_returns, benchmark_returns, tickers):
    """Runs the baseline CVaR backtest for the 2020-2024 period for comparison."""
    logging.info("--- Running Baseline CVaR Backtest for 2020-2024 Comparison ---")
    optimizer = CVaROptimizer(
        alpha=0.95,
        lasso_penalty=0.01,
        max_weight=0.05,
        transaction_cost=0.001,
        solver="SCS",
    )

    lookback = 252
    rebalance_dates = pd.date_range(
        start=BACKTEST_START_DATE, end=BACKTEST_END_DATE, freq="BQ"
    ).to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns.index)]

    all_weights = {}
    current_weights = pd.Series(1 / len(tickers), index=tickers)

    for date in rebalance_dates:
        start_window = date - pd.DateOffset(days=lookback)
        hist_returns = asset_returns.loc[start_window:date]
        if hist_returns.empty:
            continue
        try:
            opt_result = optimizer.optimize(returns=hist_returns, current_weights=current_weights.values)
            if opt_result and opt_result.status in ["optimal", "optimal_inaccurate"]:
                current_weights = pd.Series(opt_result.weights, index=hist_returns.columns)
        except Exception:
            pass  # Hold weights on failure
        all_weights[date] = current_weights

    weights_df = pd.DataFrame(all_weights).T.reindex(asset_returns.index, method="ffill").dropna()
    daily_returns_raw = (weights_df * asset_returns).sum(axis=1)

    # Apply transaction costs
    drifted_weights = weights_df.shift(1) * (1 + asset_returns.shift(1))
    drifted_weights = drifted_weights.div(drifted_weights.sum(axis=1), axis=0).fillna(0)
    turnover = (weights_df - drifted_weights).abs().sum(axis=1)
    transaction_costs = turnover * 0.001
    daily_returns_net = (daily_returns_raw - transaction_costs).loc[BACKTEST_START_DATE:BACKTEST_END_DATE]

    # Calculate and save metrics
    raw_metrics = calculate_raw_metrics(daily_returns_net, benchmark_returns)
    metrics_path = os.path.join(RESULTS_DIR, "baseline_cvar_performance_2020-2024.csv")
    raw_metrics.to_csv(metrics_path, header=True)
    logging.info(f"Saved comparable baseline metrics to {metrics_path}")


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
    benchmark_returns = returns_df[BENCHMARK_TICKER].loc[BACKTEST_START_DATE:BACKTEST_END_DATE]
    asset_returns = returns_df.drop(columns=[BENCHMARK_TICKER]).loc[BACKTEST_START_DATE:BACKTEST_END_DATE]
    tickers = asset_returns.columns.tolist()

    # --- Run Baseline for Comparison ---
    run_baseline_for_comparison(asset_returns.copy(), benchmark_returns.copy(), tickers)

    # --- Generate Regime Probabilities ---
    logging.info("Generating market regime probabilities using Ensemble detector...")
    regime_detector = EnsembleRegimeDetector(sma_weight=0.7, mrs_weight=0.3)
    spy_prices = price_df[BENCHMARK_TICKER]
    regime_probs = regime_detector.detect_regime(spy_prices)
    logging.info("Regime probabilities generated.")

    # --- Run Regime-Aware Backtest ---
    logging.info("Setting up regime-aware optimizer...")
    optimizer = RegimeAwareCVaROptimizer(
        risk_on_params=RISK_ON_PARAMS,
        risk_off_params=RISK_OFF_PARAMS,
        transaction_cost=0.001,
        solver="SCS",
    )

    logging.info("Running rolling backtest with dynamic regime parameters...")
    lookback = 252
    rebalance_dates = pd.date_range(
        start=BACKTEST_START_DATE, end=BACKTEST_END_DATE, freq="BQ"
    ).to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns.index)]
    logging.info(f"Found {len(rebalance_dates)} rebalancing dates.")

    all_weights = {}
    rebalance_results_list = []
    current_weights = pd.Series(1 / len(tickers), index=tickers)

    for date in rebalance_dates:
        start_window = date - pd.DateOffset(days=lookback)
        hist_returns = asset_returns.loc[start_window:date]
        hist_benchmark = benchmark_returns.loc[start_window:date]
        if hist_returns.empty:
            logging.warning(f"Not enough historical data for {date}. Skipping rebalance.")
            continue
        current_regime_prob = regime_probs["risk_off_probability"].loc[date]
        try:
            opt_result = optimizer.optimize(
                returns=hist_returns,
                benchmark_returns=hist_benchmark,
                current_weights=current_weights.values,
                regime_prob=current_regime_prob,
            )
            if opt_result and opt_result.status in ["optimal", "optimal_inaccurate"]:
                current_weights = pd.Series(opt_result.weights, index=hist_returns.columns)
                rebalance_results_list.append({"date": date, "status": opt_result.status, "weights": opt_result.weights})
            else:
                status = opt_result.status if opt_result else "unknown failure"
                logging.warning(f"Optimization non-optimal on {date} with status {status}. Holding weights.")
                rebalance_results_list.append({"date": date, "status": status, "weights": current_weights.values})
        except Exception as e:
            logging.error(f"Optimization failed on {date}: {e}. Holding weights.")
            rebalance_results_list.append({"date": date, "status": "failure", "weights": current_weights.values})
        all_weights[date] = current_weights

    # --- Process and Save Results ---
    if not rebalance_results_list:
        logging.error("Backtest failed to produce any rebalance results. Exiting.")
        return

    weights_df = pd.DataFrame(all_weights).T.reindex(asset_returns.index, method="ffill").dropna()
    daily_returns_raw = (weights_df * asset_returns).sum(axis=1)

    # Apply transaction costs
    logging.info("Applying transaction costs to regime-aware returns...")
    drifted_weights = weights_df.shift(1) * (1 + asset_returns.shift(1))
    drifted_weights = drifted_weights.div(drifted_weights.sum(axis=1), axis=0).fillna(0)
    turnover = (weights_df - drifted_weights).abs().sum(axis=1)
    transaction_costs = turnover * 0.001
    daily_returns_net = daily_returns_raw - transaction_costs

    # Clean up returns series for saving
    first_rebalance_date = rebalance_dates.iloc[0]
    final_returns = daily_returns_net.loc[first_rebalance_date:].copy()
    final_returns.name = "Regime_Aware_CVaR"
    logging.info(f"Final daily returns series generated with {len(final_returns)} entries.")

    # Calculate and save metrics
    logging.info("Calculating performance metrics...")
    raw_metrics = calculate_raw_metrics(final_returns, benchmark_returns)
    metrics_path = os.path.join(RESULTS_DIR, "regime_aware_cvar_performance.csv")
    raw_metrics.to_csv(metrics_path, header=True)
    logging.info(f"Saved regime-aware metrics to {metrics_path}")

    # Save weights
    weights_path = os.path.join(RESULTS_DIR, "regime_aware_rebalance_weights.csv")
    pd.DataFrame.from_records(rebalance_results_list).set_index("date")["weights"].apply(
        lambda w: pd.Series(w, index=asset_returns.columns)
    ).to_csv(weights_path)
    logging.info(f"Saved rebalance weights to {weights_path}")

    # Save daily returns
    returns_path = os.path.join(RESULTS_DIR, "regime_aware_daily_returns.csv")
    final_returns.to_csv(returns_path, header=True)
    logging.info(f"Saved daily returns to {returns_path}")

    logging.info(f"Results saved to {RESULTS_DIR}")
    logging.info("--- Backtest Complete ---")
    print("\n--- Regime-Aware Performance Metrics ---")
    print(raw_metrics)


if __name__ == "__main__":
    main()
