# Task Tracking - Quantoro Project

## Legend
- [ ] Pending
- [@] In Progress
- [x] Completed
- [!] Blocked/Issue

---

## 🎯 Active Tasks

- [x] **Final Cleanup & Submission**
  - [x] Assemble final `report.pdf` with all findings, methodologies, and visualizations.
  - [x] Final code review and cleanup.
  - [x] Push final changes for submission.

## ✅ Completed Tasks

- [x] **Project Setup & Initialization**
- [x] **Task A: Baseline CVaR Index**
  - [x] Implemented CVaR optimization based on CLEIR paper.
  - [x] Backtested successfully over the 2020-2024 period.
  - [x] Generated all required results and metrics.
- [x] **Task B: Regime-Aware Enhancement**
  - [x] Implemented `EnsembleRegimeDetector` using SMA and Volatility signals.
  - [x] Implemented `RegimeAwareCVaROptimizer` with dynamic parameter adjustment.
  - [x] Backtested successfully and demonstrated improved risk-adjusted returns.
  - [x] Completed method summary and interpretability report.
- [x] **Task C: Hybrid ML Alpha Model**
  - [x] Implemented data loader for FMP signals.
  - [x] Implemented LightGBM model for alpha score generation.
  - [x] Implemented `AlphaAwareCVaROptimizer` to integrate alpha scores.
  - [x] Successfully debugged and backtested the full hybrid model.
  - [x] Completed method summary and interpretability report.
- [x] **Fix Solver Issues**
  - [x] Updated all backtest scripts to use the 'SCS' solver, resolving runtime errors.
- [x] **Debug Core Backtest Engine & Benchmarks**
  - [x] Resolved persistent `KeyError: 'date'` in `RollingCVaROptimizer`.
  - [x] Refactored `backtest` method for robustness and clarity.
  - [x] Implemented rigorous quarterly-rebalanced equal-weighted benchmark with correct turnover calculation.
