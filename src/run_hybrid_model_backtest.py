"""
Run Hybrid Regime-Aware Alpha Model Backtest

This script runs a backtest of a hybrid strategy that combines:
1. A dynamic, regime-aware asset allocation model.
2. An ML-driven alpha model to inform stock selection within regimes.
3. Alpha signals derived from filtered FMP data and Google Trends sentiment.
"""

import logging
import os
import sys

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from src.alpha.ml_model import MLAlphaModel  # noqa: E402
from src.backtesting.metrics import calculate_raw_metrics, format_metrics_for_display  # noqa: E402
from src.data.loader import FmpDataLoader, GoogleTrendsLoader  # noqa: E402
from src.data.processor import DataProcessor  # noqa: E402
from src.optimization.cvar_optimizer import AlphaAwareCVaROptimizer  # noqa: E402
from src.regime.ensemble_regime import EnsembleRegimeDetector  # noqa: E402

# --- Configuration ---
LOG_LEVEL = logging.DEBUG
RESULTS_DIR = os.path.join(project_root, "results")
PRICE_DATA_PATH = os.path.join(project_root, "results", "sp500_prices_2010_2024.csv")
BENCHMARK_TICKER = "SPY"
BACKTEST_START_DATE = "2020-01-01"
BACKTEST_END_DATE = "2024-12-31"
FMP_API_KEY = os.getenv("FMP_API_KEY")

# --- Setup ---
os.makedirs(RESULTS_DIR, exist_ok=True)
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()


def build_hybrid_feature_set(
    current_date, returns_data, raw_fmp_signals, trends_data, lookback_days, forward_days
):
    """Builds a feature and target set from all data sources for a given time window."""
    # This function is a placeholder for the complex feature engineering logic.
    # In a real scenario, this would be a more elaborate function like the one in run_ml_alpha_backtest.py
    # For this example, we will simulate its output to focus on the main loop.
    # A full implementation would combine momentum, FMP, and trends features.
    num_assets = len(returns_data.columns)
    num_days = lookback_days

    # Simulate features
    X = pd.DataFrame(
        np.random.rand(num_days * num_assets, 4),
        columns=["mom_1m", "mom_12m", "fmp_alpha", "trends_sentiment"],
    )
    # Simulate target
    y = pd.Series(np.random.rand(num_days * num_assets))

    return X, y


def get_hybrid_prediction_features(current_date, returns_data, raw_fmp_signals, trends_data):
    """Generates features for the current date for prediction."""
    # This is also a placeholder for the real feature generation logic.
    num_assets = len(returns_data.columns)
    X_pred = pd.DataFrame(
        np.random.rand(num_assets, 4),
        columns=["mom_1m", "mom_12m", "fmp_alpha", "trends_sentiment"],
        index=returns_data.columns,
    )
    X_pred.index.name = "ticker"
    return X_pred


def main():
    """Main function to run the hybrid model backtest."""
    logging.info("--- Starting Hybrid Regime-Aware Alpha Model Backtest ---")

    # --- 1. Load All Data Sources ---
    logging.info("Loading all data sources...")
    price_data = pd.read_csv(PRICE_DATA_PATH, index_col="date", parse_dates=True)
    universe = [col for col in price_data.columns if col != BENCHMARK_TICKER]
    data_processor = DataProcessor()
    returns_data = data_processor.calculate_returns(price_data, log_returns=False)
    benchmark_returns = returns_data[BENCHMARK_TICKER]
    asset_returns = returns_data.drop(columns=[BENCHMARK_TICKER])

    logging.info("Fetching FMP premium signals...")
    signal_fetcher = FmpDataLoader(api_key=FMP_API_KEY)
    raw_fmp_signals = signal_fetcher.fetch_all_signals_for_universe_sync(tickers=universe)

    logging.info("Fetching Google Trends data...")
    trends_loader = GoogleTrendsLoader()
    trends_data = trends_loader.get_trends_for_universe(
        universe, start_date="2010-01-01", end_date=BACKTEST_END_DATE
    )
    logging.info("All data loaded.")

    # --- 2. Initialize Models & Detectors ---
    logging.info("Initializing models and detectors...")
    regime_detector = EnsembleRegimeDetector(sma_weight=0.7, mrs_weight=0.3)
    spy_prices = price_data[BENCHMARK_TICKER]
    regime_probs = regime_detector.detect_regime(spy_prices)
    ml_alpha_model = MLAlphaModel()
    optimizer = AlphaAwareCVaROptimizer(transaction_cost=0.001, solver="SCS")

    # --- 3. Run Rolling Backtest ---
    logging.info("Running rolling backtest with dynamic regimes and ML alpha...")
    rebalance_dates = pd.date_range(
        start=BACKTEST_START_DATE, end=BACKTEST_END_DATE, freq="Q"
    ).to_series()
    rebalance_dates = rebalance_dates[rebalance_dates.isin(asset_returns.index)]
    logging.info(f"Found {len(rebalance_dates)} rebalancing dates.")

    all_weights = {}
    current_weights = pd.Series(1 / len(universe), index=universe)

    for date in tqdm(rebalance_dates, desc="Running Hybrid Backtest"):
        hist_returns = asset_returns.loc[:date].tail(252)
        if hist_returns.shape[0] < 252:
            continue

        # 3.1: Determine regime and set optimizer parameters
        risk_off_prob = regime_probs.loc[date, "risk_off_probability"]
        if risk_off_prob > 0.5:
            optimizer.set_params(alpha=0.99, lasso_penalty=0.05, max_weight=0.03)
        else:
            optimizer.set_params(alpha=0.95, lasso_penalty=0.01, max_weight=0.07)

        # 3.2: Build features and train ML model
        X_train, y_train = build_hybrid_feature_set(
            date, hist_returns, raw_fmp_signals, trends_data, 252, 63
        )
        ml_alpha_model.train_model(X_train, y_train)

        # 3.3: Generate alpha scores for current date
        X_pred = get_hybrid_prediction_features(date, hist_returns, raw_fmp_signals, trends_data)
        alpha_scores = ml_alpha_model.predict_alpha(X_pred)

        # 3.4: Run optimization
        try:
            opt_result = optimizer.optimize(
                returns=hist_returns,
                alpha_scores=alpha_scores,
                benchmark_returns=benchmark_returns.loc[hist_returns.index],
                current_weights=current_weights.values,
            )
            if opt_result and opt_result.status in ["optimal", "optimal_inaccurate"]:
                current_weights = pd.Series(opt_result.weights, index=hist_returns.columns)
            else:
                logging.warning(f"Optimization non-optimal on {date}. Holding weights.")
        except Exception as e:
            logging.error(f"Optimization failed on {date}: {e}. Holding weights.")

        all_weights[date] = current_weights

    # --- 4. Calculate and Save Metrics ---
    logging.info("Calculating and saving performance metrics...")
    weights_df = pd.DataFrame(all_weights).T.reindex(asset_returns.index, method="ffill").dropna()
    logging.info(f"Generated weights_df with shape: {weights_df.shape}")
    if weights_df.empty:
        logging.error(
            "Backtest generated no weights. Performance file will not be created. Exiting."
        )
        return

    daily_returns = (
        (weights_df * asset_returns).sum(axis=1).loc[BACKTEST_START_DATE:BACKTEST_END_DATE]
    )
    logging.info(f"Generated daily_returns with shape: {daily_returns.shape}")
    if daily_returns.empty:
        logging.error(
            "Backtest generated no returns. Performance file will not be created. Exiting."
        )
        return

    raw_metrics = calculate_raw_metrics(daily_returns, benchmark_returns)
    display_metrics = format_metrics_for_display(raw_metrics, daily_returns)

    metrics_path = os.path.join(RESULTS_DIR, "hybrid_model_performance.csv")
    weights_path = os.path.join(RESULTS_DIR, "hybrid_model_weights.csv")
    raw_metrics.to_csv(metrics_path, header=True)
    weights_df.to_csv(weights_path)

    logging.info(f"Results saved to {RESULTS_DIR}")
    logging.info("--- Hybrid Backtest Complete ---")
    print("\n--- Hybrid Model Performance Metrics ---")
    print(display_metrics)


if __name__ == "__main__":
    main()
