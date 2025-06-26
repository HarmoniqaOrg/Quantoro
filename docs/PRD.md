# Product Requirements Document - Quantoro

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

- **Primary Metric**: The enhanced strategy (Task B) must outperform the baseline strategy (Task A) on a risk-adjusted basis (Sharpe Ratio) over the 2020-2024 backtest period. **(Achieved)**
- **Secondary Metric**: The final report must be clear, professional, and fully reproducible. **(Achieved)**

## 7. Final Project Status

**Status: Completed**

All tasks outlined in the assignment have been successfully implemented, backtested, and documented. The final deliverables, including the comprehensive `report.pdf`, all source code, and result files, have been generated and are ready for submission.
