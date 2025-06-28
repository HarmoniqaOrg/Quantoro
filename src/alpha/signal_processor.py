import pandas as pd
import numpy as np
from typing import Dict
import logging

logger = logging.getLogger(__name__)

# --- Base Classes ---


class BaseSignalProcessor:
    """Base class for signal processors to hold common initialization."""

    def __init__(
        self, signals_data: Dict[str, Dict[str, pd.DataFrame]], selected_features: list = None
    ):
        self.signals_data = signals_data
        self.selected_features = selected_features


class SignalProcessor(BaseSignalProcessor):
    """
    Processes raw FMP signals into a composite alpha score.
    """

    def __init__(
        self, signals_data: Dict[str, Dict[str, pd.DataFrame]], selected_features: list = None
    ):
        super().__init__(signals_data, selected_features)
        self.feature_map = {
            "analyst_recs": self._score_analyst_recs,
            "insider_trades": self._score_insider_trades,
        }

    def _score_analyst_recs(self, ticker_data: Dict[str, pd.DataFrame]) -> float:
        """Scores analyst recommendations."""
        recs = ticker_data.get("analyst_recs", pd.DataFrame())
        if recs.empty or "rating" not in recs.columns:
            return 0.0

        score_map = {"strong buy": 2, "buy": 1, "hold": 0, "sell": -1, "strong sell": -2}
        recs["rating_lower"] = recs["rating"].str.lower()
        scores = recs["rating_lower"].map(score_map).mean()
        return scores if not np.isnan(scores) else 0.0

    def _score_insider_trades(self, ticker_data: Dict[str, pd.DataFrame]) -> float:
        """Scores insider transactions."""
        trades = ticker_data.get("insider_trades", pd.DataFrame())
        if (
            trades.empty
            or "transactionType" not in trades.columns
            or "securitiesTransacted" not in trades.columns
            or "price" not in trades.columns
        ):
            return 0.0

        trades["transactionValue"] = trades["securitiesTransacted"] * trades["price"]
        buys = trades[trades["transactionType"] == "P-Purchase"]["transactionValue"].sum()
        sells = trades[trades["transactionType"] == "S-Sale"]["transactionValue"].sum()
        total_volume = buys + sells
        return (buys - sells) / total_volume if total_volume > 0 else 0.0

    def generate_composite_alpha_scores(self) -> pd.DataFrame:
        """Generates a composite alpha score for each ticker."""
        alpha_scores = {}
        features_to_use = self.selected_features or self.feature_map.keys()

        for ticker, data in self.signals_data.items():
            scores = [
                self.feature_map[name](data)
                for name in features_to_use
                if name in self.feature_map and self.feature_map[name](data) != 0.0
            ]
            alpha_scores[ticker] = np.mean(scores) if scores else 0.0

        return pd.DataFrame.from_dict(alpha_scores, orient="index", columns=["alpha_score"])


# --- Dynamic and Cross-Asset Processors ---


class DynamicSignalProcessor(SignalProcessor):
    """
    Extends SignalProcessor to handle time-aware signals with exponential decay.
    """

    def __init__(
        self,
        signals_data: Dict[str, Dict[str, pd.DataFrame]],
        decay_halflife_days: int = 30,
        selected_features: list = None,
    ):
        super().__init__(signals_data, selected_features)
        self.decay_halflife = decay_halflife_days
        # Override the feature map to point to the time-aware scoring methods
        self.feature_map = {
            "analyst_recs": self._score_analyst_recs_decay,
            "insider_trades": self._score_insider_trades_decay,
        }

    def _score_analyst_recs_decay(
        self, ticker_data: Dict[str, pd.DataFrame], current_date: pd.Timestamp
    ) -> float:
        """Scores analyst recommendations with time decay."""
        recs = ticker_data.get("analyst_recs", pd.DataFrame()).copy()
        if recs.empty or "rating" not in recs.columns or "publishedDate" not in recs.columns:
            return 0.0

        recs["date"] = pd.to_datetime(recs["publishedDate"], errors="coerce")
        recs = recs.dropna(subset=["date"])
        # Filter for the last year of signals to avoid noise from very old data
        recs = recs.loc[
            (recs["date"] <= current_date) & (recs["date"] >= current_date - pd.Timedelta(days=252))
        ]
        if recs.empty:
            return 0.0

        score_map = {"strong buy": 2, "buy": 1, "hold": 0, "sell": -1, "strong sell": -2}
        recs["rating_lower"] = recs["rating"].str.lower()
        recs["score"] = recs["rating_lower"].map(score_map).fillna(0)

        recs["age_days"] = (current_date - recs["date"]).dt.days
        recs["weight"] = np.exp(-np.log(2) * recs["age_days"] / self.decay_halflife)

        weighted_score = np.average(recs["score"], weights=recs["weight"])
        return weighted_score if not np.isnan(weighted_score) else 0.0

    def _score_insider_trades_decay(
        self, ticker_data: Dict[str, pd.DataFrame], current_date: pd.Timestamp
    ) -> float:
        """Scores insider transactions with time decay."""
        trades = ticker_data.get("insider_trades", pd.DataFrame()).copy()
        if trades.empty or "transactionDate" not in trades.columns:
            return 0.0

        trades["date"] = pd.to_datetime(trades["transactionDate"], errors="coerce")
        trades = trades.dropna(subset=["date"])
        # Filter for the last year of signals to avoid noise from very old data
        trades = trades.loc[
            (trades["date"] <= current_date)
            & (trades["date"] >= current_date - pd.Timedelta(days=252))
        ]
        if trades.empty:
            return 0.0

        trades["transactionValue"] = trades["securitiesTransacted"] * trades["price"]
        trades["age_days"] = (current_date - trades["date"]).dt.days
        trades["weight"] = np.exp(-np.log(2) * trades["age_days"] / self.decay_halflife)

        buys = (
            trades[trades["transactionType"] == "P-Purchase"]["transactionValue"] * trades["weight"]
        ).sum()
        sells = (
            trades[trades["transactionType"] == "S-Sale"]["transactionValue"] * trades["weight"]
        ).sum()

        total_volume = buys + sells
        return (buys - sells) / total_volume if total_volume > 0 else 0.0

    def generate_time_aware_alpha_scores(self, current_date: pd.Timestamp) -> pd.DataFrame:
        """Generates a composite alpha score for each ticker using time-decayed signals."""
        alpha_scores = {}
        features_to_use = self.selected_features or self.feature_map.keys()

        for ticker, data in self.signals_data.items():
            scores = []
            for name in features_to_use:
                if (
                    name in self.feature_map
                    and data.get(name) is not None
                    and not data.get(name).empty
                ):
                    score = self.feature_map[name](data, current_date)
                    if score != 0.0:
                        scores.append(score)

            alpha_scores[ticker] = np.mean(scores) if scores else 0.0

        return pd.DataFrame.from_dict(alpha_scores, orient="index", columns=["alpha_score"])


class CrossAssetAlphaProcessor(DynamicSignalProcessor):
    """
    Combines FMP signals with cross-asset momentum from Pitkäjärvi et al. (2020).
    """

    def generate_combined_alpha(
        self, stock_returns: pd.DataFrame, spy_returns: pd.Series, current_date: pd.Timestamp
    ) -> pd.Series:
        """
        Combines time-aware FMP alpha with cross-asset momentum signals.
        """
        # 1. Get FMP alpha signals (time-awareness is a placeholder)
        fmp_alpha = self.generate_time_aware_alpha_scores(current_date)["alpha_score"]

        # 2. Calculate cross-asset momentum signals
        cross_asset_scores = self._calculate_cross_asset_momentum(stock_returns, spy_returns)

        # 3. Combine signals (60% cross-asset, 40% FMP)
        # Ensure indices are aligned before combining
        fmp_alpha, cross_asset_scores = fmp_alpha.align(
            cross_asset_scores, join="right", fill_value=0
        )
        combined_alpha = 0.6 * cross_asset_scores + 0.4 * fmp_alpha

        # 4. Normalize final scores
        if combined_alpha.std() > 0:
            combined_alpha = (combined_alpha - combined_alpha.mean()) / combined_alpha.std()

        logger.info(
            f"Generated combined alpha for {current_date}: mean={combined_alpha.mean():.3f}, std={combined_alpha.std():.3f}"
        )
        return combined_alpha.fillna(0.0)

    def _calculate_cross_asset_momentum(
        self, stock_returns: pd.DataFrame, spy_returns: pd.Series
    ) -> pd.Series:
        """
        Generates cross-asset momentum signals based on Pitkäjärvi et al. (2020).
        """
        lookback = 252  # Approx. 12 months
        if len(spy_returns) < lookback or len(stock_returns) < lookback:
            logging.warning(
                f"Not enough data for cross-asset alpha (need {lookback} days). Returning zero scores."
            )
            return pd.Series(0.0, index=stock_returns.columns)

        # Annualized momentum over the past year
        spy_momentum = spy_returns.tail(lookback).mean() * 252
        stock_momentum = stock_returns.tail(lookback).mean() * 252

        # Signal = β1 * BondMomentum - β2 * StockMomentum (β1=0.5, β2=0.3)
        cross_signal = (0.5 * spy_momentum) - (0.3 * stock_momentum)

        # Bound signal to [-1, 1] for stability
        return np.tanh(cross_signal).fillna(0.0)
