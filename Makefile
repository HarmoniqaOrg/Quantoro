.PHONY: install run-all run-baseline run-regime run-hybrid clean report quality format lint type-check

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
	python -m src.run_full_backtest

# Run Task B: Regime-Aware CVaR Backtest
run-regime:
	@echo "--- Running Task B: Regime-Aware CVaR Backtest ---"
	python -m src.run_regime_aware_backtest

# Run Task C: Hybrid ML Alpha Backtest
run-hybrid:
	@echo "--- Running Task C: Hybrid ML Alpha Backtest ---"
	python -m src.run_hybrid_model_backtest

# Clean up generated results
clean:
	@echo "--- Cleaning up results directory ---"
	@if exist "results\\*.csv" (del /F /Q "results\\*.csv")
	@if exist "results\\*.png" (del /F /Q "results\\*.png")
	@echo "--- Cleanup complete ---"

# Generate the final report
report: run-all
	@echo "--- Consolidating results and generating final report ---"
	python -m src.utils.generate_task_b_report
	python -m src.reporting.consolidate_results
	python -m src.utils.generate_consolidated_plot
	python -m src.reporting.generate_final_report
	@echo "--- Final report generated successfully --- "

# --- Code Quality ---

# Run all quality checks
quality: format lint type-check
	@echo "--- Code quality checks completed ---"

# Format code with Black
format:
	@echo "--- Formatting code with Black ---"
	python -m black . --line-length 100

# Lint with Ruff and apply auto-fixes
lint:
	@echo "--- Linting with Ruff ---"
	python -m ruff check . --fix

# Type check with MyPy
type-check:
	@echo "--- Type checking with MyPy ---"
	python -m mypy src/ --ignore-missing-imports
