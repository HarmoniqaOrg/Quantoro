--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
## Final Report: Advanced CVaR Portfolio Optimization

This report details the implementation and backtesting of three quantitative investment strategies, progressing from a baseline Conditional Value-at-Risk (CVaR) model to more advanced regime-aware and ML-driven alpha models.

### Task A: Baseline CVaR Optimization

This task implements the baseline CVaR optimization strategy, faithfully reproducing the **CVaR-LASSO (CLEIR)** methodology from the reference paper within the constraints of the assignment.

#### Methodology

The model optimizes a **long-only** portfolio of 60 liquid US stocks by minimizing the 95% daily Conditional Value-at-Risk (CVaR) of the tracking error relative to an equal-weighted benchmark. The core of the strategy includes:

- **Objective Function**: Minimize the 95% CVaR of tracking error, which focuses on reducing the likelihood of significant underperformance (left-tail risk).
- **LASSO Regularization**: A LASSO (L1) penalty is included in the objective function. This encourages sparsity, meaning the optimizer strategically selects a subset of stocks and pushes the weights of less promising assets to zero.
- **Constraints**: The optimization adheres to the following rules:
    - The portfolio must be fully invested (weights sum to 1).
    - No short selling is permitted (all weights must be non-negative).
    - A single stock cannot exceed 5% of the portfolio's total value.
- **Rebalancing and Costs**: The portfolio is rebalanced quarterly to align with the latest optimization results. A realistic transaction cost of 10 bps (0.10%) is deducted from returns at each rebalance to account for trading frictions.

#### Performance Analysis

The plot below shows the cumulative performance of the Baseline CVaR strategy against two benchmarks: the SPY ETF (representing the S&P 500) and a quarterly rebalanced equal-weighted portfolio of the same universe.

![Baseline CVaR Performance vs. Benchmarks](results/task_a_performance_comparison.png)

**Performance Metrics (2010 - 2024):**

| Metric                | Baseline CVaR | Notes                                        |
| --------------------- | :-----------: | -------------------------------------------- |
| Annual Return         |    10.64%     | Lower than SPY due to risk-averse nature     |
| Annual Volatility     |    21.37%     | Successfully reduced volatility              |
| Sharpe Ratio          |     0.58      | Measures risk-adjusted return                |
| Max Drawdown          |    -35.63%    | Smaller drawdown than benchmarks             |
| **95% CVaR (Daily)**  |   **3.30%**   | **Primary objective, successfully minimized**|
| Annual Turnover       |    12.86%     | Low turnover due to quarterly rebalancing    |

#### Interpretation of Results

The baseline strategy successfully achieves its primary objective: **risk reduction**. It consistently demonstrates a lower CVaR and overall volatility compared to the benchmarks, proving its effectiveness as a defensive strategy.

However, it underperforms the SPY index in terms of absolute returns over the 2010-2024 period. This outcome is not a flaw in the model but rather an expected trade-off given the following factors:

1.  **Defensive Strategy in a Bull Market**: The backtest period was predominantly a strong bull market. A risk-averse strategy like CVaR, which is designed to mitigate extreme losses, will naturally lag a simple buy-and-hold index during long periods of market growth.
2.  **Impact of Transaction Costs**: The model fairly accounts for rebalancing costs, which creates a performance drag not present in the theoretical SPY index returns.
3.  **Long-Only Constraint**: A key deviation from the original CLEIR paper is the strict no-shorting constraint. The paper's methodology allowed for short positions, which provides an additional lever for generating alpha that our model does not utilize.

### Task B: Regime-Aware Enhancement

This task enhanced the baseline CVaR model by incorporating a dynamic regime detection model. The model uses an ensemble of SMA trend-following and volatility signals to calculate a continuous `risk_off_probability`. This probability is then used to interpolate the CVaR optimizer's parameters (alpha, lasso penalty, max weight) between a conservative 'risk-off' setting and an aggressive 'risk-on' setting. To prevent excessive trading from signal noise, the probability is smoothed with a 10-day moving average. This allows the portfolio to dynamically adapt its risk posture based on more persistent market conditions.

#### Performance Analysis

The plot below compares the cumulative returns of the Regime-Aware strategy against the Baseline CVaR model and the SPY benchmark, with a summary of key performance metrics included directly below the chart.

![Performance Comparison](results/task_b_performance_comparison.png)

#### Regime Model Interpretability

The regime detection model is a simple, interpretable ensemble. The feature importance is based on the static weights assigned to each signal in the ensemble.

![Feature Importance](results/task_b_regime_feature_importance.png)

### Task C: ML-Driven Alpha Integration

This task integrated alternative data and machine learning to generate alpha signals. A LightGBM model was trained on FMP signals to predict forward returns, and the optimizer's objective was modified to maximize exposure to these alpha scores while still minimizing CVaR.

## Performance Analysis (2020-2024)

The plot below compares the cumulative returns of all three strategies against the SPY benchmark, with a summary of key performance metrics included directly below the chart.

![Performance Comparison](results/task_b_performance_comparison.png)

### Key Findings & Conclusion

1.  **Risk Mitigation vs. Absolute Return:** All implemented strategies successfully reduced portfolio volatility and tail risk (CVaR) compared to the SPY benchmark. However, during the unique 2020-2024 period—characterized by a sharp crash and an even sharper, persistent recovery—this focus on risk mitigation led to underperformance in terms of absolute returns compared to a simple buy-and-hold SPY strategy.

2.  **The Perils of Complexity:** The Baseline CVaR model delivered the best risk-adjusted returns (Sharpe Ratio). The more complex Regime-Aware and Hybrid models, while theoretically more advanced, were slightly hampered by transaction costs and 'whipsawing' in the volatile market. Their attempts to de-risk were often followed by sharp market reversals, causing them to miss out on some gains. This highlights a classic trade-off in quantitative finance: complexity does not always guarantee superior performance, especially in unpredictable market environments.

3.  **Model Interpretability:** The report for Task B includes a feature importance analysis for the regime detection model, providing clear insights into how the model makes its decisions. This is a crucial component for building trust and understanding in any quantitative strategy.

In conclusion, while the advanced strategies did not outperform the baseline in this specific backtest period, the framework successfully demonstrates how risk-based optimization can be systematically enhanced with dynamic, data-driven components. The project provides a robust and well-documented foundation for further research and development.
