import unittest
import pandas as pd
import numpy as np
from typing import Dict

from src.alpha.signal_processor import DynamicSignalProcessor


class TestDynamicSignalProcessor(unittest.TestCase):
    def setUp(self):
        """Set up common test data."""
        self.tickers = ["AAPL", "MSFT"]
        self.current_date = pd.to_datetime("2023-12-31")

        # Mock signals data with specific dates
        self.mock_signals_data = {
            "AAPL": {
                "analyst_recs": pd.DataFrame(
                    {"date": [pd.to_datetime("2023-12-01")], "rating": ["Buy"]}
                )
            },
            "MSFT": {
                "insider_trades": pd.DataFrame(
                    {
                        "date": [pd.to_datetime("2023-11-01")],
                        "transactionType": ["P-Purchase"],
                        "securitiesTransacted": [100],
                        "price": [300],
                    }
                )
            },
        }
        self.processor = DynamicSignalProcessor(self.mock_signals_data, decay_halflife_days=30)

        # Mock returns data for cross-asset alpha
        dates = pd.date_range(end=self.current_date, periods=300)
        self.stock_returns = pd.DataFrame(
            np.random.randn(300, 2) * 0.01, index=dates, columns=self.tickers
        )
        self.spy_returns = pd.Series(np.random.randn(300) * 0.01, index=dates, name="SPY")

    def test_signal_decay(self):
        """Test that older signals have their scores decayed correctly."""
        # Make AAPL's signal fresh and MSFT's stale
        self.mock_signals_data["AAPL"]["analyst_recs"]["date"] = [self.current_date]
        self.mock_signals_data["MSFT"]["insider_trades"]["date"] = [
            self.current_date - pd.Timedelta(days=30)
        ]  # 1 half-life old

        processor = DynamicSignalProcessor(self.mock_signals_data, decay_halflife_days=30)
        decayed_scores = processor.generate_time_aware_fmp_scores(self.current_date)

        # Base scores are simple averages of dummy scores
        base_aapl_score = 1.0  # Buy = 1
        base_msft_score = 1.0  # Purchase = 1

        # Expected decay
        expected_aapl_score = base_aapl_score * np.exp(-np.log(2) * 0 / 30)  # No decay
        expected_msft_score = base_msft_score * np.exp(-np.log(2) * 30 / 30)  # 50% decay

        self.assertAlmostEqual(
            decayed_scores.loc["AAPL", "alpha_score"], expected_aapl_score, places=5
        )
        self.assertAlmostEqual(
            decayed_scores.loc["MSFT", "alpha_score"], expected_msft_score, places=5
        )

    def test_cross_asset_alpha_logic(self):
        """Test the logic of the cross-asset momentum signal."""
        # Case 1: Strong bond market, weak stock market (Expect positive alpha)
        spy_returns_positive = self.spy_returns.copy() + 0.005
        stock_returns_negative = self.stock_returns.copy() - 0.005
        alpha_scores_pos = self.processor.generate_cross_asset_alpha(
            stock_returns_negative, spy_returns_positive
        )
        self.assertTrue(
            all(alpha_scores_pos > 0), "Expected positive alpha when bonds outperform stocks"
        )

        # Case 2: Weak bond market, strong stock market (Expect negative alpha)
        spy_returns_negative = self.spy_returns.copy() - 0.005
        stock_returns_positive = self.stock_returns.copy() + 0.005
        alpha_scores_neg = self.processor.generate_cross_asset_alpha(
            stock_returns_positive, spy_returns_negative
        )
        self.assertTrue(
            all(alpha_scores_neg < 0), "Expected negative alpha when stocks outperform bonds"
        )

    def test_cross_asset_alpha_insufficient_data(self):
        """Test that it returns zeros when data is insufficient."""
        short_stock_returns = self.stock_returns.iloc[-100:]
        short_spy_returns = self.spy_returns.iloc[-100:]
        alpha_scores = self.processor.generate_cross_asset_alpha(
            short_stock_returns, short_spy_returns
        )
        self.assertTrue(all(alpha_scores == 0), "Expected zero alpha scores with insufficient data")


if __name__ == "__main__":
    unittest.main()
