import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
from pathlib import Path
import dataframe_image as dfi

# --- Configuration & Styling ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
RESULTS_DIR = Path(__file__).resolve().parents[2] / 'results'
IMG_DIR = RESULTS_DIR / 'img'
IMG_DIR.mkdir(exist_ok=True) # Create img subdirectory if it doesn't exist

# Set a professional and consistent style for all plots
sns.set_theme(style="whitegrid", palette="deep", font_scale=1.1)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']


def plot_performance_comparison(returns_df: pd.DataFrame):
    """
    Generates a professional plot comparing the performance of all strategies against benchmarks.
    Includes cumulative returns and drawdowns.
    """
    logging.info("Generating comprehensive performance comparison plot...")

    # --- Data Preparation ---
    # Define columns and their desired legend names
    plot_map = {
        'baseline_cvar_index': 'Baseline CVaR',
        'regime_aware_cvar_index': 'Regime-Aware CVaR',
        'alpha_aware_cvar_index': 'Alpha-Aware CVaR',
        'SPY Benchmark': 'SPY Benchmark',
        'Equal-Weighted Benchmark': 'Equal-Weighted Benchmark'
    }
    plot_cols = [col for col in plot_map.keys() if col in returns_df.columns]
    if not plot_cols:
        logging.error("No strategy columns found in the returns data. Aborting performance plot.")
        return

    # Create a DataFrame with readable names for plotting
    plot_df = returns_df[plot_cols].rename(columns=plot_map)
    cum_returns = (1 + plot_df).cumprod()

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(16, 12), sharex=True, gridspec_kw={'height_ratios': [2.5, 1]}
    )
    fig.suptitle('Comprehensive Strategy Performance Comparison (2020-2024)', fontsize=20, fontweight='bold')

    # 1. Cumulative Returns Plot
    cum_returns.plot(ax=ax1, lw=2, alpha=0.9)
    ax1.set_ylabel('Growth of $1 (Log Scale)', fontsize=12)
    ax1.set_yscale('log')
    ax1.set_title('Cumulative Returns (Logarithmic Scale)', fontsize=14)
    ax1.legend(title='Strategies', fontsize=10)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # 2. Drawdown Plot
    for col in cum_returns.columns:
        running_max = cum_returns[col].expanding().max()
        drawdown = (cum_returns[col] - running_max) / running_max
        ax2.plot(drawdown.index, drawdown, label=col, lw=1.5, alpha=0.8)

    ax2.set_ylabel('Drawdown', fontsize=12)
    ax2.set_title('Strategy Drawdowns', fontsize=14)
    ax2.fill_between(ax2.get_lines()[0].get_xdata(), ax2.get_lines()[0].get_ydata(), 0, alpha=0.1)
    ax2.legend(fontsize=10)
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.xlabel("Date", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_path = IMG_DIR / 'performance_comparison.png'
    plt.savefig(save_path)
    plt.close()
    logging.info(f"Saved performance comparison plot to {save_path}")


def plot_regime_analysis(returns_df: pd.DataFrame, price_df: pd.DataFrame):
    """
    Generates a professional plot showing the Regime-Aware strategy against market regimes.
    """
    logging.info("Generating regime analysis plot...")

    # --- Data Preparation ---
    # Generate regime signals
    price_df['SMA50'] = price_df['SPY'].rolling(window=50).mean()
    price_df['SMA200'] = price_df['SPY'].rolling(window=200).mean()
    price_df.dropna(inplace=True)
    price_df['regime'] = np.where(price_df['SMA50'] > price_df['SMA200'], 1, 0) # 1 for Risk-On, 0 for Risk-Off
    regime_df = price_df[['regime']]

    # Align data to the start of the regime signals
    start_date = regime_df.index.min()
    aligned_prices = price_df.loc[start_date:]
    aligned_returns = returns_df.loc[start_date:]
    
    # --- Plotting ---
    fig, ax1 = plt.subplots(figsize=(16, 8))
    fig.suptitle('Regime-Aware Strategy Performance vs. Market Regimes', fontsize=18, fontweight='bold')

    # Plot SPY price as the market indicator
    ax1.plot(aligned_prices.index, aligned_prices['SPY'], color='black', lw=1.5, label='SPY Price (Log Scale)', alpha=0.8)
    ax1.set_ylabel('SPY Price (Log Scale)', fontsize=12)
    ax1.set_yscale('log')
    ax1.grid(False) # Turn off grid for the price plot for clarity

    # Shade background based on regime
    ax1.fill_between(regime_df.index, ax1.get_ylim()[0], ax1.get_ylim()[1],
                     where=regime_df['regime'] == 1, facecolor='green', alpha=0.15, label='Risk-On Regime (SMA50 > SMA200)')
    ax1.fill_between(regime_df.index, ax1.get_ylim()[0], ax1.get_ylim()[1],
                     where=regime_df['regime'] == 0, facecolor='red', alpha=0.15, label='Risk-Off Regime (SMA50 < SMA200)')

    # Plot cumulative returns of the regime-aware strategy on a secondary axis
    ax2 = ax1.twinx()
    cum_returns = (1 + aligned_returns['regime_aware_cvar_index']).cumprod()
    ax2.plot(cum_returns.index, cum_returns, color='royalblue', lw=2.5, label='Regime-Aware Strategy Returns')
    ax2.set_ylabel('Cumulative Returns', fontsize=12)
    ax2.grid(True, which='major', linestyle='--', linewidth=0.5, axis='y')

    # Combine legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=10)

    plt.xlabel("Date", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    save_path = IMG_DIR / 'regime_analysis_plot.png'
    plt.savefig(save_path)
    plt.close()
    logging.info(f"Saved regime analysis plot to {save_path}")


def generate_metrics_table():
    """
    Loads pre-calculated metrics for all strategies, formats them into a professional
    table, and saves it as a high-quality PNG image.
    """
    logging.info("Generating final performance metrics table...")
    
    metric_files = {
        'Baseline CVaR': 'baseline_cvar_performance_metrics.csv',
        'Regime-Aware CVaR': 'enhanced_cvar_performance_metrics.csv',
        'Alpha-Aware CVaR': 'alpha_aware_cvar_performance.csv' # Note: filename from script is different
    }
    
    all_metrics = {}
    for name, filename in metric_files.items():
        try:
            filepath = RESULTS_DIR / filename
            # Read the first column of metrics, assuming it's the value we want
            metric_series = pd.read_csv(filepath, index_col=0).iloc[:, 0]
            metric_series.name = name
            all_metrics[name] = metric_series
        except FileNotFoundError:
            logging.warning(f"Metric file not found: {filename}. Skipping.")
        except Exception as e:
            logging.error(f"Could not process {filename}: {e}")

    if not all_metrics:
        logging.error("No metrics were loaded. Aborting table generation.")
        return

    metrics_df = pd.DataFrame(all_metrics).T # Transpose to have strategies as rows
    
    # Select and rename columns for the final table
    display_cols = {
        'Cumulative Returns': 'Cumulative Return',
        'Annual Return': 'Annualized Return (%)',
        'Annual Volatility': 'Annual Volatility (%)',
        'Sharpe Ratio': 'Sharpe Ratio',
        'Max Drawdown': 'Max Drawdown (%)',
        'Calmar Ratio': 'Calmar Ratio',
        'Sortino Ratio': 'Sortino Ratio',
    }
    metrics_df = metrics_df[display_cols.keys()].rename(columns=display_cols)
    
    # Convert percentage columns
    for col in ['Annualized Return (%)', 'Annual Volatility (%)', 'Max Drawdown (%)', 'Cumulative Return']:
        if col in metrics_df.columns:
            metrics_df[col] = metrics_df[col] * 100

    # Format the table for better readability
    styled_df = metrics_df.style \
        .format('{:.2f}', na_rep='-') \
        .set_caption("Consolidated Performance Metrics (2020-2024)") \
        .set_table_styles([
            {'selector': 'caption', 'props': [('font-size', '18px'), ('font-weight', 'bold'), ('margin-bottom', '10px')]},
            {'selector': 'th', 'props': [('font-size', '12px'), ('text-align', 'center'), ('font-weight', 'bold')]},
            {'selector': 'td', 'props': [('text-align', 'center'), ('font-size', '12px')]},
        ]) \
        .background_gradient(cmap='Greens', subset=['Annualized Return (%)', 'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio']) \
        .background_gradient(cmap='Reds_r', subset=['Annual Volatility (%)', 'Max Drawdown (%)']) \
        .highlight_max(color='#90EE90', axis=0) \
        .set_properties(**{'border': '1px solid black'})

    # Save styled table as an image
    table_path = IMG_DIR / 'consolidated_metrics_table.png'
    try:
        dfi.export(styled_df, str(table_path))
        logging.info(f"Saved styled metrics table to {table_path}")
    except Exception as e:
        logging.error(f"Failed to save metrics table as image: {e}. Ensure `pip install dataframe-image` and a web browser like Chrome is available for the headless export.")

    # Save raw data to CSV for reference
    metrics_df.to_csv(RESULTS_DIR / 'consolidated_performance_metrics.csv')


def main():
    """Main function to generate all professional report visuals."""
    logging.info("--- Starting Professional Report Visual Generation ---")
    
    # Load data
    try:
        returns_df = pd.read_csv(RESULTS_DIR / 'daily_returns.csv', index_col=0, parse_dates=True)
        # Use a more recent price file if available, otherwise fallback
        price_file = RESULTS_DIR / 'sp500_prices_2010_2024.csv'
        if not price_file.exists():
             price_file = RESULTS_DIR / 'sp500_prices.csv' # Fallback
        price_df = pd.read_csv(price_file, index_col=0, parse_dates=True)
    except FileNotFoundError as e:
        logging.error(f"Could not load a required data file: {e}. Aborting visual generation.")
        return

    # Generate and save all visuals and tables
    plot_performance_comparison(returns_df)
    plot_regime_analysis(returns_df, price_df)
    generate_metrics_table()
    
    logging.info("--- Professional Report Visual Generation Complete ---")
    logging.info(f"All visuals and tables saved to: {IMG_DIR}")

if __name__ == '__main__':
    main()
