import pandas as pd
import empyrical as ep

def calculate_performance_metrics(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    risk_free_rate: float = 0.0
) -> pd.Series:
    """
    Calculates key performance metrics for a portfolio using the empyrical library.

    Args:
        portfolio_returns (pd.Series): A Series of portfolio returns (daily).
        benchmark_returns (pd.Series): A Series of benchmark returns (daily).
        risk_free_rate (float): The daily risk-free rate of return.

    Returns:
        pd.Series: A series containing the calculated performance metrics.
    """
    # Ensure inputs are pandas Series and are aligned
    if not isinstance(portfolio_returns, pd.Series):
        portfolio_returns = pd.Series(portfolio_returns)
    if not isinstance(benchmark_returns, pd.Series):
        benchmark_returns = pd.Series(benchmark_returns)

    portfolio_returns = portfolio_returns.dropna()
    benchmark_returns = benchmark_returns.reindex(portfolio_returns.index).dropna()

    metrics = pd.Series(name="Performance Metrics", dtype=object)

    # Use empyrical for standard metrics
    metrics['Cumulative Returns'] = ep.cum_returns_final(portfolio_returns)
    metrics['Annual Return'] = ep.annual_return(portfolio_returns)
    metrics['Annual Volatility'] = ep.annual_volatility(portfolio_returns)
    metrics['Sharpe Ratio'] = ep.sharpe_ratio(portfolio_returns, risk_free=risk_free_rate)
    metrics['Max Drawdown'] = ep.max_drawdown(portfolio_returns)
    metrics['Calmar Ratio'] = ep.calmar_ratio(portfolio_returns)
    metrics['Sortino Ratio'] = ep.sortino_ratio(portfolio_returns)

    # Metrics relative to benchmark
    alpha, beta = ep.alpha_beta(portfolio_returns, benchmark_returns)
    metrics['Alpha (annual)'] = alpha
    metrics['Beta'] = beta

    # Information Ratio (Sharpe Ratio of active returns)
    active_returns = portfolio_returns - benchmark_returns
    metrics['Information Ratio'] = ep.sharpe_ratio(active_returns)

    # Other statistical measures
    metrics['Skewness'] = portfolio_returns.skew()
    metrics['Kurtosis'] = portfolio_returns.kurtosis()

    # Format for better readability
    metrics['Cumulative Returns'] = f"{metrics['Cumulative Returns']:.2%}"
    metrics['Annual Return'] = f"{metrics['Annual Return']:.2%}"
    metrics['Annual Volatility'] = f"{metrics['Annual Volatility']:.2%}"
    metrics['Max Drawdown'] = f"{metrics['Max Drawdown']:.2%}"
    metrics['Sharpe Ratio'] = f"{metrics['Sharpe Ratio']:.2f}"
    metrics['Calmar Ratio'] = f"{metrics['Calmar Ratio']:.2f}"
    metrics['Sortino Ratio'] = f"{metrics['Sortino Ratio']:.2f}"
    metrics['Alpha (annual)'] = f"{metrics['Alpha (annual)']:.4f}"
    metrics['Beta'] = f"{metrics['Beta']:.2f}"
    metrics['Information Ratio'] = f"{metrics['Information Ratio']:.2f}"
    metrics['Skewness'] = f"{metrics['Skewness']:.2f}"
    metrics['Kurtosis'] = f"{metrics['Kurtosis']:.2f}"

    return metrics
