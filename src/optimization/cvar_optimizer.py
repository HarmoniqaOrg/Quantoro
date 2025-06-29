"""
CVaR Portfolio Optimizer
Implements the CLEIR methodology for Task A
"""

import logging
import numpy as np
import pandas as pd
import cvxpy as cp
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """Container for optimization results."""

    weights: np.ndarray
    cvar: float
    portfolio_return: float
    portfolio_volatility: float
    tracking_error: float
    turnover: float
    status: str
    solve_time: float


class CVaROptimizer:
    """
    Conditional Value-at-Risk (CVaR) portfolio optimizer with LASSO constraints.

    Implements the CLEIR methodology from Gendreau et al. (2019).
    """

    def __init__(
        self,
        alpha: float = 0.95,
        lasso_penalty: float = 1.5,
        max_weight: float = 0.05,
        transaction_cost: float = 0.002,  # Increased from 0.001 per feedback
        solver: str = "ECOS",
    ):
        """
        Initialize CVaR optimizer.

        Args:
            alpha: Confidence level for CVaR (default 0.95)
            lasso_penalty: LASSO penalty parameter (default 1.5)
            max_weight: Maximum weight per stock (default 0.05)
            transaction_cost: Transaction cost per trade (default 0.001)
            solver: CVXPY solver to use (default 'ECOS'). 'SCS' is a good alternative.
        """
        self.alpha = alpha
        self.lasso_penalty = lasso_penalty
        self.max_weight = max_weight
        self.transaction_cost = transaction_cost
        self.solver = solver

        logger.info(
            f"Initialized CVaROptimizer with alpha={alpha}, "
            f"lasso_penalty={lasso_penalty}, max_weight={max_weight}"
        )

    def _get_empty_result(self, n_assets: int, status: str = "failed") -> OptimizationResult:
        """Returns an empty OptimizationResult for failed optimizations."""
        return OptimizationResult(
            weights=np.full(n_assets, np.nan),
            cvar=np.nan,
            portfolio_return=np.nan,
            portfolio_volatility=np.nan,
            tracking_error=np.nan,
            turnover=np.nan,
            status=status,
            solve_time=0.0,
        )

    def optimize(
        self,
        returns: pd.DataFrame,
        benchmark_returns: Optional[pd.Series] = None,
        current_weights: Optional[np.ndarray] = None,
        **kwargs,
    ) -> OptimizationResult:
        """
        Optimize portfolio to minimize CVaR of tracking error.

        Args:
            returns: DataFrame of asset returns (T x N)
            benchmark_returns: Series of benchmark returns (T x 1)
            current_weights: Current portfolio weights for turnover calculation

        Returns:
            OptimizationResult containing optimal weights and metrics
        """
        # Fill NaNs to prevent numerical errors in the solver
        returns = returns.fillna(0.0)
        if benchmark_returns is not None:
            benchmark_returns = benchmark_returns.fillna(0.0)

        n_assets = returns.shape[1]

        try:
            n_scenarios = returns.shape[0]

            if benchmark_returns is None:
                benchmark_returns = returns.mean(axis=1)

            R = returns.values
            b = benchmark_returns.values.reshape(-1, 1)

            w = cp.Variable(n_assets)
            z = cp.Variable(n_scenarios)
            zeta = cp.Variable()

            tracking_error = (R @ w) - b.flatten()
            cvar = zeta + (1.0 / ((1 - self.alpha) * n_scenarios)) * cp.sum(z)

            constraints = [
                z >= 0,
                z >= -tracking_error - zeta,
                cp.sum(w) == 1.0,  # Fully invested constraint
                w >= 0,
                w <= self.max_weight,
            ]

            objective_terms = [cvar]
            if self.lasso_penalty > 0:
                objective_terms.append(self.lasso_penalty * cp.norm1(w))
            if current_weights is not None:
                turnover = cp.sum(cp.abs(w - current_weights))
                objective_terms.append(self.transaction_cost * turnover)

            objective = cp.Minimize(cp.sum(objective_terms))
            problem = cp.Problem(objective, constraints)

            # Try the default solver first, then fall back to SCS for robustness
            solvers = [self.solver]
            if self.solver != "SCS":
                solvers.append("SCS")

            for solver in solvers:
                try:
                    solver_kwargs = {"solver": solver, "verbose": False}
                    # Use more robust settings specifically for the SCS fallback solver
                    if solver == "SCS":
                        solver_kwargs.update(
                            {
                                "max_iters": 5000,
                                "eps": 1e-4,
                            }
                        )
                    problem.solve(**solver_kwargs)
                    if problem.status in ["optimal", "optimal_inaccurate"] and w.value is not None:
                        logger.info(f"Successfully solved with {solver}.")
                        break  # Exit loop on success
                except (cp.SolverError, ValueError) as e:
                    logger.warning(f"Solver {solver} failed with error: {e}. Trying next solver.")
                    continue

            if problem.status not in ["optimal", "optimal_inaccurate"]:
                logger.warning(f"Optimization status: {problem.status}. Returning empty result.")
                return self._get_empty_result(n_assets, status=problem.status)

            optimal_weights = w.value
            if optimal_weights is None:
                logger.error(
                    f"Opt status is {problem.status}, but weights are None. Returning empty."
                )
                return self._get_empty_result(n_assets, status=f"{problem.status}_no_weights")

            portfolio_ret_series = R @ optimal_weights
            tracking_err_series = portfolio_ret_series - b.flatten()
            turnover_val = (
                np.sum(np.abs(optimal_weights - current_weights))
                if current_weights is not None
                else 0.0
            )

            result = OptimizationResult(
                weights=optimal_weights,
                cvar=cvar.value,
                portfolio_return=np.mean(portfolio_ret_series),
                portfolio_volatility=np.std(portfolio_ret_series),
                tracking_error=np.std(tracking_err_series),
                turnover=turnover_val,
                status=problem.status,
                solve_time=problem.solver_stats.solve_time
                if problem.solver_stats.solve_time is not None
                else 0.0,
            )

            logger.info(f"Optimization complete: CVaR={result.cvar:.4f}, Status={result.status}")
            return result

        except Exception as e:
            logger.error(f"Optimization failed: {str(e)}")
            return self._get_empty_result(n_assets, status="exception")

    def calculate_portfolio_metrics(
        self,
        returns: pd.DataFrame,
        weights: np.ndarray,
        benchmark_returns: Optional[pd.Series] = None,
    ) -> Dict[str, float]:
        """
        Calculate comprehensive portfolio metrics.

        Args:
            returns: DataFrame of asset returns
            weights: Portfolio weights
            benchmark_returns: Benchmark returns for comparison

        Returns:
            Dictionary of portfolio metrics
        """
        # Portfolio returns
        portfolio_returns = returns @ weights

        # Basic metrics
        metrics = {
            "annual_return": portfolio_returns.mean() * 252,
            "annual_volatility": portfolio_returns.std() * np.sqrt(252),
            "sharpe_ratio": (portfolio_returns.mean() * 252)
            / (portfolio_returns.std() * np.sqrt(252)),
            "max_drawdown": self._calculate_max_drawdown(portfolio_returns),
            "calmar_ratio": (portfolio_returns.mean() * 252)
            / abs(self._calculate_max_drawdown(portfolio_returns)),
            "sortino_ratio": self._calculate_sortino_ratio(portfolio_returns),
            "cvar_95": self._calculate_cvar(portfolio_returns, 0.95),
            "cvar_99": self._calculate_cvar(portfolio_returns, 0.99),
        }

        # Tracking error metrics if benchmark provided
        if benchmark_returns is not None:
            tracking_error = portfolio_returns - benchmark_returns
            metrics.update(
                {
                    "tracking_error": tracking_error.std() * np.sqrt(252),
                    "information_ratio": (tracking_error.mean() * 252)
                    / (tracking_error.std() * np.sqrt(252)),
                    "beta": portfolio_returns.cov(benchmark_returns) / benchmark_returns.var(),
                    "correlation": portfolio_returns.corr(benchmark_returns),
                }
            )

        # Weight concentration metrics
        metrics.update(
            {
                "effective_n": 1 / np.sum(weights**2),
                "max_weight": np.max(weights),
                "n_positions": np.sum(weights > 0.001),
                "concentration_top5": np.sum(np.sort(weights)[-5:]),
            }
        )

        return metrics

    @staticmethod
    def _calculate_max_drawdown(returns: pd.Series) -> float:
        """Calculate maximum drawdown from returns series."""
        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.expanding().max()
        drawdowns = (cum_returns - running_max) / running_max
        return drawdowns.min()

    @staticmethod
    def _calculate_sortino_ratio(returns: pd.Series, mar: float = 0.0) -> float:
        """Calculate Sortino ratio."""
        excess_returns = returns - mar
        downside_returns = excess_returns[excess_returns < 0]
        downside_std = np.sqrt(np.mean(downside_returns**2))
        return (
            (returns.mean() * 252) / (downside_std * np.sqrt(252)) if downside_std > 0 else np.inf
        )

    @staticmethod
    def _calculate_cvar(returns: pd.Series, alpha: float) -> float:
        """Calculate Conditional Value at Risk (CVaR)."""
        var_threshold = np.percentile(returns, (1 - alpha) * 100)
        tail_losses = returns[returns <= var_threshold]
        return -tail_losses.mean() if len(tail_losses) > 0 else 0.0

    def calculate_risk_decomposition(self, returns: pd.DataFrame, weights: np.ndarray) -> pd.Series:
        """
        Calculate risk contribution by asset based on portfolio variance.

        Args:
            returns (pd.DataFrame): DataFrame of asset returns.
            weights (np.ndarray): Array of portfolio weights.

        Returns:
            pd.Series: Series of risk contributions for each asset.
        """
        portfolio_variance = weights.T @ returns.cov().values @ weights
        if portfolio_variance < 1e-9:
            return pd.Series(np.zeros_like(weights), index=returns.columns)

        # Marginal Contribution to Risk (MCTR)
        mctr = returns.cov().values @ weights

        # Risk Contribution (RC) = weight * MCTR / portfolio_stdev
        portfolio_stdev = np.sqrt(portfolio_variance)
        risk_contribution = weights * mctr / portfolio_stdev

        return pd.Series(risk_contribution, index=returns.columns)


class RollingCVaROptimizer:
    """
    Implements rolling window CVaR optimization with rebalancing.
    """

    def __init__(
        self, optimizer: CVaROptimizer, lookback_window: int = 252, rebalance_frequency: str = "Q"
    ):
        """
        Initialize rolling optimizer.

        Args:
            optimizer: CVaROptimizer instance
            lookback_window: Number of days for historical data
            rebalance_frequency: 'D', 'W', 'M', or 'Q'
        """
        self.optimizer = optimizer
        self.lookback_window = lookback_window
        self.rebalance_frequency = rebalance_frequency
        self.original_params = {
            "max_weight": optimizer.max_weight,
            "lasso_penalty": optimizer.lasso_penalty,
        }

    def backtest(
        self,
        returns: pd.DataFrame,
        benchmark_returns: pd.Series,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        alpha_scores: Optional[pd.DataFrame] = None,
        regimes: Optional[pd.Series] = None,
    ) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
        """
        Run rolling window backtest.

        Args:
            returns: Full dataset of returns.
            benchmark_returns: Benchmark returns.
            start_date: Backtest start date.
            end_date: Backtest end date.
            alpha_scores: DataFrame of alpha scores.
            regimes: Series of market regimes.

        Returns:
            A tuple containing:
            - DataFrame with backtest rebalance results.
            - Series with daily portfolio returns.
            - DataFrame with daily portfolio weights.
        """
        # 1. Filter date range
        if start_date:
            start_idx = returns.index.searchsorted(pd.to_datetime(start_date), side="left")
            returns = returns.iloc[start_idx:]
            benchmark_returns = benchmark_returns.iloc[start_idx:]
        if end_date:
            end_idx = returns.index.searchsorted(pd.to_datetime(end_date), side="right")
            returns = returns.iloc[:end_idx]
            benchmark_returns = benchmark_returns.iloc[:end_idx]

        rebalance_dates = self._get_rebalance_dates(returns.index, self.lookback_window)
        if rebalance_dates.empty:
            logger.error("No valid rebalance dates found.")
            return pd.DataFrame(), pd.Series(dtype=float), pd.DataFrame()

        # 2. Main backtest loop
        rebalance_results = []
        # Initialize weights for the first period
        current_weights = np.ones(returns.shape[1]) / returns.shape[1]

        for date in rebalance_dates:
            lookback_end_loc = returns.index.get_loc(date)
            assert isinstance(
                lookback_end_loc, int
            ), "Index lookup for rebalance date did not return a single integer location."
            lookback_start_loc = max(0, lookback_end_loc - self.lookback_window)
            lookback_returns = returns.iloc[lookback_start_loc:lookback_end_loc]
            lookback_benchmark = benchmark_returns.iloc[lookback_start_loc:lookback_end_loc]

            # Ensure current_weights match the current asset universe size
            if len(current_weights) != lookback_returns.shape[1]:
                current_weights = np.ones(lookback_returns.shape[1]) / lookback_returns.shape[1]

            # --- Parameter Adjustment (for compatible optimizers) ---
            optimizer_kwargs = {
                "returns": lookback_returns,
                "benchmark_returns": lookback_benchmark,
                "current_weights": current_weights,
            }
            if regimes is not None and hasattr(self.optimizer, "_interpolate_params"):
                regime_prob = regimes.asof(date)
                optimizer_kwargs["regime_prob"] = regime_prob

            if alpha_scores is not None and isinstance(
                self.optimizer, (AlphaAwareCVaROptimizer, RegimeAwareCVaROptimizer)
            ):
                latest_alpha = alpha_scores.asof(date)
                if isinstance(latest_alpha, pd.DataFrame):
                    latest_alpha = latest_alpha.iloc[-1]

                aligned_alpha, _ = latest_alpha.align(
                    pd.Series(index=lookback_returns.columns), join="right", fill_value=0
                )
                optimizer_kwargs["alpha_scores"] = aligned_alpha

            # --- Run Optimization ---
            opt_result = self.optimizer.optimize(**optimizer_kwargs)

            # --- Store Results ---
            if opt_result and opt_result.status in ["optimal", "optimal_inaccurate"]:
                current_weights = opt_result.weights
                result_dict = {
                    "date": date,
                    "universe": lookback_returns.columns.tolist(),
                    "weights": opt_result.weights,
                    "cvar": opt_result.cvar,
                    "tracking_error": opt_result.tracking_error,
                    "turnover": opt_result.turnover,
                    "n_positions": (opt_result.weights > 1e-4).sum(),
                    "status": opt_result.status,
                }
                logger.info(
                    f"Rebalanced on {date}: CVaR={opt_result.cvar:.4f}, Status={opt_result.status}"
                )
            else:
                status = opt_result.status if opt_result else "failed"
                logger.warning(
                    f"Optimization failed on {date} with status {status}. Holding previous weights."
                )
                result_dict = {
                    "date": date,
                    "universe": lookback_returns.columns.tolist(),
                    "weights": current_weights,
                    "cvar": np.nan,
                    "tracking_error": np.nan,
                    "turnover": 0,
                    "n_positions": (current_weights > 1e-4).sum(),
                    "status": "failed_optimization",
                }
            rebalance_results.append(result_dict)

        if not rebalance_results:
            logger.error("Backtest loop finished but no results were generated.")
            return pd.DataFrame(), pd.Series(dtype=float), pd.DataFrame()

        # 3. Process Results
        rebalance_df = pd.DataFrame(rebalance_results)
        rebalance_df["date"] = pd.to_datetime(rebalance_df["date"])
        rebalance_df.set_index("date", inplace=True)

        # 4. Construct Daily Weights DataFrame
        all_weights_rows = []
        for date, row in rebalance_df.iterrows():
            weights_series = pd.Series(row["weights"], index=row["universe"], name=date)
            all_weights_rows.append(weights_series)

        weights_df = pd.concat(all_weights_rows, axis=1).T.fillna(0.0)

        daily_index = returns.loc[weights_df.index.min() :].index
        daily_weights_df = weights_df.reindex(daily_index, method="ffill").fillna(0.0)

        # 5. Calculate Portfolio Returns with Transaction Costs
        aligned_returns, aligned_weights = returns.align(daily_weights_df, join="inner", axis=0)
        portfolio_returns = (aligned_weights * aligned_returns).sum(axis=1)

        # Deduct transaction costs on rebalance days based on turnover from drifted weights
        rebalance_dates_in_period = rebalance_df.index.intersection(portfolio_returns.index)

        for date in rebalance_dates_in_period:
            loc = aligned_weights.index.get_loc(date)
            if loc == 0:
                # For the first rebalance, turnover is calculated against an initial EW portfolio.
                # This is already handled inside the optimizer. We use that value directly.
                turnover = rebalance_df.loc[date, "turnover"]
            else:
                # For subsequent rebalances, calculate turnover against price-drifted weights
                prev_trading_day = aligned_weights.index[loc - 1]
                weights_before_rebalance = aligned_weights.loc[prev_trading_day]
                returns_on_prev_day = aligned_returns.loc[prev_trading_day]

                # Calculate drifted weights at end of previous day
                drifted_numerator = weights_before_rebalance * (1 + returns_on_prev_day)
                drifted_weights = drifted_numerator / drifted_numerator.sum()

                # Target weights for the current rebalance day
                target_weights = aligned_weights.loc[date]

                # Align and calculate turnover
                aligned_target, aligned_drifted = target_weights.align(
                    drifted_weights, join="outer", fill_value=0.0
                )
                turnover = (aligned_target - aligned_drifted).abs().sum()

            # Deduct transaction costs from the gross return.
            # `turnover` is the sum of absolute changes in weights (i.e., total volume of trades).
            # `transaction_cost` is the per-side cost, so this correctly models the total cost.
            transaction_cost = turnover * self.optimizer.transaction_cost
            portfolio_returns.loc[date] -= transaction_cost
            logger.info(
                f"Applied transaction cost on {date}: {transaction_cost:.4f} (Turnover: {turnover:.2%})"
            )

        rebalance_df.reset_index(inplace=True)

        return rebalance_df, portfolio_returns, daily_weights_df

    def _get_rebalance_dates(self, dates: pd.DatetimeIndex, lookback: int) -> pd.DatetimeIndex:
        """Get rebalancing dates, ensuring enough lookback data exists."""
        # Generate calendar period ends within the data's date range
        resampled_dates = pd.date_range(
            start=dates.min(), end=dates.max(), freq=self.rebalance_frequency
        )

        valid_rebalance_dates: List[pd.Timestamp] = []
        for date in resampled_dates:
            # Find the location of the last trading day on or before the period end.
            # searchsorted finds the insertion point, so -1 gives the prior date's location.
            loc = dates.searchsorted(date, side="right")
            if loc == 0:
                continue

            actual_date_loc = loc - 1

            # Ensure there is enough historical data for the lookback window
            if actual_date_loc >= lookback:
                actual_date = dates[actual_date_loc]
                # Avoid adding duplicate dates if periods are short
                if not valid_rebalance_dates or valid_rebalance_dates[-1] != actual_date:
                    valid_rebalance_dates.append(actual_date)

        return pd.DatetimeIndex(valid_rebalance_dates)


class AlphaAwareCVaROptimizer(CVaROptimizer):
    """
    A CVaR optimizer that incorporates an alpha signal into the objective function.
    """

    def __init__(self, alpha_factor: float = 0.01, **kwargs):
        """
        Initializes the AlphaAwareCVaROptimizer.

        Args:
            alpha_factor (float): The weight to give the alpha signal in the objective function.
                                  A higher value means more emphasis on maximizing alpha.
            **kwargs: Arguments to pass to the base CVaROptimizer.
        """
        super().__init__(**kwargs)
        self.alpha_factor = alpha_factor

    def set_params(
        self,
        alpha: Optional[float] = None,
        lasso_penalty: Optional[float] = None,
        max_weight: Optional[float] = None,
        alpha_factor: Optional[float] = None,
    ):
        """
        Dynamically update optimizer parameters.

        Args:
            alpha (Optional[float]): New confidence level for CVaR.
            lasso_penalty (Optional[float]): New LASSO penalty.
            max_weight (Optional[float]): New maximum weight per asset.
            alpha_factor (Optional[float]): New weight for the alpha signal.
        """
        if alpha is not None:
            self.alpha = alpha
        if lasso_penalty is not None:
            self.lasso_penalty = lasso_penalty
        if max_weight is not None:
            self.max_weight = max_weight
        if alpha_factor is not None:
            self.alpha_factor = alpha_factor

        logger.info(
            f"Optimizer params updated: alpha={self.alpha}, lasso={self.lasso_penalty}, max_w={self.max_weight}, alpha_f={self.alpha_factor}"
        )

    def optimize(
        self,
        returns: pd.DataFrame,
        benchmark_returns: Optional[pd.Series] = None,
        current_weights: Optional[np.ndarray] = None,
        **kwargs,
    ) -> OptimizationResult:
        """
        Optimize portfolio to minimize CVaR and maximize alpha.
        """
        alpha_scores = kwargs.get("alpha_scores")
        if alpha_scores is None:
            raise ValueError("alpha_scores are required for AlphaAwareCVaROptimizer")

        # --- Data Preparation ---
        returns = returns.fillna(0.0)
        if benchmark_returns is not None:
            benchmark_returns = benchmark_returns.fillna(0.0)

        n_assets = returns.shape[1]
        n_scenarios = returns.shape[0]
        R = returns.values
        aligned_alpha = alpha_scores.reindex(returns.columns).fillna(0).values

        if benchmark_returns is None:
            b = returns.mean(axis=1).values
        else:
            b = benchmark_returns.values

        # --- CVXPY Problem Definition ---
        w = cp.Variable(n_assets)
        z = cp.Variable(n_scenarios)
        zeta = cp.Variable()

        tracking_error = (R @ w) - b
        cvar = zeta + (1.0 / ((1 - self.alpha) * n_scenarios)) * cp.sum(z)

        # --- Objective Function Construction ---
        objective_terms = [cvar]
        # Add Alpha Term (negative for maximization)
        objective_terms.append(-self.alpha_factor * (aligned_alpha @ w))

        # Add Lasso Term
        if self.lasso_penalty > 0:
            objective_terms.append(self.lasso_penalty * cp.norm1(w))

        # Add Transaction Cost Term
        if current_weights is not None:
            turnover = cp.sum(cp.abs(w - current_weights))
            objective_terms.append(self.transaction_cost * turnover)

        objective = cp.Minimize(cp.sum(objective_terms))

        # --- Constraints ---
        constraints = [
            z >= 0,
            z >= -tracking_error - zeta,
            cp.sum(w) == 1.0,
            w >= 0,
            w <= self.max_weight,
        ]

        problem = cp.Problem(objective, constraints)

        # --- Solve Problem ---
        try:
            problem.solve(solver=self.solver, verbose=False)
            if problem.status not in ["optimal", "optimal_inaccurate"] or w.value is None:
                logger.warning(f"Solver {self.solver} failed with status: {problem.status}. Trying SCS.")
                problem.solve(solver="SCS", verbose=False, max_iters=5000, eps=1e-4)

            if problem.status not in ["optimal", "optimal_inaccurate"] or w.value is None:
                logger.error(f"Optimization failed with all solvers. Status: {problem.status}")
                return self._get_empty_result(n_assets, status=problem.status)

        except Exception as e:
            logger.error(f"CVXPY solver failed: {e}")
            return self._get_empty_result(n_assets, status="solver_exception")

        # --- Process Results ---
        optimal_weights = w.value
        portfolio_ret_series = R @ optimal_weights
        tracking_err_series = portfolio_ret_series - b
        turnover_val = (
            np.sum(np.abs(optimal_weights - current_weights))
            if current_weights is not None
            else 0.0
        )

        return OptimizationResult(
            weights=optimal_weights,
            cvar=cvar.value,
            portfolio_return=np.mean(portfolio_ret_series),
            portfolio_volatility=np.std(portfolio_ret_series),
            tracking_error=np.std(tracking_err_series),
            turnover=turnover_val,
            status=problem.status,
            solve_time=problem.solver_stats.solve_time or 0.0,
        )


class RegimeAwareCVaROptimizer(CVaROptimizer):
    """Extends the CVaR optimizer to dynamically adjust parameters based on market regime."""

    def __init__(
        self,
        alpha: float = 0.95,
        lasso_penalty: float = 0.01,
        max_weight: float = 0.05,
        solver: str = "ECOS",
        risk_on_params: Optional[Dict[str, float]] = None,
        risk_off_params: Optional[Dict[str, float]] = None,
        **kwargs,
    ):
        """
        Initializes the RegimeAwareCVaROptimizer.

        Args:
            risk_on_params (Dict[str, float]): Parameters for 'risk-on' state.
            risk_off_params (Dict[str, float]): Parameters for 'risk-off' state.
            **kwargs: Base arguments for CVaROptimizer.
        """
        super().__init__(
            alpha=alpha, lasso_penalty=lasso_penalty, max_weight=max_weight, solver=solver, **kwargs
        )
        # Define default 'risk-on' params based on the base initializer
        self.risk_on_params = (
            risk_on_params
            if risk_on_params is not None
            else {"alpha": alpha, "lasso_penalty": lasso_penalty, "max_weight": max_weight}
        )
        # Define more defensive 'risk-off' params
        self.risk_off_params = (
            risk_off_params
            if risk_off_params is not None
            else {"alpha": 0.99, "lasso_penalty": 0.05, "max_weight": 0.03}
        )

        logger.info(
            f"RegimeAwareOptimizer initialized. Risk-On: {self.risk_on_params}, Risk-Off: {self.risk_off_params}"
        )

    def _interpolate_params(self, regime_prob: float) -> Dict[str, float]:
        """Interpolates optimizer parameters based on the regime probability."""
        # regime_prob = 0 -> fully risk-on
        # regime_prob = 1 -> fully risk-off
        interpolated = {}
        for param in self.risk_on_params:
            on_val = self.risk_on_params[param]
            off_val = self.risk_off_params[param]
            # Linear interpolation: start + (end - start) * t
            interp_val = on_val + (off_val - on_val) * regime_prob
            interpolated[param] = interp_val
        return interpolated

    def optimize(
        self,
        returns: pd.DataFrame,
        benchmark_returns: Optional[pd.Series] = None,
        current_weights: Optional[np.ndarray] = None,
        regime_prob: Optional[float] = None,
        alpha_scores: Optional[pd.Series] = None,  # For compatibility
        **kwargs,
    ) -> OptimizationResult:
        """
        Optimize with dynamic parameters based on continuous regime score.
        """
        # Store original parameters to restore after optimization
        original_params = {
            "alpha": self.alpha,
            "lasso_penalty": self.lasso_penalty,
            "max_weight": self.max_weight,
        }

        if regime_prob is not None:
            # Interpolate parameters based on the continuous regime probability
            interpolated_params = self._interpolate_params(regime_prob)

            logger.info(
                f"Regime-adjusted params (prob={regime_prob:.2f}): "
                f"α={interpolated_params['alpha']:.3f}, "
                f"λ={interpolated_params['lasso_penalty']:.4f}, "
                f"max_w={interpolated_params['max_weight']:.3f}"
            )

            # Apply the interpolated parameters for this optimization run
            self.alpha = interpolated_params["alpha"]
            self.lasso_penalty = interpolated_params["lasso_penalty"]
            self.max_weight = interpolated_params["max_weight"]

        try:
            # Call the base class's optimize method with the dynamically adjusted parameters
            return super().optimize(
                returns=returns,
                benchmark_returns=benchmark_returns,
                current_weights=current_weights,
            )
        finally:
            # Restore original parameters to ensure statelessness for the next run
            self.alpha = original_params["alpha"]
            self.lasso_penalty = original_params["lasso_penalty"]
            self.max_weight = original_params["max_weight"]
