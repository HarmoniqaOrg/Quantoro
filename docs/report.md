--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
## Final Report: Advanced CVaR Portfolio Optimization

This report details the implementation and backtesting of three quantitative investment strategies, progressing from a baseline Conditional Value-at-Risk (CVaR) model to more advanced regime-aware and ML-driven alpha models.

### Task A: Baseline CVaR Optimization

This task implemented the baseline CVaR optimization strategy. The model optimizes a long-only portfolio of 60 liquid US stocks, minimizing the 95% daily CVaR. The portfolio is rebalanced quarterly with a 10 bps transaction cost.

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
