import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
RESULTS_DIR = "d:/Quantoro/results"
BASELINE_RETURNS_PATH = os.path.join(RESULTS_DIR, "baseline_daily_returns.csv")
ML_RETURNS_PATH = os.path.join(RESULTS_DIR, "ml_alpha_returns.csv")
OUTPUT_PLOT_PATH = os.path.join(RESULTS_DIR, "performance_comparison.png")


def plot_cumulative_returns():
    """Loads, processes, and plots the cumulative returns of different strategies."""
    print("--- Generating Performance Comparison Plot ---")

    # --- Load Data ---
    print(f"Loading baseline returns from {BASELINE_RETURNS_PATH}")
    baseline_df = pd.read_csv(BASELINE_RETURNS_PATH, index_col=0, parse_dates=True)

    print(f"Loading ML Alpha returns from {ML_RETURNS_PATH}")
    ml_df = pd.read_csv(ML_RETURNS_PATH, index_col=0, parse_dates=True)
    ml_df.columns = ["ML_Alpha"]

    # --- Data Preparation ---
    # The baseline file contains both the baseline strategy and the SPY benchmark
    spy_returns = baseline_df["SPY"]
    baseline_returns = baseline_df["Baseline_CVaR"]

    # Combine all returns into a single DataFrame, aligning by date
    combined_df = pd.concat([baseline_returns, ml_df["ML_Alpha"], spy_returns], axis=1)
    combined_df = combined_df.loc[ml_df.index]  # Align to the ML backtest period
    combined_df.columns = ["Baseline CVaR", "ML Alpha-Aware CVaR", "SPY Benchmark"]
    combined_df.fillna(0, inplace=True)

    # --- Calculate Cumulative Returns ---
    cumulative_returns = (1 + combined_df).cumprod() - 1

    # --- Plotting ---
    print(f"Generating and saving plot to {OUTPUT_PLOT_PATH}")
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))

    cumulative_returns.plot(ax=ax, lw=2)

    # CRITICAL FIX: Set x-axis limits to actual data range to avoid plotting into the future
    ax.set_xlim(cumulative_returns.index.min(), cumulative_returns.index.max())

    ax.set_title(
        "Comparative Performance: ML Alpha vs. Baseline vs. SPY", fontsize=18, fontweight="bold"
    )
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Cumulative Returns", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.legend(title="Strategy", fontsize=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT_PATH, dpi=300)
    print("--- Plotting Complete ---")


if __name__ == "__main__":
    plot_cumulative_returns()
