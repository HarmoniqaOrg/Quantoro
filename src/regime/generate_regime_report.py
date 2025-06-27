import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import logging
from regime import RegimeDetector

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_regime_plot(prices: pd.DataFrame, results_dir: str):
    """
    Generates and saves a plot visualizing the market regimes.

    Args:
        prices (pd.DataFrame): DataFrame with a 'close' column for prices.
        results_dir (str): The directory to save the plot to.
    """
    logging.info("Initializing Regime Detector...")
    detector = RegimeDetector(lookback_short=50, lookback_long=200)
    
    # Use a proxy for market, like SPY if available, otherwise mean of all prices
    if 'SPY' in prices.columns:
        market_prices = prices['SPY']
    else:
        logging.warning("'SPY' not in columns, using mean of all asset prices as market proxy.")
        market_prices = prices.mean(axis=1)

    market_prices.index = pd.to_datetime(market_prices.index)

    logging.info("Detecting regimes...")
    regimes = detector.detect_regime(market_prices)
    sma_short = market_prices.rolling(window=detector.lookback_short).mean()
    sma_long = market_prices.rolling(window=detector.lookback_long).mean()

    # Save the regime timeseries for the dashboard
    regime_output_path = os.path.join(results_dir, 'regime_ts.csv')
    regimes.to_csv(regime_output_path, header=True)
    logging.info(f"Regime timeseries saved to {regime_output_path}")

    logging.info("Generating plot...")
    fig, ax = plt.subplots(figsize=(15, 8))

    # Plot prices and SMAs
    ax.plot(market_prices.index, market_prices, label='Market Proxy (SPY)', color='black', alpha=0.7)
    ax.plot(sma_short.index, sma_short, label=f'SMA-{detector.lookback_short}', color='blue', linestyle='--')
    ax.plot(sma_long.index, sma_long, label=f'SMA-{detector.lookback_long}', color='red', linestyle='--')

    # Shade the background based on the regime
    start_date = regimes.index.min()
    end_date = regimes.index.max()

    ax.fill_between(regimes.index, ax.get_ylim()[0], ax.get_ylim()[1],
                    where=(regimes == 1), color='green', alpha=0.2, label='Risk-On')
    ax.fill_between(regimes.index, ax.get_ylim()[0], ax.get_ylim()[1],
                    where=(regimes == 0), color='red', alpha=0.2, label='Risk-Off')

    # Formatting
    ax.set_title('Market Regime Detection (SMA Crossover)', fontsize=16)
    ax.set_ylabel('Price')
    ax.set_xlabel('Date')
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.autofmt_xdate()
    plt.tight_layout()

    # Save the plot
    plot_path = os.path.join(results_dir, 'regime_detection_interpretability.png')
    plt.savefig(plot_path, dpi=300)
    logging.info(f"Interpretability plot saved to {plot_path}")
    plt.close()

def main():
    """Main function to run the report generation."""
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(base_dir, 'results', 'sp500_prices_2010_2024.csv')
    results_dir = os.path.join(base_dir, 'results')

    if not os.path.exists(data_path):
        logging.error(f"Data file not found at {data_path}. Please run a backtest first to generate it.")
        return

    # Load data
    logging.info(f"Loading data from {data_path}...")
    prices_df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    
    # Filter for the relevant period for the ML enhancement backtest
    prices_df = prices_df.loc['2010-01-01':'2024-01-01']

    # Generate and save the plot
    generate_regime_plot(prices_df, results_dir)

if __name__ == "__main__":
    main()
