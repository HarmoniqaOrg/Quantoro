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

    def get_regime_statistics(self, regimes: pd.Series) -> dict:
        """
        Calculate regime duration and transition probabilities.

        Args:
            regimes (pd.Series): A pandas Series of regime signals (1 for risk-on, 0 for risk-off).

        Returns:
            dict: A dictionary containing average regime duration and the transition matrix.
        """
        if regimes.empty or regimes.nunique() < 2:
            return {
                'avg_duration_days': float('nan'),
                'transition_matrix': pd.DataFrame()
            }
            
        # Calculate durations of consecutive regimes
        regime_changes = regimes.diff().fillna(0) != 0
        # The size of each group of consecutive non-changes gives the duration
        regime_durations = regimes.groupby(regime_changes.cumsum()).size()

        # Transition matrix
        transitions = pd.crosstab(regimes.shift(1), regimes, normalize='index')
        
        return {
            'avg_duration_days': regime_durations.mean(),
            'transition_matrix': transitions
        }

    def get_regime_statistics(self, regimes: pd.Series) -> dict:
        """
        Calculate regime duration and transition probabilities.

        Args:
            regimes (pd.Series): A pandas Series of regime signals (1 for risk-on, 0 for risk-off).

        Returns:
            dict: A dictionary containing average regime duration and the transition matrix.
        """
        if regimes.empty or regimes.nunique() < 2:
            return {
                'avg_duration_days': float('nan'),
                'transition_matrix': pd.DataFrame()
            }
            
        # Calculate durations of consecutive regimes
        regime_changes = regimes.diff().fillna(0) != 0
        # The size of each group of consecutive non-changes gives the duration
        regime_durations = regimes.groupby(regime_changes.cumsum()).size()

        # Transition matrix
        transitions = pd.crosstab(regimes.shift(1), regimes, normalize='index')
        
        return {
            'avg_duration_days': regime_durations.mean(),
            'transition_matrix': transitions
        }

    def get_regime_statistics(self, regimes: pd.Series) -> dict:
        """
        Calculate regime duration and transition probabilities.

        Args:
            regimes (pd.Series): A pandas Series of regime signals (1 for risk-on, 0 for risk-off).

        Returns:
            dict: A dictionary containing average regime duration and the transition matrix.
        """
        if regimes.empty or regimes.nunique() < 2:
            return {
                'avg_duration_days': float('nan'),
                'transition_matrix': pd.DataFrame()
            }
            
        # Calculate durations of consecutive regimes
        regime_changes = regimes.diff().fillna(0) != 0
        # The size of each group of consecutive non-changes gives the duration
        regime_durations = regimes.groupby(regime_changes.cumsum()).size()

        # Transition matrix
        transitions = pd.crosstab(regimes.shift(1), regimes, normalize='index')
        
        return {
            'avg_duration_days': regime_durations.mean(),
            'transition_matrix': transitions
        }
