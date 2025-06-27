# Makefile for Quantoro Project

# Define the Python interpreter
PYTHON = python

# Define directories
SRC_DIR = src
RESULTS_DIR = results
REPORTS_DIR = reporting

# Define primary output files for each stage
BASELINE_PERF = $(RESULTS_DIR)/baseline_cvar_performance.csv
REGIME_PERF = $(RESULTS_DIR)/regime_aware_cvar_performance.csv
ALPHA_PERF = $(RESULTS_DIR)/alpha_aware_cvar_performance.csv
# Assuming the report script generates at least one image
REPORT_VISUAL = $(RESULTS_DIR)/img/performance_summary.png

# --- Targets ---
.PHONY: all clean report

# Default target: run the full pipeline from start to finish.
all: $(REPORT_VISUAL)

# --- Reporting ---
# The report target depends on all backtests being successfully completed.
report: $(REPORT_VISUAL)

$(REPORT_VISUAL): $(ALPHA_PERF)
	@echo "--- Generating Final Report Visuals ---"
	$(PYTHON) $(SRC_DIR)/$(REPORTS_DIR)/generate_report_visuals.py
	@echo "--- Full pipeline complete. Results are in the '$(RESULTS_DIR)' directory. ---"

# --- Backtests ---
# Each backtest depends on the output of the previous one.
$(ALPHA_PERF): $(REGIME_PERF) $(SRC_DIR)/run_alpha_backtest.py
	@echo "--- Running Alpha-Aware CVaR Backtest ---"
	$(PYTHON) $(SRC_DIR)/run_alpha_backtest.py

$(REGIME_PERF): $(BASELINE_PERF) $(SRC_DIR)/run_regime_aware_backtest.py
	@echo "--- Running Enhanced (Regime-Aware) CVaR Backtest ---"
	$(PYTHON) $(SRC_DIR)/run_regime_aware_backtest.py

$(BASELINE_PERF): $(SRC_DIR)/run_full_backtest.py
	@echo "--- Running Baseline CVaR Backtest ---"
	$(PYTHON) $(SRC_DIR)/run_full_backtest.py

# Target to clean up result files
clean:
	@echo "Cleaning up results directory..."
	@if exist "$(RESULTS_DIR)" ( \
		del /F /Q "$(RESULTS_DIR)\*.csv" 2>nul & \
		del /F /Q "$(RESULTS_DIR)\img\*.png" 2>nul \
	)
	@echo "Cleanup complete."
