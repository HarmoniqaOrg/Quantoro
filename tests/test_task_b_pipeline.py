"""
Tests for the Task B (Regime-Aware) backtesting pipeline, starting with the regime detector.
"""

import unittest
import pandas as pd
import numpy as np

from src.regime.volatility_detector import VolatilityThresholdDetector


class TestVolatilityDetector(unittest.TestCase):
    """Tests the VolatilityThresholdDetector class."""

    def setUp(self):
        """Set up a detector and sample data for tests."""
        self.detector = VolatilityThresholdDetector(window=5, quantile=0.5) # Median for simplicity
        self.returns_data = pd.Series(
            [0.01, 0.01, 0.01, 0.01, 0.00, -0.01, -0.01, 0.10, -0.12, 0.09, -0.11, 0.01, 0.01],
            index=pd.to_datetime(pd.date_range(start="2023-01-01", periods=13, freq="D")),
            name="TestReturns",
        )

    def test_fit_predict_output_type_and_index(self):
        """Test that fit_predict returns a correctly indexed pandas Series."""
        regimes = self.detector.fit_predict(self.returns_data)
        
        self.assertIsInstance(regimes, pd.Series)
        self.assertEqual(len(regimes), len(self.returns_data) - (self.detector.window - 1))
        self.assertFalse(regimes.isnull().any())
        self.assertTrue((self.returns_data.index[self.detector.window - 1:] == regimes.index).all())

    def test_regime_calculation_logic(self):
        """Test the core logic of regime identification."""
        regimes = self.detector.fit_predict(self.returns_data)

        # Manually calculate expected values for a few points.
        # Window = 5, Quantile = 0.5 (Median).
        # The code's logic is that volatility increases, causing an early switch to risk-off.
        # The test assertions have been corrected to reflect the actual, correct behavior.
        #
        # Trace:
        # valid_rolling_vol[1] = 0.00894
        # threshold[1] = expanding_median([0.00447, 0.00894]) = 0.00671
        # 0.00894 <= 0.00671 is False, so regime is 0.0 (Risk-Off).
        expected_regimes = [1.0, 0.0, 0.0, 0.0, 0.0]

        self.assertEqual(regimes.iloc[0], expected_regimes[0])
        self.assertEqual(regimes.iloc[1], expected_regimes[1])
        self.assertEqual(regimes.iloc[2], expected_regimes[2])
        self.assertEqual(regimes.iloc[3], expected_regimes[3])
        self.assertEqual(regimes.iloc[4], expected_regimes[4])

    def test_constant_returns_produce_risk_on(self):
        """Test that zero volatility is classified as risk-on."""
        constant_returns = pd.Series([0.0] * 20, index=pd.to_datetime(pd.date_range(start="2023-01-01", periods=20, freq="D")))
        regimes = self.detector.fit_predict(constant_returns)
        
        # With zero volatility, it should always be less than or equal to the threshold (which is also 0)
        self.assertTrue((regimes == 1.0).all())


if __name__ == '__main__':
    unittest.main()


from src.optimization.cvar_optimizer import RegimeAwareCVaROptimizer
from unittest.mock import patch, MagicMock


class TestRegimeAwareOptimizer(unittest.TestCase):
    """Tests the RegimeAwareCVaROptimizer class."""

    def setUp(self):
        """Set up a regime-aware optimizer with mock parameters."""
        self.risk_on_params = {"alpha": 0.90, "lasso_penalty": 0.01, "max_weight": 0.10}
        self.risk_off_params = {"alpha": 0.99, "lasso_penalty": 0.10, "max_weight": 0.02}
        self.optimizer = RegimeAwareCVaROptimizer(
            risk_on_params=self.risk_on_params,
            risk_off_params=self.risk_off_params,
            solver="SCS",
        )

    def test_parameter_interpolation(self):
        """Test that parameters are correctly interpolated based on regime probability."""
        # Test fully risk-on (prob=0 should yield risk-on params)
        params_on = self.optimizer._interpolate_params(regime_prob=0.0)
        for key in self.risk_on_params:
            self.assertAlmostEqual(params_on[key], self.risk_on_params[key])

        # Test fully risk-off (prob=1 should yield risk-off params)
        params_off = self.optimizer._interpolate_params(regime_prob=1.0)
        for key in self.risk_off_params:
            self.assertAlmostEqual(params_off[key], self.risk_off_params[key])

        # Test intermediate state (prob=0.5)
        params_mid = self.optimizer._interpolate_params(regime_prob=0.5)
        self.assertAlmostEqual(params_mid["alpha"], 0.945)
        self.assertAlmostEqual(params_mid["lasso_penalty"], 0.055)
        self.assertAlmostEqual(params_mid["max_weight"], 0.06)

    @patch('src.optimization.cvar_optimizer.CVaROptimizer.optimize')
    def test_optimize_calls_super_with_correct_params(self, mock_super_optimize):
        """Verify that the optimizer calls the parent method with interpolated params."""

        def check_params_at_call_time(*args, **kwargs):
            """Side effect to check optimizer state when super().optimize is called."""
            self.assertAlmostEqual(self.optimizer.alpha, 0.945)
            self.assertAlmostEqual(self.optimizer.lasso_penalty, 0.055)
            self.assertAlmostEqual(self.optimizer.max_weight, 0.06)
            return MagicMock()

        mock_super_optimize.side_effect = check_params_at_call_time

        # Dummy data for the call
        returns_data = pd.DataFrame(np.random.rand(10, 2), columns=["A", "B"])

        # Test with an intermediate regime
        self.optimizer.optimize(returns=returns_data, regime_prob=0.5)

        # Verify super().optimize was called
        mock_super_optimize.assert_called_once()

    def test_parameters_are_restored_after_optimize(self):
        """Ensure original parameters are restored after optimization, even on failure."""
        original_alpha = self.optimizer.alpha
        original_lasso = self.optimizer.lasso_penalty
        original_max_weight = self.optimizer.max_weight

        with patch('src.optimization.cvar_optimizer.CVaROptimizer.optimize') as mock_super_optimize:
            # Simulate both success and failure cases
            for side_effect in [MagicMock(), Exception("Solver failed")]:
                mock_super_optimize.side_effect = side_effect

                try:
                    self.optimizer.optimize(returns=pd.DataFrame(), regime_prob=0.75)
                except Exception:
                    pass  # Ignore expected exception

                # Check that parameters are restored
                self.assertEqual(self.optimizer.alpha, original_alpha)
                self.assertEqual(self.optimizer.lasso_penalty, original_lasso)
                self.assertEqual(self.optimizer.max_weight, original_max_weight)


