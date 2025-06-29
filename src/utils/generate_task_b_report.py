# src/utils/generate_task_b_report.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.backtesting.metrics import calculate_raw_metrics

# --- Configuration ---
RESULTS_DIR = "results"
DOCS_DIR = "docs"


def generate_task_b_report():
    """Generates a comprehensive report for Task B, including a plot with an embedded metrics table."""
    print("--- Generating Task B Interpretability Report ---")

    # --- Load Data ---
    try:
        # Load original metrics to get turnover later
        baseline_metrics = pd.read_csv(os.path.join(RESULTS_DIR, "task_a_baseline_cvar_performance_metrics.csv"), index_col=0).squeeze()
        regime_metrics = pd.read_csv(os.path.join(RESULTS_DIR, "task_b_regime_aware_cvar_performance.csv"), index_col=0).squeeze()

        # Load return series
        baseline_returns_full = pd.read_csv(os.path.join(RESULTS_DIR, "task_a_baseline_daily_returns.csv"), index_col=0, parse_dates=True).squeeze()
        baseline_returns = baseline_returns_full.loc["2020-01-01":].rename("Baseline_CVaR")
        regime_returns = pd.read_csv(os.path.join(RESULTS_DIR, "task_b_regime_aware_daily_returns.csv"), index_col=0, parse_dates=True).squeeze()
        SPY_RETURNS_PATH = os.path.join(RESULTS_DIR, "spy_daily_returns_2020-2024.csv")
        benchmark_returns = pd.read_csv(SPY_RETURNS_PATH, index_col=0, parse_dates=True).squeeze().loc["2020-01-01":].rename("SPY")
    except FileNotFoundError as e:
        print(f"Error: Could not find a required data file. {e}")
        print("Please ensure all backtests have run successfully with the latest changes.")
        return

    # --- 1. Align Dates for Fair Comparison ---
    print("Aligning all return series for fair comparison...")
    # Combine into a single DataFrame to align automatically, dropping any non-common dates
    combined_returns = pd.DataFrame({
        'baseline': baseline_returns,
        'regime': regime_returns,
        'benchmark': benchmark_returns
    }).dropna()

    baseline_returns = combined_returns['baseline']
    regime_returns = combined_returns['regime']
    benchmark_returns = combined_returns['benchmark']

    print(f"All series aligned. Common date range: {combined_returns.index.min().date()} to {combined_returns.index.max().date()}")

    # --- 2. Recalculate Metrics on Aligned Data ---
    print("Recalculating performance metrics on aligned data for fair comparison...")
    spy_metrics = calculate_raw_metrics(benchmark_returns, benchmark_returns)  # Benchmark is its own benchmark
    baseline_metrics_aligned = calculate_raw_metrics(baseline_returns, benchmark_returns)
    regime_metrics_aligned = calculate_raw_metrics(regime_returns, benchmark_returns)

    metrics_to_display = ["Annual Return", "Annual Volatility", "Sharpe Ratio", "Max Drawdown", "95% CVaR", "Alpha", "Beta"]
    
    summary_df = pd.DataFrame({
        "SPY Benchmark": spy_metrics,
        "Baseline CVaR": baseline_metrics_aligned,
        "Regime-Aware CVaR": regime_metrics_aligned
    }).loc[metrics_to_display]

    # Add turnover from original files as it can't be recalculated from returns alone
    summary_df.loc["Annual Turnover"] = [
        0.0,  # SPY turnover is 0 by definition
        baseline_metrics.get("Annual Turnover", 0.0),
        regime_metrics.get("Annual Turnover", 0.0)
    ]

    # --- 3. Generate Cumulative Performance Plot with Table ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # Plot cumulative returns
    baseline_cum = (1 + baseline_returns).cumprod()
    regime_cum = (1 + regime_returns).cumprod()
    benchmark_cum = (1 + benchmark_returns).cumprod()

    ax1.plot(regime_cum.index, regime_cum, label="Regime-Aware CVaR", color="blue", linestyle="-")
    ax1.plot(baseline_cum.index, baseline_cum, label="Baseline CVaR", color="black", linestyle="-", alpha=0.8)
    ax1.plot(benchmark_cum.index, benchmark_cum, label="SPY Benchmark", color="green", linestyle="--")
    ax1.set_title("Cumulative Performance Comparison (2020-2024)", fontsize=16)
    ax1.set_ylabel("Cumulative Returns")
    ax1.legend()
    ax1.grid(True)

    # Add metrics table
    ax2.axis('off')
    table = ax2.table(cellText=summary_df.round(4).values, colLabels=summary_df.columns, rowLabels=summary_df.index, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.tight_layout(pad=3.0)
    plot_path = os.path.join(RESULTS_DIR, "task_b_performance_comparison.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved performance comparison plot with metrics table to {plot_path}")

    # --- 4. Generate Feature Importance Plot ---
    feature_importance = pd.Series({'SMA Trend Signal': 0.7, 'Volatility Signal': 0.3}, name="Feature Importance")
    feature_importance = feature_importance.sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importance.values, y=feature_importance.index, palette="viridis")
    plt.title('Static Feature Importance in Ensemble Regime Detector')
    plt.xlabel('Assigned Weight')
    plt.ylabel('Feature')
    plt.xlim(0, 1)

    importance_plot_path = os.path.join(RESULTS_DIR, "task_b_regime_feature_importance.png")
    plt.savefig(importance_plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved feature importance plot to {importance_plot_path}")

    # --- 5. Update Main Report File ---
    md_table = summary_df.to_markdown(floatfmt=".4f")
    report_content = f"""### Task B: Regime-Aware Enhancement

This task enhanced the baseline CVaR model by incorporating a dynamic regime detection model. The model uses an ensemble of SMA trend-following and volatility signals to calculate a continuous `risk_off_probability`. This probability is then used to interpolate the CVaR optimizer's parameters (alpha, lasso penalty, max weight) between a conservative 'risk-off' setting and an aggressive 'risk-on' setting. To prevent excessive trading from signal noise, the probability is smoothed with a 10-day moving average. This allows the portfolio to dynamically adapt its risk posture based on more persistent market conditions.

#### Performance Analysis

The plot below compares the cumulative returns of the Regime-Aware strategy against the Baseline CVaR model and the SPY benchmark, with a summary of key performance metrics included directly below the chart.

![Performance Comparison](results/task_b_performance_comparison.png)

#### Regime Model Interpretability

The regime detection model is a simple, interpretable ensemble. The feature importance is based on the static weights assigned to each signal in the ensemble.

![Feature Importance](results/task_b_regime_feature_importance.png)

"""

    report_file_path = os.path.join(DOCS_DIR, "report.md")
    try:
        with open(report_file_path, "r", encoding='utf-8') as f:
            full_report = f.read()
    except FileNotFoundError:
        print(f"Warning: {report_file_path} not found. Will create it.")
        full_report = ""

    start_marker = "### Task B: Regime-Aware Enhancement"
    end_marker = "### Task C:"

    start_index = full_report.find(start_marker)
    end_index = full_report.find(end_marker)

    if start_index != -1 and end_index != -1:
        new_report = full_report[:start_index] + report_content + full_report[end_index:]
        with open(report_file_path, "w", encoding='utf-8') as f:
            f.write(new_report)
        print(f"Updated Task B section in {report_file_path}")
    else:
        print("Could not find Task B markers in report.md. Appending content.")
        with open(report_file_path, "a", encoding='utf-8') as f:
            f.write("\n" + report_content)

    print("--- Task B Report Generation Complete ---")


if __name__ == "__main__":
    generate_task_b_report()


