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

        # Drop initial NaNs from the rolling calculation before proceeding
        valid_rolling_vol = rolling_vol.dropna()

        if valid_rolling_vol.empty:
            return pd.Series(dtype=float)

        # Use an expanding window on the valid data to calculate the threshold
        threshold = valid_rolling_vol.expanding().quantile(self.quantile)

        # Risk-on (1) if volatility is below the threshold, risk-off (0) otherwise.
        # This correctly identifies periods of high volatility as "risk-off" (0).
        risk_scores = (valid_rolling_vol <= threshold).astype(float)

        return risk_scores
