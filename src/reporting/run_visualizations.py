import pandas as pd
import os
from pathlib import Path
import logging
from .generate_report_visuals import plot_performance_comparison, plot_task_a_comparison

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
ROOT_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT_DIR / "results"

# --- File Paths ---
BASELINE_RETURNS_PATH = RESULTS_DIR / "baseline_daily_returns.csv"
REGIME_RETURNS_PATH = RESULTS_DIR / "regime_aware_daily_returns.csv"
HYBRID_RETURNS_PATH = RESULTS_DIR / "hybrid_model_daily_returns.csv"
ALL_PRICES_PATH = RESULTS_DIR / "sp500_prices_2010_2024.csv"
DAILY_WEIGHTS_PATH = RESULTS_DIR / "baseline_daily_weights.csv"


def load_all_returns_data() -> dict:
    """Loads all available daily returns files into a dictionary of DataFrames."""
    logging.info("Loading all available returns data...")

    paths = {
        "baseline": BASELINE_RETURNS_PATH,
        "regime_aware": REGIME_RETURNS_PATH,
        "hybrid": HYBRID_RETURNS_PATH,
    }

    data_frames = {}
    for name, path in paths.items():
        if path.exists():
            try:
                data_frames[name] = pd.read_csv(path, index_col="date", parse_dates=True)
                logging.info(f"Successfully loaded {path}")
            except Exception as e:
                logging.error(f"Failed to load {path}: {e}")
        else:
            logging.warning(f"File not found: {path}. Skipping.")

    return data_frames


def main():
    """Main function to generate all report visualizations."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("--- Starting Report Visualization Generation ---")

    # Load all returns data
    logging.info("Loading all available returns data...")
    all_returns_data = load_all_returns_data()

    # Load daily weights for turnover calculation
    if DAILY_WEIGHTS_PATH.exists():
        logging.info(f"Loading daily weights from {DAILY_WEIGHTS_PATH}")
        daily_weights_df = pd.read_csv(DAILY_WEIGHTS_PATH, index_col=0, parse_dates=True)
    else:
        logging.warning("Daily weights file not found. Turnover will not be calculated.")
        daily_weights_df = None

    # Generate plots
    if not all_returns_data:
        logging.error("No returns data found. Exiting.")
    else:
        plot_performance_comparison(all_returns_data)
        plot_task_a_comparison(all_returns_data, daily_weights=daily_weights_df)

    logging.info("--- Visualization Generation Finished ---")


if __name__ == "__main__":
    main()
