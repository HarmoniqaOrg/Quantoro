# src/reporting/utils.py

import pandas as pd


def read_file_content(file_path: str) -> str:
    """Reads the content of a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def format_metrics_table(file_path: str) -> str:
    """Reads a CSV and formats it as a Markdown table."""
    df = pd.read_csv(file_path, index_col=0)
    return df.to_markdown()


def calculate_turnover(daily_weights: pd.DataFrame) -> float:
    """
    Calculates the annualized turnover of a portfolio from its daily weights.

    Args:
        daily_weights (pd.DataFrame): DataFrame of daily portfolio weights,
                                      with dates as index and tickers as columns.

    Returns:
        float: Annualized portfolio turnover.
    """
    if daily_weights is None or daily_weights.empty:
        return 0.0

    # Calculate the absolute difference in weights from one day to the next
    turnover = (daily_weights.shift(1) - daily_weights).abs().sum(axis=1)

    # The total turnover is half the sum of all buys and sells
    daily_turnover = turnover / 2

    # Annualize the turnover
    annualized_turnover = daily_turnover.mean() * 252
    return annualized_turnover


def calculate_turnover_with_drift(
    daily_target_weights: pd.DataFrame, daily_asset_returns: pd.DataFrame
) -> float:
    """
    Calculates annualized turnover accounting for price drift.

    Args:
        daily_target_weights: DataFrame of daily target weights, forward-filled.
        daily_asset_returns: DataFrame of daily returns for each asset.

    Returns:
        Annualized turnover as a float.
    """
    if daily_target_weights.empty or daily_asset_returns.empty:
        return 0.0

    # Align weights and returns to the same dates and columns
    weights, returns = daily_target_weights.align(
        daily_asset_returns, join="inner", axis=0, copy=False
    )
    weights = weights.fillna(0)
    returns = returns.fillna(0)

    # Get weights from previous day (these are the weights at start of the current day)
    w_prev = weights.shift(1).fillna(0)

    # Calculate portfolio return for the denominator of the drift calculation
    portfolio_returns = (w_prev * returns).sum(axis=1)

    # Calculate the value of holdings at end of day, before rebalancing (drifted weights)
    # w_drifted = w_prev * (1 + asset_return) / (1 + portfolio_return)
    drift_denominator = 1 + portfolio_returns
    # Avoid division by zero if portfolio_returns is -1 for a day
    drift_denominator[drift_denominator == 0] = 1e-12

    drift_numerator = w_prev.multiply(1 + returns)
    w_drifted = drift_numerator.div(drift_denominator, axis=0).fillna(0)

    # Trades are the difference between the target weights for today and the drifted weights
    trades = (weights - w_drifted).abs().sum(axis=1)

    # Daily turnover is half the sum of all trades (buys + sells)
    daily_turnover = trades / 2

    # Annualize by multiplying by the number of trading days
    annualized_turnover = daily_turnover.mean() * 252

    return annualized_turnover
