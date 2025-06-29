import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from src.regime.ensemble_regime import EnsembleRegimeDetector  # noqa: E402

RESULTS_DIR = "results"
PRICE_DATA_PATH = os.path.join(RESULTS_DIR, "sp500_prices_2010_2024.csv")
BENCHMARK_TICKER = "SPY"


def create_regime_interpretability_plot(price_data_path, benchmark_ticker, output_path):
    """Creates and saves a plot showing the identified market regimes."""
    if not os.path.exists(price_data_path):
        print(f"Error: Price data not found at {price_data_path}")
        return

    price_data = pd.read_csv(price_data_path, index_col="date", parse_dates=True)
    spy_prices = price_data[benchmark_ticker]

    regime_detector = EnsembleRegimeDetector(sma_weight=0.7, mrs_weight=0.3)
    regime_probs = regime_detector.detect_regime(spy_prices)

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(spy_prices.loc[regime_probs.index], label="SPY Price")

    risk_off_periods = regime_probs[regime_probs["risk_off_probability"] > 0.5]
    for start, end in get_continuous_periods(risk_off_periods.index):
        ax.axvspan(start, end, color="red", alpha=0.2, label="Risk-Off Period")

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    ax.set_title("Regime Interpretability: SPY Price and Identified Risk-Off Periods")
    ax.set_ylabel("Price")
    ax.set_xlabel("Date")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Regime plot saved to {output_path}")


def get_continuous_periods(dates):
    """Finds continuous periods from a DatetimeIndex."""
    if not isinstance(dates, pd.DatetimeIndex) or dates.empty:
        return

    periods = []
    start = dates[0]
    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days > 1:
            periods.append((start, dates[i - 1]))
            start = dates[i]
    periods.append((start, dates[-1]))
    return periods


if __name__ == "__main__":
    output_file = os.path.join(RESULTS_DIR, "regime_interpretability.png")
    create_regime_interpretability_plot(PRICE_DATA_PATH, BENCHMARK_TICKER, output_file)
