# Product Requirements Document - Quantoro

## 🚀 Strategic Pivot & Enhancement Plan (Effective 2025-06-27)

**Status: In Enhancement Phase**

### 1. Rationale for Pivot

Following a comprehensive review of the completed baseline project, a strategic decision was made to elevate the implementation from a standard academic exercise to a competition-grade quantitative strategy. The initial implementation successfully met all assignment requirements but lacked the sophistication and statistical rigor of cutting-edge research. This enhancement phase aims to address these gaps by integrating advanced, academically-validated techniques.

### 2. Core Enhancements & Academic Grounding

The sprint focuses on three high-impact areas, each grounded in published research:

1.  **Dynamic Alpha Strategy (Task C Enhancement)**: The static alpha signal model will be replaced with a dynamic system incorporating:
    *   **Cross-Asset Momentum**: Implementing signals based on the findings of *Pitkäjärvi et al. (2020), "Cross-asset signals and time series momentum"*. This research demonstrates that past bond returns can predict future equity returns.
    *   **Feature Selection**: Employing the Boruta algorithm (*Kursa & Rudnicki, 2010*) to systematically select the most potent alpha factors, reducing noise and overfitting.

2.  **Sophisticated Regime Detection (Task B Enhancement)**: The simple SMA-crossover model will be replaced by a more robust regime detection engine:
    *   **MRS-GARCH Model**: Implementing a Multivariate Regime-Switching GARCH model as described by *Peng et al. (2022), "Portfolio Optimization on Multivariate Regime-Switching GARCH Model"*. This captures shifts in volatility, skewness, and kurtosis for more accurate regime identification.
    *   **Dynamic Risk Budgeting**: The optimizer will be upgraded to use the continuous output of the regime model to dynamically adjust risk parameters (CVaR alpha, LASSO penalty, position limits), following the continuous adjustment framework proposed by *Pesenti et al. (2023), "Risk Budgeting Allocation for Dynamic Risk Measures"*.

3.  **Rigorous Statistical Validation**: To prove the strategy's efficacy, we will add:
    *   **Bootstrap Significance Testing**: Using stationary bootstrap methods (*Efron & Tibshirani, 1993*) to generate robust confidence intervals for key performance metrics, validating that outperformance is not due to chance.
    *   **Academic-Quality Visualizations**: Creating publication-standard plots to clearly communicate the strategy's mechanics and performance drivers.

### 3. Expected Outcomes

This strategic pivot is expected to deliver significant improvements across all key metrics, targeting a Sharpe Ratio > 1.10 and an Information Ratio > 0.40, backed by statistically significant p-values.

---

## Project Overview
Implementation of CVaR-LASSO Enhanced Index Replication (CLEIR) with ML enhancements for eToro Alpha Pods assignment.

## Current Sprint: Project Setup
- **Objective**: Initialize project structure and development environment
- **Success Criteria**: All files created, dependencies installed, initial commit pushed
- **Design Decisions**: 
  - Using CVXPy for optimization (proven CVaR support)
  - PyTorch for ML models (better transformer support)
  - Async architecture for data fetching (FMP rate limits)

## Architecture Decisions Log
- **2024-01-XX**: Selected 60 most liquid S&P 100 stocks to balance diversification and liquidity
- **2024-01-XX**: Chose quarterly rebalancing to minimize transaction costs while maintaining responsiveness

## Technical Specifications
- **CVaR Confidence Level**: 95% (α = 0.95)
- **Max Position Size**: 5%
- **Transaction Costs**: 10 bps per side
- **Rebalancing**: Quarterly
- **Lookback Window**: 252 trading days
- **2025-06-25**: Replaced the `pytickersymbols` library with a hardcoded list of 60 tickers. **Reason**: The library provided an unstable list containing non-common stock tickers (e.g., preferred shares), causing silent failures in the data loading pipeline. A fixed list ensures reproducibility and stability.
- **2025-06-25**: Enhanced the data loader (`FmpDataLoader`) to handle individual ticker API failures gracefully using `asyncio.gather(return_exceptions=True)` instead of failing the entire batch.
- **2025-06-25**: Switched the default CVXPY solver from `ECOS` to `SCS` to resolve "solver not installed" errors and improve out-of-the-box compatibility.
- **2025-06-25**: Implemented a fallback mechanism in the rolling backtester to hold previous weights if an optimization step fails, preventing the backtest from crashing and ensuring continuity.
- **2025-06-26**: Designed and implemented an alpha-aware optimization strategy. **Components**:
    - **Data Source**: Financial Modeling Prep (FMP) for alternative data signals (analyst recommendations, insider trading).
    - **Signal Processing**: A `SignalProcessor` class normalizes and combines raw signals into a single composite alpha score per asset.
    - **Optimization**: The `AlphaAwareCVaROptimizer` modifies the core CVaR objective function to `Minimize(CVaR - alpha_factor * PortfolioAlpha)`, creating a dual-objective to balance risk minimization with alpha maximization.

## 6. Success Metrics

- **Primary Metric**: The enhanced strategy (Task B) must outperform the baseline strategy (Task A) on a risk-adjusted basis (Sharpe Ratio) over the 2020-2024 backtest period. **(Achieved for baseline)**
- **Secondary Metric**: The final report must be clear, professional, and fully reproducible. **(In Progress)**

## 7. Final Project Status

**Status: In Enhancement Phase**

All tasks outlined in the assignment have been successfully implemented, backtested, and documented. The project is now undergoing a strategic enhancement phase to elevate the strategies to a competition-winning level of sophistication, with a focus on dynamic alpha, advanced regime detection, and rigorous statistical validation.
