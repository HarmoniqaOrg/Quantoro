import pandas as pd

class RegimeDetector:
    """
    Detects market regimes based on a simple moving average (SMA) crossover strategy.
    """
    def __init__(self, lookback_short: int = 50, lookback_long: int = 200):
        """
        Initializes the RegimeDetector.

        Args:
            lookback_short (int): The lookback period for the short-term SMA.
            lookback_long (int): The lookback period for the long-term SMA.
        """
        if lookback_short >= lookback_long:
            raise ValueError("Short-term lookback must be less than long-term lookback.")
        self.lookback_short = lookback_short
        self.lookback_long = lookback_long
        self.name = f"SMA_{lookback_short}_{lookback_long}"

    def detect_regime(self, prices: pd.Series) -> pd.Series:
        """
        Detects the market regime for a given price series.

        A 'risk-on' regime (1) is signaled when the short-term SMA is above the long-term SMA.
        A 'risk-off' regime (0) is signaled otherwise.

        Args:
            prices (pd.Series): A pandas Series of prices (e.g., SPY).

        Returns:
            pd.Series: A pandas Series of regime signals (1 for risk-on, 0 for risk-off).
        """
        if not isinstance(prices, pd.Series):
            raise TypeError("Input 'prices' must be a pandas Series.")
            
        sma_short = prices.rolling(window=self.lookback_short, min_periods=self.lookback_short).mean()
        sma_long = prices.rolling(window=self.lookback_long, min_periods=self.lookback_long).mean()
        
        # Risk-on (1) when short > long, risk-off (0) otherwise
        regime = (sma_short > sma_long).astype(int)
        
        return regime.rename("regime")
