import logging
from typing import Callable, Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class BaseSignalProcessor:
    """Base class for signal processors to hold common initialization."""

    def __init__(
        self,
        signals_data: Dict[str, Dict[str, pd.DataFrame]],
        selected_features: Optional[List[str]] = None,
    ):
        self.signals_data = signals_data
        self.selected_features = selected_features


class SignalProcessor(BaseSignalProcessor):
    """Processes raw FMP signals into a composite alpha score."""

    def __init__(
        self,
        signals_data: Dict[str, Dict[str, pd.DataFrame]],
        selected_features: Optional[List[str]] = None,
    ):
        super().__init__(signals_data, selected_features)
        self.feature_map: Dict[str, Callable[..., float]] = {
            "analyst_recs": self._score_analyst_recs,
            "insider_trades": self._score_insider_trades,
        }

    def _score_analyst_recs(self, ticker_data: Dict[str, pd.DataFrame]) -> float:
        recs = ticker_data.get("analyst_recs", pd.DataFrame())
        if recs.empty or "rating" not in recs.columns:
            return 0.0
        score_map = {"strong buy": 2, "buy": 1, "hold": 0, "sell": -1, "strong sell": -2}
        recs["rating_lower"] = recs["rating"].str.lower()
        scores = recs["rating_lower"].map(score_map).mean()
        return scores if not np.isnan(scores) else 0.0

    def _score_insider_trades(self, ticker_data: Dict[str, pd.DataFrame]) -> float:
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

    def generate_composite_alpha_scores(
        self, current_date: Optional[pd.Timestamp] = None
    ) -> pd.DataFrame:
        alpha_scores = {}
        features_to_use = self.selected_features or list(self.feature_map.keys())
        for ticker, data in self.signals_data.items():
            scores = []
            for name in features_to_use:
                if name in self.feature_map:
                    score = self.feature_map[name](data)
                    if score != 0.0:
                        scores.append(score)
            alpha_scores[ticker] = np.mean(scores) if scores else 0.0
        return pd.DataFrame.from_dict(alpha_scores, orient="index", columns=["alpha_score"])


class DynamicSignalProcessor(SignalProcessor):
    """Extends SignalProcessor to handle time-aware signals with exponential decay."""

    def __init__(
        self,
        signals_data: Dict[str, Dict[str, pd.DataFrame]],
        decay_halflife_days: int = 30,
        selected_features: Optional[List[str]] = None,
    ):
        super().__init__(signals_data, selected_features)
        self.decay_halflife = decay_halflife_days
        self.feature_map: Dict[str, Callable[[Dict[str, pd.DataFrame], pd.Timestamp], float]] = {
            "analyst_recs": self._score_analyst_recs_decay,
            "insider_trades": self._score_insider_trades_decay,
        }

    def generate_composite_alpha_scores(
        self, current_date: Optional[pd.Timestamp] = None
    ) -> pd.DataFrame:
        if current_date is None:
            raise ValueError("current_date must be provided for DynamicSignalProcessor")
        alpha_scores = {}
        features_to_use = self.selected_features or list(self.feature_map.keys())
        for ticker, data in self.signals_data.items():
            scores = [
                self.feature_map[name](data, current_date)
                for name in features_to_use
                if name in self.feature_map
            ]
            valid_scores = [s for s in scores if s != 0.0]
            alpha_scores[ticker] = np.mean(valid_scores) if valid_scores else 0.0
        return pd.DataFrame.from_dict(alpha_scores, orient="index", columns=["alpha_score"])

    def _score_analyst_recs_decay(
        self, ticker_data: Dict[str, pd.DataFrame], current_date: pd.Timestamp
    ) -> float:
        recs_df = ticker_data.get("analyst_recs")
        if (
            recs_df is None
            or recs_df.empty
            or "rating" not in recs_df.columns
            or "publishedDate" not in recs_df.columns
        ):
            return 0.0
        recs = recs_df.copy()
        recs["date"] = pd.to_datetime(recs["publishedDate"], errors="coerce")
        recs = recs.dropna(subset=["date"])
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
        trades_df = ticker_data.get("insider_trades")
        if trades_df is None or trades_df.empty or "transactionDate" not in trades_df.columns:
            return 0.0
        trades = trades_df.copy()
        trades["date"] = pd.to_datetime(trades["transactionDate"], errors="coerce")
        trades = trades.dropna(subset=["date"])
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
        alpha_scores = {}
        features_to_use = self.selected_features or list(self.feature_map.keys())
        for ticker, data in self.signals_data.items():
            scores = []
            for name in features_to_use:
                signal_data = data.get(name)
                if name in self.feature_map and signal_data is not None and not signal_data.empty:
                    score = self.feature_map[name](data, current_date)
                    if score != 0.0:
                        scores.append(score)
            alpha_scores[ticker] = np.mean(scores) if scores else 0.0
        return pd.DataFrame.from_dict(alpha_scores, orient="index", columns=["alpha_score"])


class CrossAssetAlphaProcessor(DynamicSignalProcessor):
    """Combines FMP signals with cross-asset momentum."""

    def generate_combined_alpha(
        self, stock_returns: pd.DataFrame, spy_returns: pd.Series, current_date: pd.Timestamp
    ) -> pd.Series:
        fmp_alpha = self.generate_time_aware_alpha_scores(current_date)["alpha_score"]
        cross_asset_scores = self._calculate_cross_asset_momentum(stock_returns, spy_returns)
        fmp_alpha, cross_asset_scores = fmp_alpha.align(
            cross_asset_scores, join="right", fill_value=0
        )
        combined_alpha = 0.6 * cross_asset_scores + 0.4 * fmp_alpha
        if combined_alpha.std() > 0:
            combined_alpha = (combined_alpha - combined_alpha.mean()) / combined_alpha.std()
        logger.info(
            f"Generated combined alpha for {current_date}: mean={combined_alpha.mean():.3f}, std={combined_alpha.std():.3f}"
        )
        return combined_alpha.fillna(0.0)

    def _calculate_cross_asset_momentum(
        self, stock_returns: pd.DataFrame, spy_returns: pd.Series
    ) -> pd.Series:
        lookback = 252
        if len(spy_returns) < lookback or len(stock_returns) < lookback:
            logging.warning(
                f"Not enough data for cross-asset alpha (need {lookback} days). Returning zero scores."
            )
            return pd.Series(0.0, index=stock_returns.columns)
        spy_momentum = spy_returns.tail(lookback).mean() * 252
        stock_momentum = stock_returns.tail(lookback).mean() * 252
        cross_signal = (0.5 * spy_momentum) - (0.3 * stock_momentum)
        return np.tanh(cross_signal).fillna(0.0)
