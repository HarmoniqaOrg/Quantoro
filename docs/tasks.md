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

### Pending [ ]
- [ ] **Generate Final Plots**
  - [ ] Plot CVaR index performance against equal-weighted and cap-weighted benchmarks.

## Task B: ML Enhancements

### Pending [ ]
- [ ] **Research & Design**
  - [ ] Choose an ML enhancement strategy (e.g., regime detection, tail-risk model).
  - [ ] Identify necessary data sources.
  - [ ] Design the model architecture and backtesting integration plan.
- [ ] **Implementation**
  - [ ] Implement the ML model.
  - [ ] Integrate the model into the backtesting framework.
- [ ] **Evaluation & Reporting**
  - [ ] Run out-of-sample backtest (2020-2024).
  - [ ] Generate performance comparison and interpretability analysis (e.g., SHAP).
- **Acceptance**: Improves Sharpe by >0.1

## Task C: Alternative Data (FMP)

### Pending [ ]
- [ ] FMP API integration for alternative data.
- [ ] Microstructure signals.
- [ ] Smart money tracking.
- [ ] Alpha signal generation.
- **Acceptance**: Additional 1-1.5% alpha

## Issues/Blockers [!]
- None currently
