# Quantoro: A Framework for Advanced CVaR Portfolio Optimization

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

This repository contains the implementation of a quantitative investment strategy framework, progressing from a baseline Conditional Value-at-Risk (CVaR) optimization to advanced regime-aware and alpha-aware models. The project was completed as a take-home assignment for Alpha Pods.

---

## ❯ Performance Highlights (2020-2024)

The **Regime-Aware CVaR** strategy demonstrated the most robust performance, successfully navigating volatile market conditions by dynamically adjusting its risk posture. It outperformed both the baseline and alpha-aware models on a risk-adjusted basis.

| Strategy             | Annualized Return | Annualized Volatility | Sharpe Ratio | Max Drawdown |
| -------------------- | ----------------- | --------------------- | ------------ | ------------ |
| **Regime-Aware CVaR**| **15.87%**        | **17.22%**            | **0.94**     | **-28.79%**  |
| Baseline CVaR        | 15.62%            | 17.25%                | 0.93         | -29.72%      |
| Alpha-Aware CVaR     | 14.37%            | 17.47%                | 0.86         | -27.82%      |

*For a complete breakdown of all performance metrics, please see the [Final Report](report.pdf).*

---

## ❯ Core Strategies Implemented

This project develops and backtests three distinct portfolio optimization strategies:

1.  **Task A: Baseline CVaR Optimization**
    - Implements the CVaR optimization methodology as described in the CLEIR paper.
    - Minimizes the 95% CVaR of the tracking error against an equal-weight benchmark, rebalancing quarterly.

2.  **Task B: Regime-Aware Enhancement**
    - Enhances the baseline model with a dynamic risk framework based on market regimes.
    - Uses a **50-day vs. 200-day Simple Moving Average (SMA) crossover** on the SPY ETF to identify "Risk-On" and "Risk-Off" states.
    - The optimizer adjusts its parameters (e.g., `cvar_alpha`, `lasso_penalty`) to be more defensive during "Risk-Off" periods and more aggressive during "Risk-On" periods.

3.  **Task C: Alpha-Aware Integration**
    - Integrates alternative data to generate alpha and further enhance portfolio returns.
    - Sources fundamental signals (e.g., P/E Ratio, ROE) from the Financial Modeling Prep (FMP) API.
    - The optimizer's objective function is modified to simultaneously minimize CVaR and maximize exposure to these alpha signals.

---

## ❯ Getting Started

### Prerequisites
- Python 3.9+
- Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd quantoro
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### API Key Configuration

The Alpha-Aware strategy (Task C) requires an API key from [Financial Modeling Prep (FMP)](https://site.financialmodelingprep.com/).

1.  **Create a `.env` file** from the example template:
    ```bash
    cp .env.example .env
    ```
2.  **Add your FMP API key** to the newly created `.env` file:
    ```
    FMP_API_KEY=your_key_here
    ```

### Running the Analysis

You can run the full analysis pipeline, including backtests and report generation, using the following commands from the root directory:

```bash
# Run the baseline CVaR backtest (Task A)
python src/run_baseline_backtest.py

# Run the regime-aware backtest (Task B)
python src/run_enhanced_backtest.py

# Run the alpha-aware backtest (Task C)
python src/run_alpha_backtest.py

# Generate all report visuals
python src/reporting/generate_report_visuals.py

# Assemble the final PDF report
python src/reporting/generate_final_report.py
```

---

## ❯ Project Structure

```
quantoro/
├── data/               # Data storage and caching
├── docs/               # Project documentation
├── results/            # Backtest outputs, metrics, and plots
├── src/                # Source code
│   ├── alpha/          # Alpha signal generation
│   ├── backtesting/    # Backtesting engine and metrics
│   ├── data/           # Data loading and processing
│   ├── ml/             # Regime detection model (SMA Crossover)
│   ├── optimization/   # CVaR optimizers
│   └── reporting/      # Report and visualization generation
├── .env.example        # Example environment file
├── README.md           # This file
├── report.pdf          # Final consolidated PDF report
└── requirements.txt    # Project dependencies
```

---

## ❯ Detailed Report

For a deep dive into the methodology, analysis, and conclusions for each task, please see the comprehensive final report:

**[➡️ View Final Report (report.pdf)](report.pdf)**
