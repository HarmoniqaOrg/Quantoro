# Task Tracking - Quantoro Project

## Legend
- [ ] Pending
- [@] In Progress
- [x] Completed
- [!] Blocked/Issue

---

## 🎯 Active Tasks

- [@] **Task B Fix: Ensemble Regime Model**
  - [ ] Refactor regime detectors into separate files.
  - [ ] Fix logic in `MRSGARCHRegimeDetector`.
  - [ ] Create `EnsembleRegimeDetector` combining SMA and MRS-GARCH.
  - [ ] Update `RegimeAwareCVaROptimizer` with more balanced parameters.
  - [ ] Integrate ensemble model into `run_regime_aware_backtest.py`.

- [@] **Task C Enhancement: Cross-Asset Momentum**
  - [ ] Create `feature_config.py` with hand-picked features, skipping Boruta.
  - [ ] Implement `CrossAssetAlphaProcessor` in `signal_processor.py`.
  - [ ] Integrate new processor and features into `run_alpha_backtest.py`.

## ⏳ Pending & Blocked Tasks

- [!] **Final Reporting** - Assemble `report.pdf` with all findings. (Blocked by Task B & C completion)

## ✅ Completed Tasks

- [x] **Task A: Baseline CVaR Index** - All sub-tasks completed.
- [x] **Initial Implementations** - Foundational versions of Task B (SMA, MRS-GARCH) and Task C (FMP) are complete and serve as baselines for these enhancements.

---

## 🚀 Strategic Enhancement Sprint (Competition-Winning Phase)

### Day 1: Fix & Enhance Alpha Strategy (Task C)

- [x] **Enhance Signal Processor (`src/alpha/signal_processor.py`)**
  - [x] Implement `DynamicSignalProcessor` with signal decay logic.
  - [x] Implement `generate_cross_asset_alpha` based on Pitkäjärvi et al. (2020).
- [x] **Implement Boruta Feature Selection (`src/alpha/feature_selector.py`)**
  - [x] Create new file `feature_selector.py`.
  - [x] Implement `FinancialFeatureSelector` class based on Kursa & Rudnicki (2010).
- [x] **Update Alpha Backtest (`src/run_alpha_backtest.py`)**
  - [x] Integrate dynamic signal generation into the rebalancing loop.
  - [x] Combine cross-asset alpha with FMP signals.
- [x] **Unit & Integration Testing**
  - [x] Test `DynamicSignalProcessor` independently.
  - [x] Test `FinancialFeatureSelector` independently.
  - [x] Run a partial backtest to ensure integration works.

### Day 2: Sophisticated Regime Detection & Dynamic Optimization (Task B)

- [x] **Implement MRS-GARCH Regime Model (`src/ml/regime_detector.py`)**
  - [x] Replace existing `RegimeDetector` with `MRSGARCHRegimeDetector` based on Peng et al. (2022).
  - [x] Implement HMM logic with volatility, skewness, and kurtosis features.
- [x] **(Optional) Create Ensemble Regime Detector (`src/ml/ensemble_regime.py`)**
  - [x] Create new file `ensemble_regime.py`.
  - [x] Combine MRS-GARCH with other signals (SMA, Volatility) for a robust score.
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
