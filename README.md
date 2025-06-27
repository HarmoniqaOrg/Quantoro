# Quantoro: A Framework for Advanced CVaR Portfolio Optimization

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

This repository contains the implementation of a quantitative investment strategy framework, progressing from a baseline Conditional Value-at-Risk (CVaR) optimization to advanced regime-aware and ML-driven alpha models.

---

## ❯ Performance Highlights (2020-2024)

The final **Hybrid Regime-Aware Alpha Model** delivered robust performance, successfully navigating market turbulence by blending macroeconomic regime signals with ML-driven stock selection.

| Strategy                      | Annualized Return | Annualized Volatility | Sharpe Ratio | Max Drawdown |
| ----------------------------- | ----------------- | --------------------- | ------------ | ------------ |
| **Hybrid ML Alpha Model (C)** | **19.93%**        | **16.82%**            | **1.16**     | **-27.85%**  |
| Regime-Aware CVaR (B)         | 15.85%            | 17.19%                | 0.94         | -28.40%      |
| Baseline CVaR (A)             | 15.62%            | 17.25%                | 0.93         | -29.72%      |

*Performance metrics are calculated on out-of-sample data from Jan 2020 to Dec 2024.*

---

## ❯ Core Strategies Implemented

This project develops and backtests three distinct portfolio optimization strategies:

1.  **Task A: Baseline CVaR Optimization**
    - Implements the CVaR optimization methodology as described in the CLEIR paper.
    - Minimizes the 95% CVaR of the tracking error against an equal-weight benchmark, rebalancing quarterly.

2.  **Task B: Regime-Aware Enhancement**
    - Enhances the baseline model with a dynamic risk framework based on market regimes.
    - Uses an `EnsembleRegimeDetector` that combines a trend-following (SMA) model and a volatility (Mean Reversion Speed) model to produce a continuous "Risk-Off" probability.
    - The optimizer dynamically adjusts its parameters based on this probability, becoming more defensive in turbulent markets.

3.  **Task C: ML-Driven Alpha Integration**
    - Integrates alternative data and machine learning to generate alpha signals.
    - A LightGBM model is trained on FMP signals and momentum features to predict 63-day forward returns.
    - The optimizer's objective function is modified to simultaneously minimize CVaR and maximize exposure to these ML-generated alpha scores.

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

Task C requires an API key from [Financial Modeling Prep (FMP)](https://site.financialmodelingprep.com/).

1.  **Create a `.env` file** from the example template:
    ```bash
    cp .env.example .env
    ```
2.  **Add your FMP API key** to the newly created `.env` file:
    ```
    FMP_API_KEY=your_key_here
    ```

### Running the Backtests

You can run the backtest for each strategy using the following commands from the root directory:

```bash
# Run the baseline CVaR backtest (Task A)
python -m src.run_full_backtest

# Run the regime-aware backtest (Task B)
python -m src.run_regime_aware_backtest

# Run the ML-driven alpha backtest (Task C)
python -m src.run_ml_alpha_backtest
```
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
