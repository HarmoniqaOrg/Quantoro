import pandas as pd
import numpy as np
from hmmlearn.hmm import GaussianHMM


class MRSGARCHRegimeDetector:
    """
    Detects market regimes using a Hidden Markov Model (HMM) on financial features,
    approximating a Multivariate Regime-Switching GARCH model.
    """

    def __init__(self, n_regimes: int = 2, lookback_window: int = 60):
        """
        Initializes the MRSGARCHRegimeDetector.

        Args:
            n_regimes (int): The number of hidden regimes to detect (e.g., 2 for bull/bear).
            lookback_window (int): The lookback period for calculating rolling features.
        """
        self.n_regimes = n_regimes
        self.lookback_window = lookback_window
        self.model = GaussianHMM(n_components=n_regimes, covariance_type="full", n_iter=1000)
        self.name = f"MRSGARCH_HMM_{n_regimes}_{lookback_window}"

    def _calculate_features(self, prices: pd.Series) -> pd.DataFrame:
        """
        Calculates rolling features (volatility, skewness, kurtosis) from a price series.
        """
        log_returns = np.log(prices / prices.shift(1))

        features = pd.DataFrame(index=prices.index)
        features["volatility"] = log_returns.rolling(window=self.lookback_window).std() * np.sqrt(
            252
        )
        features["skewness"] = log_returns.rolling(window=self.lookback_window).skew()
        features["kurtosis"] = log_returns.rolling(window=self.lookback_window).kurt()

        return features.dropna()

    def detect_regime(self, prices: pd.Series) -> pd.Series:
        """
        Fits the HMM and returns the probability of being in the high-volatility regime.

        Args:
            prices (pd.Series): A pandas Series of prices (e.g., SPY).

        Returns:
            pd.Series: A pandas Series of probabilities for the high-volatility regime.
        """
        features = self._calculate_features(prices)
        if features.empty:
            return pd.Series(index=prices.index, dtype=float).rename("regime_prob")

        self.model.fit(features)

        # Identify the high-volatility regime
        # The state with the highest mean volatility is considered the 'risk-off' or 'turbulent' state.
        high_vol_regime = np.argmax(self.model.means_[:, 0])

        # Get the posterior probabilities for each state
        posterior_probs = self.model.predict_proba(features)

        # Extract the probability of being in the high-volatility regime
        regime_probabilities = pd.Series(posterior_probs[:, high_vol_regime], index=features.index)

        # Reindex to match original price series, forward-filling initial NaNs
        return regime_probabilities.reindex(prices.index).ffill().fillna(0).rename("regime_prob")


class SMARegimeDetector:
    """
    Detects market regimes using a simple moving average crossover strategy.
    """

    def __init__(self, short_window: int = 50, long_window: int = 200):
        """
        Initializes the SMARegimeDetector.

        Args:
            short_window (int): The lookback period for the short moving average.
            long_window (int): The lookback period for the long moving average.
        """
        self.short_window = short_window
        self.long_window = long_window
        self.name = f"SMA_{self.short_window}_{self.long_window}"

    def detect_regime(self, prices: pd.Series) -> pd.Series:
        """
        Determines the regime based on the crossover of two moving averages.

        Args:
            prices (pd.Series): A pandas Series of prices (e.g., SPY).

        Returns:
            pd.Series: A pandas Series where 1 indicates a 'risk-on' regime
                       (short MA > long MA) and 0 indicates a 'risk-off' regime.
        """
        short_ma = prices.rolling(window=self.short_window).mean()
        long_ma = prices.rolling(window=self.long_window).mean()

        # A 'risk-on' regime is when the short-term trend is above the long-term trend
        regime = (short_ma > long_ma).astype(int)

        return regime.rename("regime_prob").ffill().fillna(0)
