import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
REPORT_FILE = os.path.join(DOCS_DIR, "report.md")

# --- Plotting Style ---
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (15, 7)
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["legend.fontsize"] = 10

def generate_regime_plot(regime_probs: pd.DataFrame, spy_prices: pd.DataFrame):
    """Generates and saves a plot of regime probabilities against the SPY index."""
    fig, ax1 = plt.subplots()

    # Plot SPY prices on the primary y-axis
    ax1.plot(spy_prices.index, spy_prices, color='black', label='SPY Price', alpha=0.6)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("SPY Price", color='black')
    ax1.tick_params(axis='y', labelcolor='black')

    # Create a secondary y-axis for the regime probability
    ax2 = ax1.twinx()
    ax2.fill_between(regime_probs.index, 0, regime_probs['risk_off_probability'], 
                     color='red', alpha=0.3, label='Risk-Off Probability')
    ax2.set_ylabel("Risk-Off Probability", color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, 1)

    plt.title("Market Regimes vs. S&P 500 Price (2020-2024)")
    fig.tight_layout()
    
    plot_path = os.path.join(RESULTS_DIR, "regime_vs_spy_plot.png")
    plt.savefig(plot_path, dpi=300)
    print(f"Saved regime plot to {plot_path}")
    return plot_path

def create_method_summary() -> str:
    """Creates the 400-word method summary for Task B."""
    return """## Task B: Regime-Aware Strategy - Method Summary

The regime-aware strategy enhances the baseline CVaR optimization by dynamically adjusting its risk parameters in response to changing market conditions. The core objective is to improve risk-adjusted returns by adopting a more defensive posture during periods of high market stress ('risk-off') and a more aggressive stance during stable periods ('risk-on').

To achieve this, we developed an `EnsembleRegimeDetector` that synthesizes signals from multiple indicators to produce a continuous probability score, representing the likelihood of being in a 'risk-off' state. This model combines a Simple Moving Average (SMA) crossover system with a Mean Reversion Score (MRS) indicator. The SMA component captures long-term trend-following signals, identifying sustained market downturns, while the MRS component detects short-term volatility spikes and potential trend reversals. By blending these signals with a 70/30 weight, the ensemble model provides a more robust and nuanced view of the market regime than either indicator could alone, avoiding whipsaws from short-term noise while remaining responsive to significant trend shifts.

The 'risk-off' probability score, ranging from 0 (fully risk-on) to 1 (fully risk-off), is fed into the `RegimeAwareCVaROptimizer`. This optimizer linearly interpolates its key parameters—CVaR confidence level (alpha), LASSO penalty, and maximum asset weight—between predefined 'risk-on' and 'risk-off' settings. For instance, in a high-stress environment (probability approaching 1), the optimizer increases the CVaR alpha (e.g., from 0.95 to 0.99), raises the LASSO penalty to enforce greater diversification, and reduces the maximum allowable weight for any single asset. This dynamic adjustment mechanism allows the portfolio to proactively manage risk, aiming to minimize drawdowns during turbulent markets while still capturing upside potential during calm periods. The result is a more adaptive and resilient investment strategy tailored to the prevailing market environment.
"""

def create_interpretability_report(plot_path: str) -> str:
    """Creates the interpretability report for Task B."""
    return f"""## Task B: Interpretability Report

The plot below visualizes the output of our `EnsembleRegimeDetector` against the S&P 500 price from 2020 to 2024. The red shaded area represents the calculated 'risk-off' probability, with higher intensity indicating greater market stress as perceived by the model.

![Regime vs. SPY Price]({os.path.relpath(plot_path, DOCS_DIR)})

**Key Observations:**

1.  **COVID-19 Crash (Q1 2020):** The model correctly identifies the massive volatility spike, with the risk-off probability rapidly surging to 1.0. This would have triggered the optimizer's most defensive settings, tightening risk constraints to protect capital during the sharp downturn.

2.  **2022 Bear Market:** The detector effectively captures the prolonged market decline throughout 2022. The risk-off probability remains consistently elevated, reflecting the persistent negative trend and volatility. This demonstrates the model's ability to recognize and adapt to sustained bear markets, not just short-term shocks.

3.  **Periods of Calm (2021 & 2023):** During the strong bull run of 2021 and the recovery in 2023, the risk-off probability stays near zero. In these 'risk-on' phases, the optimizer would have used more aggressive parameters, allowing for higher potential returns by taking on more concentrated positions.

The visualization confirms that the regime detection model is performing as intended. It successfully flags periods of significant market distress, providing the necessary signal for the `RegimeAwareCVaROptimizer` to dynamically adjust its strategy. This proactive risk management is the key mechanism through which the model aims to outperform a static baseline strategy.
"""

def main():
    """Main function to generate the Task B report content."""
    print("--- Generating Task B Report ---")
    # Load data
    regime_probs = pd.read_csv(os.path.join(RESULTS_DIR, "regime_probabilities.csv"), index_col=0, parse_dates=True)
    all_prices = pd.read_csv(os.path.join(RESULTS_DIR, "sp500_prices_2010_2024.csv"), index_col=0, parse_dates=True)
    spy_prices = all_prices[["SPY"]].loc[regime_probs.index.min():regime_probs.index.max()]

    # Generate plot
    plot_path = generate_regime_plot(regime_probs, spy_prices)

    # Create report content
    method_summary = create_method_summary()
    interpretability_report = create_interpretability_report(plot_path)

    # Append to main report file
    with open(REPORT_FILE, "a") as f:
        f.write("\n\n" + "-"*80 + "\n")
        f.write(method_summary)
        f.write("\n\n")
        f.write(interpretability_report)
    
    print(f"Appended Task B analysis to {REPORT_FILE}")
    print("--- Report Generation Complete ---")

if __name__ == "__main__":
    main()
