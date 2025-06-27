"""
CVaR Portfolio Optimizer
Implements the CLEIR methodology for Task A
"""

import numpy as np
import pandas as pd
import cvxpy as cp
from typing import Tuple, Optional, Dict, List
from dataclasses import dataclass
import logging

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
        transaction_cost: float = 0.001,
        solver: str = 'ECOS'
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

    def optimize(
        self,
        returns: pd.DataFrame,
        benchmark_returns: Optional[pd.Series] = None,
        current_weights: Optional[np.ndarray] = None
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
        n_assets = returns.shape[1]

        def _get_empty_result(status: str = "failed") -> OptimizationResult:
            """Returns an empty OptimizationResult for failed optimizations."""
            return OptimizationResult(
                weights=np.full(n_assets, np.nan),
                cvar=np.nan,
                portfolio_return=np.nan,
                portfolio_volatility=np.nan,
                tracking_error=np.nan,
                turnover=np.nan,
                status=status,
                solve_time=0.0
            )

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
                cp.sum(w) == 1,
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
            problem.solve(solver=self.solver, verbose=False)

            if problem.status not in ["optimal", "optimal_inaccurate"]:
                logger.warning(f"Optimization status: {problem.status}. Returning empty result.")
                return self._get_empty_result(status=problem.status)

            optimal_weights = w.value
            if optimal_weights is None:
                logger.error(f"Opt status is {problem.status}, but weights are None. Returning empty.")
                return self._get_empty_result(status=f"{problem.status}_no_weights")
                
            portfolio_ret_series = R @ optimal_weights
            tracking_err_series = portfolio_ret_series - b.flatten()
            turnover_val = np.sum(np.abs(optimal_weights - current_weights)) if current_weights is not None else 0.0

            result = OptimizationResult(
                weights=optimal_weights,
                cvar=cvar.value,
                portfolio_return=np.mean(portfolio_ret_series),
                portfolio_volatility=np.std(portfolio_ret_series),
                tracking_error=np.std(tracking_err_series),
                turnover=turnover_val,
                status=problem.status,
                solve_time=problem.solver_stats.solve_time or 0.0,
            )

            logger.info(f"Optimization complete: CVaR={result.cvar:.4f}, Status={result.status}")
            return result

        except Exception as e:
            logger.error(f"Optimization failed: {str(e)}")
            return _get_empty_result(status="exception")
    
    def calculate_portfolio_metrics(
        self,
        returns: pd.DataFrame,
        weights: np.ndarray,
        benchmark_returns: Optional[pd.Series] = None
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
            'annual_return': portfolio_returns.mean() * 252,
            'annual_volatility': portfolio_returns.std() * np.sqrt(252),
            'sharpe_ratio': (portfolio_returns.mean() * 252) / (portfolio_returns.std() * np.sqrt(252)),
            'max_drawdown': self._calculate_max_drawdown(portfolio_returns),
            'calmar_ratio': (portfolio_returns.mean() * 252) / abs(self._calculate_max_drawdown(portfolio_returns)),
            'sortino_ratio': self._calculate_sortino_ratio(portfolio_returns),
            'cvar_95': self._calculate_cvar(portfolio_returns, 0.95),
            'cvar_99': self._calculate_cvar(portfolio_returns, 0.99),
        }
        
        # Tracking error metrics if benchmark provided
        if benchmark_returns is not None:
            tracking_error = portfolio_returns - benchmark_returns
            metrics.update({
                'tracking_error': tracking_error.std() * np.sqrt(252),
                'information_ratio': (tracking_error.mean() * 252) / (tracking_error.std() * np.sqrt(252)),
                'beta': portfolio_returns.cov(benchmark_returns) / benchmark_returns.var(),
                'correlation': portfolio_returns.corr(benchmark_returns)
            })
        
        # Weight concentration metrics
        metrics.update({
            'effective_n': 1 / np.sum(weights ** 2),
            'max_weight': np.max(weights),
            'n_positions': np.sum(weights > 0.001),
            'concentration_top5': np.sum(np.sort(weights)[-5:])
        })
        
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
        downside_std = np.sqrt(np.mean(downside_returns ** 2))
        return (returns.mean() * 252) / (downside_std * np.sqrt(252)) if downside_std > 0 else np.inf
    
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
        self,
        optimizer: CVaROptimizer,
        lookback_window: int = 252,
        rebalance_frequency: str = 'Q'
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
            'max_weight': optimizer.max_weight,
            'lasso_penalty': optimizer.lasso_penalty
        }

    def backtest(
        self,
        returns: pd.DataFrame,
        benchmark_returns: pd.Series,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        alpha_scores: Optional[pd.DataFrame] = None,
        regimes: Optional[pd.Series] = None
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Run rolling window backtest.

        Args:
            returns: Full dataset of returns
            benchmark_returns: Benchmark returns
            start_date: Backtest start date
            end_date: Backtest end date

        Returns:
            A tuple containing:
            - DataFrame with backtest rebalance results
            - Series with daily portfolio returns
        """
        # Filter date range
        if start_date:
            returns = returns[returns.index >= start_date]
            benchmark_returns = benchmark_returns[benchmark_returns.index >= start_date]
        if end_date:
            returns = returns[returns.index <= end_date]
            benchmark_returns = benchmark_returns[benchmark_returns.index <= end_date]

        rebalance_dates = self._get_rebalance_dates(returns.index, self.lookback_window)
        
        if rebalance_dates.empty:
            logger.error("No valid rebalance dates found for the given data range and lookback window.")
            return pd.DataFrame(), pd.Series(dtype=float)

        rebalance_results = []
        daily_weights_df = pd.DataFrame(index=returns.index, columns=returns.columns)
        current_weights = np.ones(returns.shape[1]) / returns.shape[1]

        for date in rebalance_dates:
            lookback_end_loc = returns.index.get_loc(date)
            lookback_start_loc = max(0, lookback_end_loc - self.lookback_window)
            
            hist_returns = returns.iloc[lookback_start_loc:lookback_end_loc]
            hist_benchmark = benchmark_returns.iloc[lookback_start_loc:lookback_end_loc]

            # Adjust optimizer parameters based on regime if provided
            if regimes is not None:
                current_regime = regimes.asof(date)
                if current_regime == 0:  # Risk-off
                    logger.info(f"Risk-off regime on {date}. Using defensive parameters.")
                    self.optimizer.max_weight = 0.03  # More defensive
                    self.optimizer.lasso_penalty = self.original_params['lasso_penalty'] * 1.5 # Higher penalty
                else:  # Risk-on or no regime
                    logger.info(f"Risk-on regime on {date}. Using standard parameters.")
                    self.optimizer.max_weight = self.original_params['max_weight']
                    self.optimizer.lasso_penalty = self.original_params['lasso_penalty']

            # Check if the optimizer is alpha-aware and if we have scores
            if isinstance(self.optimizer, AlphaAwareCVaROptimizer) and alpha_scores is not None:
                # Get the latest alpha scores available up to the rebalance date
                latest_alpha_scores = alpha_scores.asof(date)
                if isinstance(latest_alpha_scores, pd.DataFrame): # Handle non-unique index from asof
                    latest_alpha_scores = latest_alpha_scores.iloc[-1]
                
                if latest_alpha_scores.isnull().all():
                    logger.warning(f"No alpha scores found for {date}. Alpha term will be zero.")
                else:
                    logger.info(f"Using alpha scores for optimization on {date}.")
                
                opt_result = self.optimizer.optimize(
                    returns=hist_returns, 
                    alpha_scores=latest_alpha_scores, 
                    benchmark_returns=hist_benchmark, 
                    current_weights=current_weights
                )
            else:
                opt_result = self.optimizer.optimize(hist_returns, hist_benchmark, current_weights)

            if opt_result.status in ["optimal", "optimal_inaccurate"] and opt_result.weights is not None:
                current_weights = opt_result.weights
            else:
                logger.warning(f"Optimization failed on {date} with status {opt_result.status}. Holding previous weights.")
            
            daily_weights_df.loc[date] = current_weights
            
            rebalance_results.append({
                'weights': current_weights,
                'cvar': opt_result.cvar,
                'tracking_error': opt_result.tracking_error,
                'turnover': opt_result.turnover,
                'n_positions': np.sum(current_weights > 0.001) if current_weights is not None else 0,
                'status': opt_result.status
            })
            logger.info(f"Rebalanced on {date}: CVaR={opt_result.cvar:.4f}, Status={opt_result.status}")

        daily_weights_df.ffill(inplace=True)
        daily_weights_df.dropna(inplace=True)

        if daily_weights_df.empty:
            logger.error("Backtest produced no weights. Check rebalance dates and data range.")
            return pd.DataFrame(), pd.Series(dtype=float)
            
        aligned_returns = returns.loc[daily_weights_df.index]
        portfolio_returns = (daily_weights_df * aligned_returns).sum(axis=1)

        results_df = pd.DataFrame(rebalance_results, index=rebalance_dates)

        return results_df, portfolio_returns

    def _get_rebalance_dates(self, dates: pd.DatetimeIndex, lookback: int) -> pd.DatetimeIndex:
        """Get rebalancing dates, ensuring enough lookback data exists."""
        # Generate calendar period ends within the data's date range
        resampled_dates = pd.date_range(
            start=dates.min(), end=dates.max(), freq=self.rebalance_frequency
        )

        valid_rebalance_dates = []
        for date in resampled_dates:
            # Find the location of the last trading day on or before the period end.
            # searchsorted finds the insertion point, so -1 gives the prior date's location.
            loc = dates.searchsorted(date, side='right')
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

    def set_params(self, alpha: Optional[float] = None, lasso_penalty: Optional[float] = None, max_weight: Optional[float] = None, alpha_factor: Optional[float] = None):
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
        
        logger.info(f"Optimizer params updated: alpha={self.alpha}, lasso={self.lasso_penalty}, max_w={self.max_weight}, alpha_f={self.alpha_factor}")

    def optimize(
        self,
        returns: pd.DataFrame,
        alpha_scores: pd.Series,
        benchmark_returns: Optional[pd.Series] = None,
        current_weights: Optional[np.ndarray] = None,
        regime_prob: Optional[float] = None  # Add for compatibility with engine
    ) -> OptimizationResult:
        """
        Optimize portfolio to minimize CVaR and maximize alpha.
        """
        n_assets = returns.shape[1]
        n_scenarios = returns.shape[0]

        R = returns.values
        
        # Ensure all inputs are explicit 2D column vectors to avoid shape ambiguity
        aligned_alpha = alpha_scores.reindex(returns.columns).fillna(0).values.reshape(-1, 1)

        if benchmark_returns is None:
            b = returns.mean(axis=1).values.reshape(-1, 1)
        elif hasattr(benchmark_returns, 'values'):
            b = benchmark_returns.values.reshape(-1, 1)
        else:
            b = np.asarray(benchmark_returns).reshape(-1, 1)
        
        # Define CVXPY variables as explicit 2D column vectors
        w = cp.Variable((n_assets, 1))
        z = cp.Variable((n_scenarios, 1))
        zeta = cp.Variable()

        tracking_error = cp.matmul(R, w) - b
        cvar = zeta + (1.0 / ((1 - self.alpha) * n_scenarios)) * cp.sum(z)
        
        # Use transpose for dot product with column vectors and sum the resulting (1,1) matrix to ensure it's a scalar expression
        portfolio_alpha = cp.sum(cp.matmul(w.T, aligned_alpha)) 

        # Construct the objective function additively to create a simpler expression tree for the solver
        objective = cvar - self.alpha_factor * portfolio_alpha
        if self.lasso_penalty > 0:
            objective += self.lasso_penalty * cp.norm1(w)
        if current_weights is not None:
            current_weights_col = current_weights.reshape(-1, 1)
            turnover = cp.sum(cp.abs(w - current_weights_col))
            objective += self.transaction_cost * turnover

        objective = cp.Minimize(objective)

        # Use the simpler, more robust constraint formulation from the base class
        constraints = [
            z >= 0,
            z >= -tracking_error - zeta,
            cp.sum(w) == 1,
            w >= 0,
            w <= self.max_weight,
        ]

        problem = cp.Problem(objective, constraints)
        problem.solve(solver=self.solver, verbose=False)

        if problem.status not in ["optimal", "optimal_inaccurate"] or w.value is None:
            logger.warning(f"Optimization failed or weights are None. Status: {problem.status}")
            return OptimizationResult(
                weights=np.full(n_assets, np.nan), status=problem.status, cvar=np.nan,
                portfolio_return=np.nan, portfolio_volatility=np.nan, tracking_error=np.nan, turnover=np.nan, solve_time=0.0
            )

        optimal_weights = w.value.flatten() # Flatten for consistency in output
        portfolio_ret_series = R @ optimal_weights
        tracking_err_series = portfolio_ret_series - b.flatten()

        if current_weights is not None:
            turnover_val = np.sum(np.abs(optimal_weights - current_weights))
        else:
            turnover_val = 0.0
            
        solve_time = problem.solver_stats.solve_time if hasattr(problem, 'solver_stats') and hasattr(problem.solver_stats, 'solve_time') else 0.0

        return OptimizationResult(
            weights=optimal_weights,
            status=problem.status,
            cvar=cvar.value,
            portfolio_return=np.mean(portfolio_ret_series),
            portfolio_volatility=np.std(portfolio_ret_series),
            tracking_error=np.std(tracking_err_series),
            turnover=turnover_val,
            solve_time=solve_time
        )


class RegimeAwareCVaROptimizer(CVaROptimizer):
    """Extends the CVaR optimizer to dynamically adjust parameters based on market regime."""

    def __init__(
        self,
        alpha: float = 0.95,
        lasso_penalty: float = 0.01,
        max_weight: float = 0.05,
        risk_on_params: Optional[Dict[str, float]] = None,
        risk_off_params: Optional[Dict[str, float]] = None,
        **kwargs
    ):
        """
        Initializes the RegimeAwareCVaROptimizer.

        Args:
            risk_on_params (Dict[str, float]): Parameters for 'risk-on' state.
            risk_off_params (Dict[str, float]): Parameters for 'risk-off' state.
            **kwargs: Base arguments for CVaROptimizer.
        """
        super().__init__(
            alpha=alpha,
            lasso_penalty=lasso_penalty,
            max_weight=max_weight,
            **kwargs
        )
        # Define default 'risk-on' params based on the base initializer
        self.risk_on_params = risk_on_params if risk_on_params is not None else {
            'alpha': alpha,
            'lasso_penalty': lasso_penalty,
            'max_weight': max_weight
        }
        # Define more defensive 'risk-off' params
        self.risk_off_params = risk_off_params if risk_off_params is not None else {
            'alpha': 0.99, 'lasso_penalty': 0.05, 'max_weight': 0.03
        }
        
        logger.info(f"RegimeAwareOptimizer initialized. Risk-On: {self.risk_on_params}, Risk-Off: {self.risk_off_params}")

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
        alpha_scores: Optional[pd.Series] = None # For compatibility
    ) -> OptimizationResult:
        """
        Optimize with dynamic parameters based on continuous regime score.
        """
        # Store original parameters to restore after optimization
        original_params = {
            'alpha': self.alpha,
            'lasso_penalty': self.lasso_penalty,
            'max_weight': self.max_weight
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
            self.alpha = interpolated_params['alpha']
            self.lasso_penalty = interpolated_params['lasso_penalty']
            self.max_weight = interpolated_params['max_weight']
        
        try:
            # Call the base class's optimize method with the dynamically adjusted parameters
            return super().optimize(
                returns=returns,
                benchmark_returns=benchmark_returns,
                current_weights=current_weights
            )
        finally:
            # Restore original parameters to ensure statelessness for the next run
            self.alpha = original_params['alpha']
            self.lasso_penalty = original_params['lasso_penalty']
            self.max_weight = original_params['max_weight']
