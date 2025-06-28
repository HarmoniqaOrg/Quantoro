import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.regime.ensemble_regime import EnsembleRegimeDetector

# --- Configuration ---
RESULTS_DIR = os.path.join(project_root, "results")
DATA_FILE = os.path.join(RESULTS_DIR, "sp500_prices_2010_2024.csv")
OUTPUT_PLOT_PATH = os.path.join(RESULTS_DIR, "regime_probabilities.png")
BENCHMARK_TICKER = "SPY"
PLOT_START_DATE = "2020-01-01"
PLOT_END_DATE = "2024-12-31"


def plot_regime_probabilities():
    """Generates and saves a plot of market regime probabilities."""
    print("--- Generating Regime Probability Plot ---")

    # --- Load Data ---
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found at {DATA_FILE}")
        return

    print(f"Loading data from {DATA_FILE}")
    price_df = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    spy_prices = price_df[BENCHMARK_TICKER].loc[PLOT_START_DATE:PLOT_END_DATE]
    returns_df = price_df.pct_change()

    # --- Generate Regime Probabilities ---
    print("Generating market regime probabilities...")
    regime_detector = EnsembleRegimeDetector(sma_weight=0.7, mrs_weight=0.3)
    # Optimize by reducing the data passed to the detector to prevent long fitting times
    # We only need data from 2020 onwards for the plot, plus a burn-in period.
    regime_input_prices = price_df[BENCHMARK_TICKER].loc["2019-10-01":PLOT_END_DATE]
    regime_probs = regime_detector.detect_regime(regime_input_prices)
    risk_off_prob = regime_probs["risk_off_probability"].loc[PLOT_START_DATE:PLOT_END_DATE]

    # --- Plotting ---
    print(f"Generating and saving plot to {OUTPUT_PLOT_PATH}")
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax1 = plt.subplots(figsize=(15, 8))

    # Plot SPY price on primary y-axis
    ax1.plot(spy_prices.index, spy_prices, color="cornflowerblue", label="SPY Price", lw=2)
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_ylabel("SPY Price", color="cornflowerblue", fontsize=12)
    ax1.tick_params(axis="y", labelcolor="cornflowerblue")
    ax1.grid(False)

    # Plot Risk-Off probability on secondary y-axis
    ax2 = ax1.twinx()
    ax2.fill_between(
        risk_off_prob.index, risk_off_prob, color="tomato", alpha=0.3, label="Risk-Off Probability"
    )
    ax2.set_ylabel("Risk-Off Probability", color="tomato", fontsize=12)
    ax2.tick_params(axis="y", labelcolor="tomato")
    ax2.set_ylim(0, 1)
    ax2.grid(False)

    # Formatting
    fig.suptitle("Market Regime vs. SPY Price (2020-2024)", fontsize=18, fontweight="bold")
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(OUTPUT_PLOT_PATH, dpi=300)
    print("--- Plotting Complete ---")


if __name__ == "__main__":
    plot_regime_probabilities()
