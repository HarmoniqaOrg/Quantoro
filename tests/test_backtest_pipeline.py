"""
End-to-end tests for the Task A backtesting and reporting pipeline.

This module verifies that the entire process, from data loading to file generation,
runs correctly and produces all the expected artifacts with the correct structure.
"""

import pytest
import pandas as pd
import asyncio
import logging

# We need to import the main functions from the scripts we want to test
from src.run_full_backtest import main as run_backtest
from src.reporting.run_visualizations import main as run_visuals


@pytest.mark.pipeline
def test_task_a_full_pipeline(tmp_path, monkeypatch):
    """
    Runs the entire Task A pipeline end-to-end and validates all outputs.
    This single test handles setup, execution, and validation to avoid issues
    with running heavy processes inside pytest fixtures.
    """
    # 1. --- SETUP ---
    # Create a temporary directory for this test run
    results_dir = tmp_path
    logging.info(f"--- E2E Test: Using temporary results directory: {results_dir} ---")

    # Use monkeypatch to redirect all file outputs to our temp directory
    monkeypatch.setattr("src.run_full_backtest.RESULTS_DIR", results_dir)
    monkeypatch.setattr("src.reporting.generate_report_visuals.RESULTS_DIR", results_dir)

    # 2. --- EXECUTION ---
    logging.info("--- E2E Test: Running backtest pipeline ---")
    asyncio.run(run_backtest())
    run_visuals()
    logging.info("--- E2E Test: Finished backtest pipeline ---")

    # 3. --- VALIDATION ---
    # A. Verify that all expected CSV output files are generated and not empty
    expected_csv = [
        "baseline_cvar_index.csv",
        "baseline_cvar_performance_metrics.csv",
        "baseline_daily_returns.csv",
        "baseline_daily_weights.csv",
        "equal_weighted_daily_returns.csv",
        "equal_weighted_daily_weights.csv",
        "sp500_prices_2010_2024.csv",
    ]
    for filename in expected_csv:
        file_path = results_dir / filename
        assert file_path.exists(), f"Expected CSV file not found: {filename}"
        assert file_path.stat().st_size > 0, f"CSV file is empty: {filename}"

    # B. Verify that all expected plot images are generated and not empty
    expected_plots = ["task_a_performance_comparison.png"]
    for plot_name in expected_plots:
        plot_path = results_dir / plot_name
        assert plot_path.exists(), f"Expected plot file not found: {plot_name}"
        assert plot_path.stat().st_size > 0, f"Plot file is empty: {plot_name}"

    # C. Check the structure and content of the performance metrics CSV
    metrics_path = results_dir / "baseline_cvar_performance_metrics.csv"
    metrics_df = pd.read_csv(metrics_path, index_col=0)
    assert not metrics_df.empty
    assert "Sharpe Ratio" in metrics_df.index
    assert "Annual Turnover" in metrics_df.index
    assert "Max Drawdown" in metrics_df.index

    # D. Check the structure of the cumulative index CSV
    index_path = results_dir / "baseline_cvar_index.csv"
    index_df = pd.read_csv(index_path, index_col=0, parse_dates=True)
    assert not index_df.empty
    assert isinstance(index_df.index, pd.DatetimeIndex)
    assert index_df.iloc[0, 0] == 100.0, "Index should start at 100."
