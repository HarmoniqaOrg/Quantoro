import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def plot_performance_comparison(returns_csv_path: Path, output_path: Path):
    """
    Reads daily returns and plots the cumulative performance of different strategies.

    Args:
        returns_csv_path (Path): The path to the CSV file containing daily returns.
        output_path (Path): The path to save the generated plot image.
    """
    try:
        logging.info(f"Reading daily returns from {returns_csv_path}...")
        returns_df = pd.read_csv(returns_csv_path, index_col=0, parse_dates=True)
        
        logging.info("Calculating cumulative returns...")
        # Calculate cumulative returns (compounded)
        cumulative_returns = (1 + returns_df).cumprod()

        # --- Plotting ---
        logging.info("Generating plot...")
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(14, 8))

        # Plot each strategy
        for column in cumulative_returns.columns:
            ax.plot(cumulative_returns.index, cumulative_returns[column], label=column)

        # Formatting the plot
        ax.set_title('Strategy Performance Comparison (2010-2024)', fontsize=18, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Cumulative Growth of $1', fontsize=12)
        ax.set_yscale('log') # Use log scale for better visualization of long-term growth
        
        # Format y-axis for log scale
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'${y:,.2f}'))
        
        ax.legend(fontsize=12)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the figure
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        logging.info(f"Successfully saved performance plot to {output_path}")

    except FileNotFoundError:
        logging.error(f"Error: The file was not found at {returns_csv_path}")
    except Exception as e:
        logging.error(f"An error occurred during plotting: {e}")

if __name__ == "__main__":
    # Define project root and paths
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    RETURNS_FILE = PROJECT_ROOT / 'results' / 'daily_returns.csv'
    OUTPUT_PLOT_FILE = PROJECT_ROOT / 'results' / 'performance_comparison.png'
    
    # Create results directory if it doesn't exist
    OUTPUT_PLOT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Generate the plot
    plot_performance_comparison(RETURNS_FILE, OUTPUT_PLOT_FILE)
