import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
from pathlib import Path
from .utils import calculate_turnover, calculate_turnover_with_drift
from ..backtesting.metrics import calculate_raw_metrics
import dataframe_image as dfi

# --- Configuration & Styling ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"

# Set a professional and consistent style for all plots
sns.set_theme(style="whitegrid", palette="deep", font_scale=1.1)
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans"]


def save_metrics_df_as_image(csv_path: Path, output_path: Path):
    """Loads a metrics DataFrame from a CSV and saves it as a styled PNG image."""
    try:
        metrics_df = pd.read_csv(csv_path, index_col=0)
        # Basic styling for the table image
        styled_df = metrics_df.style.background_gradient(
            cmap="viridis", low=0.5, high=0.0
        ).set_properties(**{"font-size": "12pt", "font-family": "Arial"})

        dfi.export(styled_df, str(output_path), dpi=300)
        logging.info(f"Metrics table image successfully saved to {output_path}")
    except FileNotFoundError:
        logging.error(f"Metrics CSV not found at {csv_path}. Cannot generate table image.")
    except Exception as e:
        logging.error(f"Failed to generate metrics table image: {e}")


def plot_performance_comparison(all_returns: dict):
    """
    Generates a professional plot comparing the performance of all strategies against benchmarks.
    Includes cumulative returns and drawdowns.
    """
    logging.info("Generating comprehensive performance comparison plot...")

    # --- Data Preparation ---
    # Join the dataframes to align them for the comparison plot
    baseline_df = all_returns.get("baseline")
    if baseline_df is None:
        logging.error("Baseline returns data not found. Aborting performance plot.")
        return

    # Start with baseline columns
    returns_df = baseline_df[["Baseline_CVaR", "SPY", "Equal_Weighted"]].copy()

    # Join other strategies
    if "regime_aware" in all_returns:
        regime_df = all_returns["regime_aware"]
        regime_col = "Regime_Aware_CVaR" if "Regime_Aware_CVaR" in regime_df.columns else regime_df.columns[0]
        returns_df = returns_df.join(regime_df[[regime_col]].rename(columns={regime_col: "Regime_Aware_CVaR"}))

    if "hybrid" in all_returns:
        hybrid_df = all_returns["hybrid"]
        hybrid_col = "Hybrid_Model" if "Hybrid_Model" in hybrid_df.columns else hybrid_df.columns[0]
        returns_df = returns_df.join(hybrid_df[[hybrid_col]].rename(columns={hybrid_col: "Hybrid_Model"}))
    
    returns_df.dropna(inplace=True)

    plot_map = {
        "Baseline_CVaR": "Baseline CVaR (A)",
        "Regime_Aware_CVaR": "Regime-Aware CVaR (B)",
        "Hybrid_Model": "Hybrid Model (C)",
        "SPY": "SPY Benchmark",
        "Equal_Weighted": "Equal-Weighted Benchmark",
    }
    plot_cols = [col for col in plot_map.keys() if col in returns_df.columns]
    if not plot_cols:
        logging.error("No strategy columns found in the returns data. Aborting performance plot.")
        return

    # Create a DataFrame with readable names for plotting
    plot_df = returns_df[plot_cols].rename(columns=plot_map)
    cumulative_returns = (1 + plot_df).cumprod()

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(16, 12), sharex=True, gridspec_kw={"height_ratios": [2.5, 1]}
    )
    fig.suptitle("Strategy Performance Comparison (2010-2024)", fontsize=20, fontweight="bold")

    # 1. Cumulative Returns Plot
    cumulative_returns.plot(ax=ax1, lw=2, alpha=0.9)
    ax1.set_ylabel("Growth of $1 (Log Scale)", fontsize=12)
    ax1.set_yscale("log")
    ax1.set_title("Cumulative Returns (Logarithmic Scale)", fontsize=14)
    ax1.legend(title="Strategies", fontsize=10)
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

    # 2. Drawdown Plot
    for col in cumulative_returns.columns:
        running_max = cumulative_returns[col].expanding().max()
        drawdown = (cumulative_returns[col] - running_max) / running_max
        ax2.plot(drawdown.index, drawdown, label=col, lw=1.5, alpha=0.8)

    ax2.set_ylabel("Drawdown", fontsize=12)
    ax2.set_title("Strategy Drawdowns", fontsize=14)
    if ax2.get_lines():  # Avoid error if no data is plotted
        ax2.fill_between(
            ax2.get_lines()[0].get_xdata(), ax2.get_lines()[0].get_ydata(), 0, alpha=0.1
        )
    ax2.legend(fontsize=10)
    ax2.grid(True, which="both", linestyle="--", linewidth=0.5)

    plt.xlabel("Date", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    # Save plot directly to the results directory as requested
    save_path = RESULTS_DIR / "baseline_performance_comparison.png"
    plt.savefig(save_path)
    plt.close()
    logging.info(f"Saved performance comparison plot to {save_path}")


def plot_task_a_comparison(all_returns: dict, daily_weights: pd.DataFrame = None):
    """
    Generates a plot for Task A, comparing the Baseline CVaR strategy against benchmarks,
    and includes a performance metrics table.
    """
    logging.info("Generating Task A performance comparison plot...")

    returns_df = all_returns.get("baseline")
    if returns_df is None:
        logging.warning("Baseline returns data not found. Skipping Task A plot.")
        return

    # --- Data Preparation ---
    plot_map = {
        "Baseline_CVaR": "Baseline CVaR (A)",
        "SPY": "SPY Benchmark",
        "Equal_Weighted": "Equal-Weighted Benchmark",
    }
    plot_cols = [col for col in plot_map.keys() if col in returns_df.columns]
    if not plot_cols:
        logging.error("No Task A columns found in the returns data. Aborting plot.")
        return

    plot_df = returns_df[plot_cols].rename(columns=plot_map)

    # --- Load Data & Calculate Metrics ---
    # Load baseline CVaR weights for its turnover calculation
    baseline_weights_path = RESULTS_DIR / "baseline_daily_weights.csv"
    if baseline_weights_path.exists():
        baseline_daily_weights = pd.read_csv(baseline_weights_path, index_col=0, parse_dates=True)
    else:
        logging.warning(f"File not found: {baseline_weights_path}. Baseline turnover will be 0.")
        baseline_daily_weights = pd.DataFrame()

    # Load Equal-Weighted benchmark returns
    ew_returns_path = RESULTS_DIR / "equal_weighted_daily_returns.csv"
    if ew_returns_path.exists():
        ew_returns = pd.read_csv(ew_returns_path, index_col=0, parse_dates=True).squeeze("columns")
        plot_df["Equal-Weighted Benchmark"] = ew_returns.reindex(plot_df.index).fillna(0)
    else:
        logging.warning("Equal-Weighted benchmark returns not found. Skipping.")

    # --- Metrics Calculation ---
    raw_metrics_data = {}
    benchmark_returns = plot_df["SPY Benchmark"]

    # 1. Baseline CVaR Metrics
    baseline_turnover = calculate_turnover(baseline_daily_weights)
    baseline_metrics = calculate_raw_metrics(plot_df["Baseline CVaR (A)"], benchmark_returns)
    raw_metrics_data["Baseline CVaR (A)"] = {**baseline_metrics, "Annual Turnover": baseline_turnover}

    # 2. SPY Benchmark Metrics
    spy_metrics = calculate_raw_metrics(plot_df["SPY Benchmark"], benchmark_returns)
    raw_metrics_data["SPY Benchmark"] = {**spy_metrics, "Annual Turnover": 0.0}

    # 3. Equal-Weighted Benchmark Metrics
    ew_turnover_numeric = np.nan
    try:
        ew_weights_path = RESULTS_DIR / "equal_weighted_daily_weights.csv"
        ew_target_weights = pd.read_csv(ew_weights_path, index_col=0, parse_dates=True)
        price_path = RESULTS_DIR / "sp500_prices_2010_2024.csv"
        prices = pd.read_csv(price_path, index_col=0, parse_dates=True)
        asset_returns = prices.pct_change()
        ew_turnover_numeric = calculate_turnover_with_drift(ew_target_weights, asset_returns)
        logging.info(f"Calculated drift-adjusted turnover for EW: {ew_turnover_numeric:.2%}")
    except FileNotFoundError as e:
        logging.warning(f"Could not calculate EW turnover due to missing file: {e}")

    if "Equal-Weighted Benchmark" in plot_df:
        ew_metrics = calculate_raw_metrics(plot_df["Equal-Weighted Benchmark"], benchmark_returns)
        raw_metrics_data["Equal-Weighted Benchmark"] = {**ew_metrics, "Annual Turnover": ew_turnover_numeric}

    # --- Format Metrics for Display ---
    formatted_metrics = {}
    for name, metrics in raw_metrics_data.items():
        turnover = metrics.get('Annual Turnover', np.nan)
        turnover_str = f"{turnover:.2%}" if pd.notna(turnover) else "N/A"

        formatted_metrics[name] = {
            "Annual Return": f"{metrics['Annual Return']:.2%}",
            "Annual Volatility": f"{metrics['Annual Volatility']:.2%}",
            "Sharpe Ratio": f"{metrics['Sharpe Ratio']:.2f}",
            "Max Drawdown": f"{metrics['Max Drawdown']:.2%}",
            "95% CVaR": f"{metrics['95% CVaR']:.2%}",
            "Turnover": turnover_str,
        }
    metrics_df = pd.DataFrame(formatted_metrics).T

    # --- Plotting ---
    cumulative_returns = (1 + plot_df).cumprod()
    fig, (ax1, ax2, ax3) = plt.subplots(
        3, 1, figsize=(16, 15), sharex=True, gridspec_kw={"height_ratios": [2.5, 1, 0.8]}
    )
    fig.suptitle("Task A: Baseline CVaR vs. Benchmarks (2010-2024)", fontsize=20, fontweight="bold")

    # 1. Cumulative Returns Plot
    cumulative_returns.plot(ax=ax1, lw=2, alpha=0.9)
    ax1.set_ylabel("Growth of $1 (Log Scale)", fontsize=12)
    ax1.set_yscale("log")
    ax1.set_title("Cumulative Returns (Logarithmic Scale)", fontsize=14)
    ax1.legend(title="Strategies", fontsize=10)
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

    # 2. Drawdown Plot
    for col in cumulative_returns.columns:
        running_max = cumulative_returns[col].expanding().max()
        drawdown = (cumulative_returns[col] - running_max) / running_max
        ax2.plot(drawdown.index, drawdown, label=col, lw=1.5, alpha=0.8)

    ax2.set_ylabel("Drawdown", fontsize=12)
    ax2.set_title("Strategy Drawdowns", fontsize=14)
    if ax2.get_lines():
        ax2.fill_between(
            ax2.get_lines()[0].get_xdata(), ax2.get_lines()[0].get_ydata(), 0, alpha=0.1
        )
    ax2.legend(fontsize=10)
    ax2.grid(True, which="both", linestyle="--", linewidth=0.5)

    # 3. Metrics Table
    ax3.axis("off")
    ax3.set_title("Performance Metrics", fontsize=14, y=0.8)
    table = ax3.table(
        cellText=metrics_df.values,
        rowLabels=metrics_df.index,
        colLabels=metrics_df.columns,
        cellLoc="center",
        rowLoc="left",
        loc="center",
        colWidths=[0.15] * len(metrics_df.columns),
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.1, 1.4)

    # Style table to be black and white
    for key, cell in table.get_celld().items():
        cell.set_edgecolor("black")
        cell.set_linewidth(0.5)
        if key[0] == 0 or key[1] == -1:
            cell.set_text_props(weight="bold")

    plt.xlabel("Date", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_path = RESULTS_DIR / "task_a_performance_comparison.png"
    plt.savefig(save_path)
    plt.close()
    logging.info(f"Saved Task A performance comparison plot to {save_path}")


def plot_regime_analysis(returns_df: pd.DataFrame, price_df: pd.DataFrame):
    """
    Generates a professional plot showing the Regime-Aware strategy against market regimes.
    """
    logging.info("Generating regime analysis plot...")

    # --- Data Preparation ---
    # Generate regime signals
    price_df["SMA50"] = price_df["SPY"].rolling(window=50).mean()
    price_df["SMA200"] = price_df["SPY"].rolling(window=200).mean()
    price_df.dropna(inplace=True)
    price_df["regime"] = np.where(
        price_df["SMA50"] > price_df["SMA200"], 1, 0
    )  # 1 for Risk-On, 0 for Risk-Off
    regime_df = price_df[["regime"]]

    # Align data to the start of the regime signals
    start_date = regime_df.index.min()
    aligned_prices = price_df.loc[start_date:]
    aligned_returns = returns_df.loc[start_date:]

    # --- Plotting ---
    fig, ax1 = plt.subplots(figsize=(16, 8))
    fig.suptitle(
        "Regime-Aware Strategy Performance vs. Market Regimes", fontsize=18, fontweight="bold"
    )

    # Plot SPY price as the market indicator
    ax1.plot(
        aligned_prices.index,
        aligned_prices["SPY"],
        color="black",
        lw=1.5,
        label="SPY Price (Log Scale)",
        alpha=0.8,
    )
    ax1.set_ylabel("SPY Price (Log Scale)", fontsize=12)
    ax1.set_yscale("log")
    ax1.grid(False)  # Turn off grid for the price plot for clarity

    # Shade background based on regime
    ax1.fill_between(
        regime_df.index,
        ax1.get_ylim()[0],
        ax1.get_ylim()[1],
        where=regime_df["regime"] == 1,
        facecolor="green",
        alpha=0.15,
        label="Risk-On Regime (SMA50 > SMA200)",
    )
    ax1.fill_between(
        regime_df.index,
        ax1.get_ylim()[0],
        ax1.get_ylim()[1],
        where=regime_df["regime"] == 0,
        facecolor="red",
        alpha=0.15,
        label="Risk-Off Regime (SMA50 < SMA200)",
    )

    # Plot cumulative returns of the regime-aware strategy on a secondary axis
    ax2 = ax1.twinx()
    cum_returns = (1 + aligned_returns["regime_aware_cvar_index"]).cumprod()
    ax2.plot(
        cum_returns.index,
        cum_returns,
        color="royalblue",
        lw=2.5,
        label="Regime-Aware Strategy Returns",
    )
    ax2.set_ylabel("Cumulative Returns", fontsize=12)
    ax2.grid(True, which="major", linestyle="--", linewidth=0.5, axis="y")

    # Combine legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc="upper left", fontsize=10)

    plt.xlabel("Date", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_path = RESULTS_DIR / "regime_analysis_plot.png"
    plt.savefig(save_path)
    plt.close()
    logging.info(f"Saved regime analysis plot to {save_path}")


def generate_metrics_table(returns_df: pd.DataFrame):
    """
    Calculates performance metrics for all strategies in the returns dataframe,
    formats them into a professional table, and saves it as a high-quality PNG image.
    """
    logging.info("Generating final performance metrics table...")

    all_metrics = {}
    benchmark_returns = (
        returns_df["SPY"] if "SPY" in returns_df.columns else pd.Series(0, index=returns_df.index)
    )

    # Calculate metrics for each strategy/benchmark in the dataframe
    for col_name in returns_df.columns:
        portfolio_returns = returns_df[col_name]
        aligned_benchmark = benchmark_returns.reindex(portfolio_returns.index).ffill()
        raw_metrics = calculate_raw_metrics(portfolio_returns, aligned_benchmark)
        all_metrics[col_name] = raw_metrics

    if not all_metrics:
        logging.error("No metrics were calculated. Aborting table generation.")
        return

    metrics_df = pd.DataFrame(all_metrics).T

    # Rename index for better display
    metrics_df.rename(
        index={
            "Baseline_CVaR": "Baseline CVaR",
            "SPY": "SPY Benchmark",
            "Equal_Weighted": "Equal-Weighted",
            "Cap_Weighted": "Cap-Weighted",
        },
        inplace=True,
    )

    # Select and rename columns for the final table
    display_cols = {
        "Cumulative Returns": "Cumulative Return (%)",
        "Annual Return": "Annualized Return (%)",
        "Annual Volatility": "Annual Volatility (%)",
        "Sharpe Ratio": "Sharpe Ratio",
        "Max Drawdown": "Max Drawdown (%)",
        "Calmar Ratio": "Calmar Ratio",
        "Sortino Ratio": "Sortino Ratio",
    }
    available_cols = {k: v for k, v in display_cols.items() if k in metrics_df.columns}
    metrics_df = metrics_df[list(available_cols.keys())].rename(columns=available_cols)

    # Convert ratio columns to percentages
    for col in [
        "Cumulative Return (%)",
        "Annualized Return (%)",
        "Annual Volatility (%)",
        "Max Drawdown (%)",
    ]:
        if col in metrics_df.columns:
            metrics_df[col] = metrics_df[col] * 100

    # Format the table for better readability
    styled_df = (
        metrics_df.style.format("{:.2f}", na_rep="-")
        .set_caption("Consolidated Performance Metrics (2010-2024)")
        .set_table_styles(
            [
                {
                    "selector": "caption",
                    "props": [
                        ("font-size", "18px"),
                        ("font-weight", "bold"),
                        ("margin-bottom", "10px"),
                    ],
                },
                {
                    "selector": "th",
                    "props": [
                        ("font-size", "12px"),
                        ("text-align", "center"),
                        ("font-weight", "bold"),
                    ],
                },
                {"selector": "td", "props": [("text-align", "center"), ("font-size", "12px")]},
            ]
        )
        .background_gradient(
            cmap="Greens",
            subset=[
                "Cumulative Return (%)",
                "Annualized Return (%)",
                "Sharpe Ratio",
                "Sortino Ratio",
                "Calmar Ratio",
            ],
        )
        .background_gradient(cmap="Reds_r", subset=["Annual Volatility (%)", "Max Drawdown (%)"])
        .highlight_max(
            color="#90EE90",
            axis=0,
            subset=[
                "Cumulative Return (%)",
                "Annualized Return (%)",
                "Sharpe Ratio",
                "Sortino Ratio",
                "Calmar Ratio",
            ],
        )
        .highlight_min(
            color="#FDBAAB", axis=0, subset=["Annual Volatility (%)", "Max Drawdown (%)"]
        )
        .set_properties(**{"border": "1px solid black"})
    )

    # Save styled table as an image
    table_path = RESULTS_DIR / "consolidated_metrics_table.png"
    try:
        dfi.export(styled_df, str(table_path))
        logging.info(f"Saved styled metrics table to {table_path}")
    except Exception as e:
        logging.error(f"Failed to save metrics table as image: {e}")

    # Save raw data to CSV for reference
    metrics_df.to_csv(RESULTS_DIR / "consolidated_performance_metrics.csv")


def main():
    """Main function to generate all professional report visuals."""
    logging.info("--- Starting Professional Report Visual Generation ---")

    # Load data
    try:
        # Load baseline returns, which now include new benchmarks
        returns_df = pd.read_csv(
            RESULTS_DIR / "baseline_daily_returns.csv", index_col=0, parse_dates=True
        )

        # Use a more recent price file if available, otherwise fallback
        price_file = RESULTS_DIR / "sp500_prices_2010_2024.csv"
        if not price_file.exists():
            price_file = RESULTS_DIR / "sp500_prices.csv"  # Fallback
        price_df = pd.read_csv(price_file, index_col=0, parse_dates=True)
    except FileNotFoundError as e:
        logging.error(f"Could not load a required data file: {e}. Aborting visual generation.")
        return

    # Generate and save all visuals and tables
    plot_performance_comparison(returns_df)
    generate_metrics_table(returns_df)  # Pass the dataframe

    # The following plot may fail if its required columns are not in the baseline file.
    try:
        plot_regime_analysis(returns_df, price_df)
    except Exception as e:
        logging.warning(f"Skipping regime analysis plot, likely due to missing columns. Error: {e}")

    logging.info("--- Professional Report Visual Generation Complete ---")
    logging.info(f"All visuals and tables saved to: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
