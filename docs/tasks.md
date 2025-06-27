# Task Tracking - Quantoro Project

## Legend
- [ ] Pending
- [@] In Progress
- [x] Completed
- [!] Blocked/Issue

---

## ✅ Foundational Work (Completed)

- [x] **Task A: Baseline CVaR Index** - All sub-tasks completed.
- [x] **Task B: Simple ML Enhancement (SMA Crossover)** - All sub-tasks completed.
- [x] **Task C: Basic Alpha Integration (Static FMP)** - All sub-tasks completed.
- [x] **Initial Documentation & Reporting** - All sub-tasks completed.

---

## 🚀 Strategic Enhancement Sprint (Competition-Winning Phase)

### Day 1: Fix & Enhance Alpha Strategy (Task C)

- [ ] **Enhance Signal Processor (`src/alpha/signal_processor.py`)**
  - [ ] Implement `DynamicSignalProcessor` with signal decay logic.
  - [ ] Implement `generate_cross_asset_alpha` based on Pitkäjärvi et al. (2020).
- [ ] **Implement Boruta Feature Selection (`src/alpha/feature_selector.py`)**
  - [ ] Create new file `feature_selector.py`.
  - [ ] Implement `FinancialFeatureSelector` class based on Kursa & Rudnicki (2010).
- [ ] **Update Alpha Backtest (`src/run_alpha_backtest.py`)**
  - [ ] Integrate dynamic signal generation into the rebalancing loop.
  - [ ] Combine cross-asset alpha with FMP signals.
- [ ] **Unit & Integration Testing**
  - [ ] Test `DynamicSignalProcessor` independently.
  - [ ] Test `FinancialFeatureSelector` independently.
  - [ ] Run a partial backtest to ensure integration works.

### Day 2: Sophisticated Regime Detection & Dynamic Optimization (Task B)

- [ ] **Implement MRS-GARCH Regime Model (`src/ml/regime_detector.py`)**
  - [ ] Replace existing `RegimeDetector` with `MRSGARCHRegimeDetector` based on Peng et al. (2022).
  - [ ] Implement HMM logic with volatility, skewness, and kurtosis features.
- [ ] **(Optional) Create Ensemble Regime Detector (`src/ml/ensemble_regime.py`)**
  - [ ] Create new file `ensemble_regime.py`.
  - [ ] Combine MRS-GARCH with other signals (SMA, Volatility) for a robust score.
- [ ] **Upgrade CVaR Optimizer (`src/optimization/cvar_optimizer.py`)**
  - [ ] Modify `RegimeAwareCVaROptimizer` to accept a continuous regime score.
  - [ ] Implement dynamic, continuous adjustment of `alpha`, `lasso_penalty`, and `max_weight` based on Pesenti et al. (2023).
- [ ] **Unit & Integration Testing**
  - [ ] Test `MRSGARCHRegimeDetector` and ensure it produces sensible regimes.
  - [ ] Test dynamic parameter adjustments in the optimizer.
  - [ ] Run a partial backtest with the new regime model and optimizer.

### Day 3: Statistical Validation & Final Reporting

- [ ] **Implement Statistical Tests (`src/backtesting/statistical_tests.py`)**
  - [ ] Create new file `statistical_tests.py`.
  - [ ] Implement `test_strategy_significance` with t-tests and Stationary Bootstrap CIs.
- [ ] **Create Academic-Quality Visualizations (`src/reporting/academic_plots.py`)**
  - [ ] Create new file `academic_plots.py`.
  - [ ] Implement multi-panel regime analysis plot.
  - [ ] Implement plots for rolling Information Ratio and bootstrap CIs.
- [ ] **Final Backtests & Report Generation**
  - [ ] Run full backtests for all three enhanced strategies.
  - [ ] Update the final report generation script to include new statistical tests and plots.
  - [ ] Write a new, compelling methodology section in the report referencing the academic papers.
  - [ ] Generate the final `report.pdf`.
