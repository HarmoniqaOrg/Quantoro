# Product Requirements Document - Quantoro

## 1. Project Overview
This document outlines the final product requirements, design decisions, and outcomes for the **Quantoro** project. The goal was to implement and evaluate a series of quantitative investment strategies, starting with a baseline CVaR optimization and progressing to more advanced models incorporating market regimes and machine learning-driven alpha signals, as per the eToro Alpha Pods assignment.

---

## 2. Core Strategy Requirements

The project successfully implemented three distinct strategies:

- **Task A: Baseline CVaR Optimization**: Implement the CVaR optimization methodology from the CLEIR paper to replicate an equal-weight benchmark while minimizing tail risk (95% CVaR).
- **Task B: Regime-Aware Enhancement**: Enhance the baseline model with a dynamic risk framework. The model must detect market regimes (e.g., "Risk-On" vs. "Risk-Off") and adjust its risk-taking (CVaR constraints, penalties) accordingly.
- **Task C: Hybrid ML Alpha Model**: Integrate alternative data and machine learning to generate alpha signals. The optimizer's objective function must be modified to simultaneously minimize CVaR and maximize exposure to these ML-generated alpha scores.

---

## 3. Final Technical Specifications

The following parameters were standardized across all backtests to ensure comparability:

- **Universe**: A fixed list of 60 liquid S&P 100 stocks.
- **Backtest Period**: January 2010 - December 2024.
- **Rebalancing Frequency**: Quarterly.
- **Lookback Window**: 252 trading days (1 year).
- **CVaR Confidence Level (α)**: 95% (default).
- **Max Position Weight**: 7% (default, dynamically adjusted in regime model).
- **Transaction Costs**: 10 bps (0.10%) per transaction.
- **Optimization Solver**: `SCS` (used across all `cvxpy` optimizations for stability).

---

## 4. Key Design & Architecture Decisions

This log summarizes the key technical and design decisions made throughout the project lifecycle.

- **Universe Selection**: Replaced the volatile `pytickersymbols` library with a hardcoded list of 60 liquid tickers.
  - **Reason**: Ensured backtest reproducibility and stability by removing non-common stock tickers and API lookup failures.

- **Data Fetching**: Implemented an asynchronous data loader using `aiohttp` and `asyncio`.
  - **Reason**: Efficiently handled API rate limits from Financial Modeling Prep (FMP) and sped up data acquisition. API failures for individual tickers are now handled gracefully without halting the entire process.

- **Solver Standardization**: Selected `SCS` as the default solver for all `cvxpy` optimizations.
  - **Reason**: `SCS` provided the best balance of stability and out-of-the-box compatibility, resolving runtime errors encountered with other solvers like `ECOS`.

- **Backtest Engine Robustness**: The rolling backtester was enhanced with a fallback mechanism.
  - **Reason**: If an optimization step fails for a given period, the engine now holds the previous period's weights instead of crashing. This ensures the backtest runs to completion.

- **Regime-Aware Model Design**: An `EnsembleRegimeDetector` was built, combining a trend-following (SMA) model and a volatility (Mean Reversion Speed) model.
  - **Reason**: The ensemble approach produces a more robust, continuous "Risk-Off" probability, avoiding binary switching and allowing the optimizer to adjust its risk parameters smoothly.

- **Hybrid ML Alpha Model Design**: A dual-objective `AlphaAwareCVaROptimizer` was implemented.
  - **Reason**: The optimizer's objective function `Minimize(CVaR - λ * PortfolioAlpha)` effectively balances the competing goals of minimizing tail risk and maximizing exposure to ML-generated alpha signals. The `λ` parameter controls the trade-off.

---

## 5. Success Metrics & Final Outcomes

- **Primary Goal**: Outperform the baseline strategy (Task A) on a risk-adjusted basis (Sharpe Ratio).
  - **Outcome**: **Not Achieved.** In the unique 2020-2024 market environment, the Baseline CVaR model delivered the highest Sharpe Ratio. The more complex Regime-Aware (B) and Hybrid ML (C) models, while theoretically more advanced, were slightly hampered by transaction costs and market 'whipsawing'. Their attempts to de-risk were often followed by sharp market recoveries, causing them to miss out on gains and ultimately deliver lower risk-adjusted returns than the simpler baseline. This provided a valuable lesson on the trade-offs between model complexity and performance in volatile markets.

- **Secondary Goal**: Deliver a clear, professional, and fully reproducible project.
  - **Outcome**: **Achieved.** The project includes a `Makefile` for one-command execution, comprehensive documentation (`README.md`, `report.md`), clean, modular code, and passes all quality checks. The entire pipeline from backtesting to report generation is fully automated.

---

## 6. Final Project Status

**Status: Complete & Ready for Submission**

All tasks outlined in the assignment—Baseline CVaR (A), Regime-Aware Enhancement (B), and Hybrid ML Alpha (C)—have been successfully implemented, debugged, and backtested. All technical hurdles, including solver issues and data pipeline failures, have been resolved. The project documentation has been updated to reflect the final results, and a functional `Makefile` has been created for easy reproducibility. The project is now complete and ready for final report generation and submission.
