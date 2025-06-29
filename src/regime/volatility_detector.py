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
        # Calculate rolling volatility to avoid using future data
        rolling_vol = returns.rolling(self.window).std()

        # Use an expanding window to calculate the quantile, removing look-ahead bias
        threshold = rolling_vol.expanding().quantile(self.quantile)

        # Risk-on (1) if volatility is below the threshold, risk-off (0) otherwise.
        # This correctly identifies periods of high volatility as "risk-off" (0).
        risk_scores = (rolling_vol <= threshold).astype(float)

        return risk_scores.dropna()
