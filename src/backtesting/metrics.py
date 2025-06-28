import pandas as pd
import numpy as np
import empyrical as ep
from typing import Callable, Tuple
import os
import logging


def bootstrap_metric(
    returns: pd.Series,
    metric_func: Callable,
    n_bootstrap: int = 1000,
    alpha: float = 0.05,
    **kwargs,
) -> Tuple[float, float]:
    """
    Calculates confidence intervals for a given performance metric using bootstrapping.

    Args:
        returns (pd.Series): A Series of portfolio returns.
        metric_func (callable): The function to calculate the metric (e.g., ep.annual_return).
        n_bootstrap (int): The number of bootstrap samples to generate.
        alpha (float): The significance level for the confidence interval.
        **kwargs: Additional keyword arguments to pass to the metric function.

    Returns:
        tuple: A tuple containing the lower and upper bounds of the confidence interval.
    """
    bootstrapped_metrics = []
    for _ in range(n_bootstrap):
        resampled_returns = returns.sample(n=len(returns), replace=True)
        metric_value = metric_func(resampled_returns, **kwargs)
        bootstrapped_metrics.append(metric_value)

    lower_bound = np.percentile(bootstrapped_metrics, (alpha / 2) * 100)
    upper_bound = np.percentile(bootstrapped_metrics, (1 - alpha / 2) * 100)

    return lower_bound, upper_bound


def calculate_annual_turnover(daily_weights: pd.DataFrame) -> float:
    """
    Calculates the annualized portfolio turnover from daily weights.
    Turnover is defined as half the sum of absolute changes in weights, annualized.
    """
    if daily_weights is None or daily_weights.empty:
        return 0.0
    # The daily turnover is half the sum of absolute changes in weights
    daily_turnover = 0.5 * daily_weights.diff().abs().sum(axis=1)
    # Annualize by taking the mean daily turnover and multiplying by 252
    annualized_turnover = daily_turnover.mean() * 252
    return annualized_turnover


def calculate_raw_metrics(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    daily_weights: pd.DataFrame = None,
    risk_free_rate: float = 0.0,
) -> pd.Series:
    """Calculates key performance metrics and returns them as raw numbers."""
    if not isinstance(portfolio_returns, pd.Series):
        portfolio_returns = pd.Series(portfolio_returns)
    if not isinstance(benchmark_returns, pd.Series):
        benchmark_returns = pd.Series(benchmark_returns)

    portfolio_returns = portfolio_returns.dropna()
    benchmark_returns = benchmark_returns.reindex(portfolio_returns.index).dropna()

    metrics = pd.Series(name="Performance Metrics", dtype=np.float64)

    total_return = (1 + portfolio_returns).prod() - 1
    metrics["Cumulative Returns"] = total_return

    n_years = len(portfolio_returns) / 252.0
    if n_years == 0:
        metrics["Annual Return"] = 0
    else:
        metrics["Annual Return"] = (1 + total_return) ** (1 / n_years) - 1

    metrics["Annual Volatility"] = ep.annual_volatility(portfolio_returns)
    metrics["Sharpe Ratio"] = ep.sharpe_ratio(portfolio_returns, risk_free=risk_free_rate)
    metrics["Max Drawdown"] = ep.max_drawdown(portfolio_returns)
    metrics["Calmar Ratio"] = ep.calmar_ratio(portfolio_returns)
    metrics["Sortino Ratio"] = ep.sortino_ratio(portfolio_returns)
    metrics["95% CVaR"] = ep.conditional_value_at_risk(portfolio_returns, 0.95)

    if daily_weights is not None:
        metrics["Annual Turnover"] = calculate_annual_turnover(daily_weights)
    else:
        metrics["Annual Turnover"] = np.nan

    alpha_val, beta_val = ep.alpha_beta(portfolio_returns, benchmark_returns)
    metrics["Alpha (annual)"] = alpha_val
    metrics["Beta"] = beta_val
    metrics["Information Ratio"] = ep.sharpe_ratio(portfolio_returns - benchmark_returns)
    metrics["Skewness"] = portfolio_returns.skew()
    metrics["Kurtosis"] = portfolio_returns.kurtosis()

    return metrics


def format_metrics_for_display(
    raw_metrics: pd.Series,
    portfolio_returns: pd.Series,
    confidence_level: float = 0.95,
    risk_free_rate: float = 0.0,
) -> pd.Series:
    """Formats raw metrics for console display, adding confidence intervals."""
    display_metrics = raw_metrics.copy().astype(object)

    alpha = 1 - confidence_level
    ar_lower, ar_upper = bootstrap_metric(portfolio_returns, ep.annual_return, alpha=alpha)
    sr_lower, sr_upper = bootstrap_metric(
        portfolio_returns, ep.sharpe_ratio, alpha=alpha, risk_free=risk_free_rate
    )

    display_metrics["Cumulative Returns"] = f"{raw_metrics['Cumulative Returns']:.2%}"
    display_metrics[
        "Annual Return"
    ] = f"{raw_metrics['Annual Return']:.2%} ({ar_lower:.2%} - {ar_upper:.2%})"
    display_metrics["Annual Volatility"] = f"{raw_metrics['Annual Volatility']:.2%}"
    display_metrics["Max Drawdown"] = f"{raw_metrics['Max Drawdown']:.2%}"
    display_metrics[
        "Sharpe Ratio"
    ] = f"{raw_metrics['Sharpe Ratio']:.2f} ({sr_lower:.2f} - {sr_upper:.2f})"
    display_metrics["Calmar Ratio"] = f"{raw_metrics['Calmar Ratio']:.2f}"
    display_metrics["Sortino Ratio"] = f"{raw_metrics['Sortino Ratio']:.2f}"
    display_metrics["Alpha (annual)"] = f"{raw_metrics['Alpha (annual)']:.4f}"
    display_metrics["Beta"] = f"{raw_metrics['Beta']:.2f}"
    display_metrics["Information Ratio"] = f"{raw_metrics['Information Ratio']:.2f}"
    display_metrics["Skewness"] = f"{raw_metrics['Skewness']:.2f}"
    display_metrics["Kurtosis"] = f"{raw_metrics['Kurtosis']:.2f}"

    return display_metrics


def update_consolidated_returns(new_returns: pd.Series, strategy_name: str, output_path: str):
    """
    Loads a consolidated daily returns CSV, adds or updates a strategy's returns,
    and saves it back.
    """
    try:
        if os.path.exists(output_path):
            consolidated_returns = pd.read_csv(output_path, index_col="date", parse_dates=True)
        else:
            consolidated_returns = pd.DataFrame()

        consolidated_returns[strategy_name] = new_returns
        consolidated_returns.to_csv(output_path)
        logging.info(f"Successfully updated consolidated returns file: {output_path}")
    except Exception as e:
        logging.error(f"Failed to update consolidated returns file: {e}")
