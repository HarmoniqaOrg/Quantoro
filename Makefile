.PHONY: install run-all run-baseline run-regime run-hybrid clean report

# Default target
all: run-all

# Install dependencies
install:
	@echo "--- Installing dependencies from requirements.txt ---"
	pip install -r requirements.txt
	@echo "--- Installation complete ---"

# Run all backtests sequentially
run-all: run-baseline run-regime run-hybrid
	@echo "--- All backtests completed successfully ---"

# Run Task A: Baseline CVaR Backtest
run-baseline:
	@echo "--- Running Task A: Baseline CVaR Backtest ---"
	python src/run_full_backtest.py

# Run Task B: Regime-Aware CVaR Backtest
run-regime:
	@echo "--- Running Task B: Regime-Aware CVaR Backtest ---"
	python src/run_regime_aware_backtest.py

# Run Task C: Hybrid ML Alpha Backtest
run-hybrid:
	@echo "--- Running Task C: Hybrid ML Alpha Backtest ---"
	python src/run_hybrid_model_backtest.py

# Clean up generated results
clean:
	@echo "--- Cleaning up results directory ---"
	@if exist "results\\*.csv" (del /F /Q "results\\*.csv")
	@if exist "results\\*.png" (del /F /Q "results\\*.png")
	@echo "--- Cleanup complete ---"

# Generate the final report
report: run-all
	@echo "--- Consolidating results and generating final report ---"
	python src/reporting/consolidate_results.py
	python src/reporting/generate_final_report.py
	@echo "--- Final report generated successfully --- "
