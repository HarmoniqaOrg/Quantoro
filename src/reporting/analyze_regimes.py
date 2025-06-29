# src/reporting/analyze_regimes.py

import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# --- Configuration ---
RESULTS_DIR = "results"
IMG_DIR = os.path.join(RESULTS_DIR, "img")
REGIME_FILE = os.path.join(RESULTS_DIR, "regime_ts.csv")
PRICE_FILE = os.path.join(RESULTS_DIR, "sp500_prices_2010_2024.csv")
OUTPUT_PLOT_FILE = os.path.join(IMG_DIR, "regime_analysis_plot.png")

# Ensure the output directory exists
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

# --- Load Data ---
print("Loading data...")
regimes = pd.read_csv(REGIME_FILE, index_col=0, parse_dates=True)
prices = pd.read_csv(PRICE_FILE, index_col=0, parse_dates=True)
spy_prices = prices[["SPY"]]

# Align data to the backtest period (2020-2024)
backtest_start_date = "2020-01-01"
regimes = regimes[regimes.index >= backtest_start_date]
spy_prices = spy_prices[spy_prices.index >= backtest_start_date]

# Combine data for analysis
analysis_df = spy_prices.join(regimes)
analysis_df["daily_return"] = analysis_df["SPY"].pct_change()
analysis_df.dropna(inplace=True)

# --- Analyze Regimes ---
print("Analyzing regime characteristics...")
regime_stats = (
    analysis_df.groupby("regime")["daily_return"]
    .agg(["mean", "std", "count"])
    .rename(
        columns={"mean": "Mean Daily Return", "std": "Daily Volatility", "count": "Days in Regime"}
    )
)
regime_stats["Annualized Return"] = regime_stats["Mean Daily Return"] * 252
regime_stats["Annualized Volatility"] = regime_stats["Daily Volatility"] * (252**0.5)

print("\nRegime Characteristics:")
print(regime_stats)

# --- Generate Visualization ---
print(f"\nGenerating and saving plot to {OUTPUT_PLOT_FILE}...")
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(15, 7))

# Plot SPY price
ax.plot(analysis_df.index, analysis_df["SPY"], label="S&P 500 (SPY)", color="black", alpha=0.8)

# Add shaded regions for regimes
risk_off_color = "red"
risk_on_color = "green"

for i in range(len(analysis_df) - 1):
    start_date = analysis_df.index[i]
    end_date = analysis_df.index[i + 1]
    if analysis_df["regime"].iloc[i] == 0:  # Risk-Off
        ax.axvspan(start_date, end_date, color=risk_off_color, alpha=0.2, lw=0)
    else:  # Risk-On
        ax.axvspan(start_date, end_date, color=risk_on_color, alpha=0.2, lw=0)

# Create custom legend patches

risk_off_patch = mpatches.Patch(color=risk_off_color, alpha=0.4, label="Risk-Off Regime")
risk_on_patch = mpatches.Patch(color=risk_on_color, alpha=0.4, label="Risk-On Regime")

ax.set_title("S&P 500 Performance with Detected Market Regimes (2020-2024)", fontsize=16)
ax.set_ylabel("SPY Price")
ax.set_xlabel("Date")
ax.legend(handles=[risk_off_patch, risk_on_patch])
ax.grid(True, which="both", linestyle="--", linewidth=0.5)

plt.tight_layout()
plt.savefig(OUTPUT_PLOT_FILE, dpi=300)
print("Plot saved successfully.")
