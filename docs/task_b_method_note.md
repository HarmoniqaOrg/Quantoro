# Method Note: Regime-Aware CVaR Enhancement (Task B)

## Objective

The primary objective of the Task B enhancement was to improve upon the baseline CVaR optimization strategy by making it adaptive to changing market conditions. The hypothesis was that by identifying distinct market regimes—specifically "risk-on" and "risk-off" periods—we could dynamically adjust the portfolio optimization to improve risk-adjusted returns.

## Methodology

To achieve this, we implemented a simple yet widely recognized technical indicator: the Simple Moving Average (SMA) crossover. This method serves as a robust proxy for market trend and momentum, which are key drivers of market regimes.

-   **Regime Definition**: We used two SMAs on a broad market index (S&P 500 proxy):
    -   A **short-term 50-day SMA** to capture recent price momentum.
    -   A **long-term 200-day SMA** to represent the established, underlying trend.

-   **Signal Generation**:
    -   A **"Risk-On"** regime is signaled when the 50-day SMA crosses above the 200-day SMA. This typically corresponds to a bullish market uptrend.
    -   A **"Risk-Off"** regime is signaled when the 50-day SMA crosses below the 200-day SMA, indicating a bearish market downtrend.

## Implementation and Integration

The `RegimeDetector` class was implemented to encapsulate this logic. It takes a time series of market prices and returns a corresponding series of binary regime signals (1 for risk-on, 0 for risk-off).

These signals were then integrated into the `RollingCVaROptimizer`. The backtesting engine was designed to use these regime signals to switch between different portfolio construction parameters. For the enhanced strategy, during "risk-off" periods, the optimization constraints were tightened to favor a more defensive posture, such as lowering the maximum allowable weight for any single asset. This allows the portfolio to systematically reduce risk when the market trend is unfavorable and seek higher returns when the trend is positive.

## Conclusion

This enhancement provides a clear, interpretable, and rules-based framework for adapting the CVaR portfolio to macroeconomic trends. The generated interpretability plot visually confirms the model's behavior, showing how the identified regimes correspond to major market movements. The backtest results for the enhanced strategy demonstrated an improvement in the Sharpe Ratio, validating the effectiveness of this approach.
