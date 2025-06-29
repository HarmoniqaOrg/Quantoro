"""
Core Backtesting Engine for Quantoro.

This module provides the BacktestEngine class, which orchestrates rolling-window
backtests. It manages the timeline, data slicing, rebalancing, and portfolio state.
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, Generator, Tuple, Dict, Any

from src.optimization.cvar_optimizer import CVaROptimizer, OptimizationResult

logger = logging.getLogger(__name__)


class BacktestEngine:
    """
    Orchestrates a rolling-window backtest.
    """

    def __init__(
        self,
        returns_data: pd.DataFrame,
        optimizer: CVaROptimizer,
        start_date: str,
        end_date: str,
        rebalance_frequency: str = "M",  # 'M' for monthly, 'Q' for quarterly
        lookback_window: int = 252,
        transaction_cost_bps: float = 5.0,  # 5 basis points
    ):
        """
        Initializes the backtesting engine.

        Args:
            returns_data (pd.DataFrame): DataFrame of asset returns.
            optimizer (CVaROptimizer): The portfolio optimization model.
            start_date (str): The start date of the backtest ('YYYY-MM-DD').
            end_date (str): The end date of the backtest ('YYYY-MM-DD').
            rebalance_frequency (str): 'M' for monthly, 'Q' for quarterly.
            lookback_window (int): Number of days for the rolling lookback window.
            transaction_cost_bps (float): Transaction costs in basis points.
        """
        self.returns_data = returns_data
        self.optimizer = optimizer
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.rebalance_frequency = rebalance_frequency
        self.lookback_window = lookback_window
        self.transaction_cost = transaction_cost_bps / 10000.0
        self.current_weights: Optional[np.ndarray] = None

        self._validate_inputs()
        self.rebalance_dates = self._get_rebalance_dates()

    def _validate_inputs(self):
        """Validates that the date range is within the available data."""
        if (
            self.start_date < self.returns_data.index.min()
            or self.end_date > self.returns_data.index.max()
        ):
            raise ValueError("Backtest date range is outside the available data range.")

    def _get_rebalance_dates(self) -> pd.DatetimeIndex:
        """Calculates the rebalancing dates based on the specified frequency."""
        all_dates = self.returns_data.loc[self.start_date : self.end_date].index
        # Generate potential rebalance dates and then select only those that exist in our data
        potential_dates = pd.date_range(
            start=self.start_date, end=self.end_date, freq=f"{self.rebalance_frequency}S"
        )
        # Use get_indexer to find the positions of our desired rebalance dates
        # 'bfill' will find the next valid business day if the desired date is a weekend/holiday
        indexer = all_dates.get_indexer(potential_dates, method="bfill")
        # Filter out any invalid (-1) indices and return the actual dates
        return all_dates[indexer[indexer != -1]]

    def run_rolling_backtest(self) -> Generator[Tuple[pd.Timestamp, pd.DataFrame], None, None]:
        """
        Generator that yields the data for each rebalancing period.
        """
        for rebalance_date in self.rebalance_dates:
            window_start_index = (
                self.returns_data.index.searchsorted(rebalance_date) - self.lookback_window
            )
            if window_start_index < 0:
                logger.warning(
                    f"Not enough data for lookback window on {rebalance_date}. Skipping."
                )
                continue

            returns_window = self.returns_data.iloc[
                window_start_index : self.returns_data.index.searchsorted(rebalance_date)
            ]
            yield rebalance_date, returns_window

    def rebalance(
        self,
        rebalance_date: pd.Timestamp,
        returns_window: pd.DataFrame,
        alpha_scores: Optional[pd.Series] = None,
        regime_prob: Optional[float] = None,
    ) -> Optional[OptimizationResult]:
        """
        Executes one rebalancing step: optimize and update weights.

        Args:
            rebalance_date (pd.Timestamp): The current rebalancing date.
            returns_window (pd.DataFrame): The lookback window of returns data.
            alpha_scores (Optional[pd.Series]): Alpha signals for the assets.
            regime_prob (Optional[float]): The probability of the current market regime.

        Returns:
            Optional[OptimizationResult]: The result from the optimizer, or None if failed.
        """
        logger.debug(f"Rebalancing on {rebalance_date.date()}...")

        # Align alpha scores with the universe of the returns window
        if alpha_scores is not None:
            alpha_scores = alpha_scores.reindex(returns_window.columns).fillna(0)

        try:
            # Prepare optional arguments for the optimizer to be passed as kwargs
            # This makes the call compatible with the base optimizer's signature for mypy
            optimizer_kwargs: Dict[str, Any] = {}
            if alpha_scores is not None:
                optimizer_kwargs["alpha_scores"] = alpha_scores
            if regime_prob is not None:
                optimizer_kwargs["regime_prob"] = regime_prob

            result = self.optimizer.optimize(
                returns=returns_window,
                current_weights=self.current_weights,
                **optimizer_kwargs,
            )

            if result and result.status in ["optimal", "optimal_inaccurate"]:
                self.current_weights = result.weights
            else:
                logger.warning(
                    f"Optimization failed or returned no solution on {rebalance_date.date()}. Weights not updated."
                )
                # Keep previous weights if optimization fails
                return None

            return result

        except Exception as e:
            logger.error(
                f"Exception during optimization on {rebalance_date.date()}: {e}", exc_info=True
            )
            return None
