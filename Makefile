# Makefile for Quantoro Project

# Define the Python interpreter
PYTHON = python

# Define directories
SRC_DIR = src
RESULTS_DIR = results

# --- Targets ---
.PHONY: all backtest enhanced_backtest alpha_backtest report clean

# Default target: run the full pipeline from start to finish.
# The dependencies ensure sequential execution.
all: report

# --- Reporting --- 
# The report target depends on all backtests being successfully completed.
report: alpha_backtest
	@echo "--- Generating Final Report Visuals ---"
	$(PYTHON) $(SRC_DIR)/reporting/generate_report_visuals.py
	@echo "--- Full pipeline complete. Results are in the '$(RESULTS_DIR)' directory. ---"

# --- Backtests --- 
# Each backtest depends on the previous one, creating a chain.
alpha_backtest: enhanced_backtest
	@echo "--- Running Alpha-Aware CVaR Backtest ---"
	$(PYTHON) $(SRC_DIR)/run_alpha_backtest.py

enhanced_backtest: backtest
	@echo "--- Running Enhanced (Regime-Aware) CVaR Backtest ---"
	$(PYTHON) $(SRC_DIR)/run_enhanced_backtest.py

backtest:
	@echo "--- Running Baseline CVaR Backtest ---"
	$(PYTHON) $(SRC_DIR)/run_full_backtest.py

# Target to clean up result files
clean:
	@echo "Cleaning up results directory..."
	@if exist "$(RESULTS_DIR)" ( \
		del /F /Q "$(RESULTS_DIR)\*.csv" 2>nul & \
		del /F /Q "$(RESULTS_DIR)\*.png" 2>nul \
	)
	@echo "Cleanup complete."
