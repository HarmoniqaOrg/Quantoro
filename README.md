# Quantoro: A Framework for Advanced CVaR Portfolio Optimization

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

This repository contains the implementation of a quantitative investment strategy framework, progressing from a baseline Conditional Value-at-Risk (CVaR) optimization to advanced regime-aware and ML-driven alpha models.

---

## ❯ Performance Highlights (2020-2024)

The final **Hybrid Regime-Aware Alpha Model** delivered robust performance, successfully navigating market turbulence by blending macroeconomic regime signals with ML-driven stock selection.

| Strategy                      | Annualized Return | Annualized Volatility | Sharpe Ratio | Max Drawdown |
| ----------------------------- | ----------------- | --------------------- | ------------ | ------------ |
| **Hybrid ML Alpha Model (C)** | **19.93%**        | **16.82%**            | **1.16**     | **-27.85%**  |
| Regime-Aware CVaR (B)         | 16.30%            | 17.11%                | 0.97         | -28.04%      |
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

The easiest way to run the backtests is by using the provided `Makefile`.

1.  **Run all backtests sequentially:**
    ```bash
    make run-all
    ```

2.  **Run individual backtests:**
    ```bash
    # Run Task A: Baseline CVaR
    make run-baseline

    # Run Task B: Regime-Aware CVaR
    make run-regime

    # Run Task C: Hybrid ML Alpha Model
    make run-hybrid
    ```

Alternatively, you can run the scripts directly:
```bash
python src/run_full_backtest.py
python src/run_regime_aware_backtest.py
python src/run_hybrid_model_backtest.py
```

### Generating the Final Report

After running the backtests, you can generate the final PDF report, which includes performance analysis and visualizations:

```bash
python src/reporting/generate_final_report.py
```

---

## ❯ Project Structure

```
quantoro/
├── docs/               # Project documentation (PRD, tasks, method summaries)
├── results/            # Backtest outputs, metrics, and plots
├── src/                # Source code
│   ├── alpha/          # Alpha signal generation (FMP signals)
│   ├── backtesting/    # Backtesting engine and performance metrics
│   ├── data/           # Data loading and processing
│   ├── optimization/   # CVaR optimizer implementations
│   ├── regime/         # Regime detection models
│   ├── reporting/      # Report and visualization generation
│   ├── utils/          # Utility functions
│   ├── config.py       # Configuration settings
│   ├── run_full_backtest.py
│   ├── run_regime_aware_backtest.py
│   └── run_hybrid_model_backtest.py
├── tests/              # Unit and integration tests
├── .env.example        # Example environment file for API keys
├── Makefile            # Makefile for easy execution of tasks
├── README.md           # This file
├── report.md           # Source for the final report
├── report.pdf          # Final consolidated PDF report
└── requirements.txt    # Project dependencies
```

---

## ❯ Detailed Report

For a deep dive into the methodology, analysis, and conclusions for each task, please see the comprehensive final report:

**[➡️ View Final Report (report.pdf)](report.pdf)**
