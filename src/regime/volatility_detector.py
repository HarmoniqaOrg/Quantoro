"""
Implements a simple, robust regime detector based on a volatility threshold.
"""
import pandas as pd


class VolatilityThresholdDetector:
    """
    Detects market regimes based on a simple volatility threshold.
    This provides a robust, non-hanging alternative to complex models like HMM.
    """

    def __init__(self, window: int = 21, quantile: float = 0.75):
        """
        Initializes the detector.

        Args:
            window (int): The rolling window for volatility calculation.
            quantile (float): The quantile to use as the threshold for defining a high-volatility regime.
        """
        self.window = window
        self.quantile = quantile
        self.name = f"VolatilityThreshold_{window}_{quantile}"

    def fit_predict(self, returns: pd.Series) -> pd.Series:
        """
        Identifies regimes based on volatility.

        Args:
            returns (pd.Series): The series of asset returns.

        Returns:
            pd.Series: A series of regime scores (0 for risk-off, 1 for risk-on).
        """
        volatility = returns.rolling(self.window).std().dropna()
        threshold = volatility.quantile(self.quantile)

        # Risk-off (0) if volatility is above the threshold, risk-on (1) otherwise
        risk_scores = (volatility <= threshold).astype(float)

        return risk_scores
