import unittest
import os
import pandas as pd
import shutil
from unittest.mock import patch
import numpy as np
import sys

# Add project root to Python path to allow for correct module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.run_regime_aware_backtest import main as run_regime_main


class TestTaskBIntegration(unittest.TestCase):
    """Integration test for the full regime-aware backtest pipeline."""

    def setUp(self):
        """Set up a temporary directory and sample data for the test."""
        self.temp_dir = os.path.join(os.path.dirname(__file__), "temp_results_task_b_integration")
        os.makedirs(self.temp_dir, exist_ok=True)
        self.sample_data_path = os.path.join(self.temp_dir, "sample_prices.csv")

        # Create a small, realistic sample price dataset with a seed for reproducibility
        np.random.seed(42)
        dates = pd.date_range(start="2021-12-01", end="2022-06-30", freq="B")
        n_dates = len(dates)

        price_data = {
            "SPY": 100 + np.random.randn(n_dates).cumsum() * 0.5,
            "AAPL": 150 + np.random.randn(n_dates).cumsum() * 0.6,
            "MSFT": 200 + np.random.randn(n_dates).cumsum() * 0.4,
            "GOOG": 2500 + np.random.randn(n_dates).cumsum() * 1.2,
        }
        sample_df = pd.DataFrame(price_data, index=dates)
        sample_df.index.name = "Date"
        sample_df.to_csv(self.sample_data_path)

    def tearDown(self):
        """Clean up the temporary directory after the test."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_regime_aware_pipeline_runs_and_creates_outputs(self):
        """
        Test that the full regime-aware backtest runs and produces the expected output files.
        """
        # Patch the configuration constants and the baseline function to isolate the test
        with patch("src.run_regime_aware_backtest.RESULTS_DIR", self.temp_dir), \
             patch("src.run_regime_aware_backtest.DATA_FILE", self.sample_data_path), \
             patch("src.run_regime_aware_backtest.BACKTEST_START_DATE", "2022-03-01"), \
             patch("src.run_regime_aware_backtest.BACKTEST_END_DATE", "2022-06-30"), \
             patch("src.run_regime_aware_backtest.run_baseline_for_comparison") as mock_baseline:

            # Run the main function from the script
            run_regime_main()

            # Verify the baseline function was not run with its complex logic
            mock_baseline.assert_called_once()

            # Check that the primary regime-aware output files were created
            expected_files = [
                "regime_aware_cvar_performance.csv",
                "regime_aware_rebalance_weights.csv",
                "regime_aware_daily_returns.csv",
            ]

            for filename in expected_files:
                file_path = os.path.join(self.temp_dir, filename)
                self.assertTrue(os.path.exists(file_path), f"Output file not found: {filename}")
                self.assertGreater(os.path.getsize(file_path), 0, f"Output file is empty: {filename}")


if __name__ == '__main__':
    unittest.main()
