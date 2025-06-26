# Task Tracking - Quantoro Project

## Legend
- [ ] Pending
- [@] In Progress  
- [x] Completed
- [!] Blocked/Issue

## Task A: Baseline CVaR Index

### Completed [x]
- [x] **Project Initialization & Data Pipeline**
  - [x] Initialized project structure and Git repository.
  - [x] Implemented `FmpDataLoader` with async fetching, caching, and robust error handling.
  - [x] Replaced unreliable `pytickersymbols` with a stable, hardcoded ticker list.
  - [x] Implemented `DataProcessor` for cleaning and returns calculation.
- [x] **CVaR Optimizer Implementation**
  - [x] Implemented `CVaROptimizer` with CVaR and LASSO penalty.
  - [x] Added robust error handling for infeasible optimizations.
- [x] **Backtesting Engine**
  - [x] Implemented `RollingCVaROptimizer.backtest` method.
  - [x] Implemented quarterly rebalancing logic.
  - [x] Integrated transaction cost model.
  - [x] Added fallback logic to hold weights on optimization failure.
- [x] **Final Results Generation**
  - [x] Ran full backtest for the entire period (2010-2024).
  - [x] Calculated all required performance metrics (Sharpe, Drawdown, etc.).
  - [x] Generated final CSV output for weights and performance metrics.
- [x] **Generate Final Plots**
  - [x] Plot CVaR index performance against equal-weighted and cap-weighted benchmarks.

## Task B: ML Enhancements

### Completed [x]
- [x] **Research & Design**
  - [x] Choose an ML enhancement strategy (e.g., regime detection, tail-risk model).
  - [x] Identify necessary data sources.
  - [x] Design the model architecture and backtesting integration plan.
- [x] **Implementation**
  - [x] Implement the ML model.
  - [x] Integrate the model into the backtesting framework.
- [x] **Evaluation & Reporting**
  - [x] Run out-of-sample backtest (2020-2024).
  - [x] Generate performance comparison and interpretability analysis (e.g., SHAP).
- **Acceptance**: Improves Sharpe by >0.1
- [x] **Reporting**
  - [x] Generate model interpretability output (e.g., feature importance).
  - [x] Write method note (≤400 words) for report.

## Task C: Alternative Data (FMP)

### Completed [x] 
- [x] **FMP API Integration**
  - [x] Implemented `FmpPremiumSignals` to fetch analyst and insider data.
- [x] **Alpha Signal Generation**
  - [x] Implemented `SignalProcessor` to create a composite alpha score.
- [x] **Optimizer Integration**
  - [x] Created `AlphaAwareCVaROptimizer` to use alpha scores in the objective.
  - [x] Updated `RollingCVaROptimizer` to be compatible with the new optimizer.
- [x] **Evaluation**
  - [x] Run and debug the final `run_alpha_backtest.py` script.
  - [x] Analyze performance metrics of the alpha-aware strategy.
- **Acceptance**: Additional 1-1.5% alpha

## Issues/Blockers [!]
- None currently
