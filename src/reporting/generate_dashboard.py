import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "results"
METRICS_FILE = os.path.join(RESULTS_DIR, "consolidated_performance_metrics.csv")


def create_performance_dashboard(metrics_file, output_path):
    """Creates and saves a dashboard of key performance metrics."""
    if not os.path.exists(metrics_file):
        print(f"Error: Metrics file not found at {metrics_file}")
        return

    df = pd.read_csv(metrics_file, index_col=0)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Comprehensive Performance Dashboard", fontsize=20)

    # Annual Return
    df.loc["Annual Return"].plot(kind="bar", ax=axes[0, 0], color=["#3498db", "#2ecc71", "#e74c3c"])
    axes[0, 0].set_title("Annual Return (%)")
    axes[0, 0].tick_params(axis="x", rotation=0)

    # Annual Volatility
    df.loc["Annual Volatility"].plot(
        kind="bar", ax=axes[0, 1], color=["#3498db", "#2ecc71", "#e74c3c"]
    )
    axes[0, 1].set_title("Annual Volatility (%)")
    axes[0, 1].tick_params(axis="x", rotation=0)

    # Sharpe Ratio
    df.loc["Sharpe Ratio"].plot(kind="bar", ax=axes[1, 0], color=["#3498db", "#2ecc71", "#e74c3c"])
    axes[1, 0].set_title("Sharpe Ratio")
    axes[1, 0].tick_params(axis="x", rotation=0)

    # Max Drawdown
    df.loc["Max Drawdown"].plot(kind="bar", ax=axes[1, 1], color=["#3498db", "#2ecc71", "#e74c3c"])
    axes[1, 1].set_title("Max Drawdown (%)")
    axes[1, 1].tick_params(axis="x", rotation=0)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path)
    print(f"Dashboard saved to {output_path}")


if __name__ == "__main__":
    output_file = os.path.join(RESULTS_DIR, "comprehensive_dashboard.png")
    create_performance_dashboard(METRICS_FILE, output_file)
