### Task B Enhancement: Regime-Aware CVaR Optimization

Our enhancement to the baseline CVaR strategy introduces a dynamic, regime-aware framework designed to improve risk-adjusted returns by adapting to changing market conditions. The core hypothesis is that a static optimization model is suboptimal, as it fails to differentiate between high-risk and low-risk environments. Our model addresses this by identifying two distinct market regimes—"Risk-On" and "Risk-Off"—and adjusting its risk-taking posture accordingly.

**Methodology & Interpretability**

The regime detection mechanism is intentionally simple and interpretable, using a classic 50-day vs. 200-day Simple Moving Average (SMA) crossover on the SPY ETF as a market proxy. When the 50-day SMA is above the 200-day SMA, the model enters a "Risk-On" state. Conversely, when the 50-day SMA falls below, it triggers a "Risk-Off" state. This mechanism's primary advantage is its transparency; the model's state can be easily visualized and understood by plotting the SMAs against the market index, providing clear interpretability without complex 'black box' models.

During "Risk-On" periods, the `RegimeAwareCVaROptimizer` employs the standard 95% CVaR alpha, balancing risk and return. However, in "Risk-Off" periods, the model becomes significantly more conservative. It increases the CVaR alpha to 99% and raises the LASSO regularization penalty. This shift prioritizes tail-risk mitigation and diversification, aiming to protect capital during downturns by penalizing concentrated bets and focusing on minimizing extreme losses.

**Results & Conclusion**

The out-of-sample backtest from 2020-2024 demonstrates the value of this adaptive approach. As shown in the consolidated performance dashboard, the Enhanced CVaR strategy delivered a superior Sharpe Ratio (0.94) compared to the Baseline (0.68). It achieved a higher annualized return (15.96% vs. 10.42%) with only a marginal increase in volatility. The positive alpha and Information Ratio further confirm that the regime-switching logic added significant value beyond the benchmark.

In conclusion, by dynamically adjusting its risk parameters based on a clear, interpretable market signal, the regime-aware model successfully navigated the volatile 2020-2024 period, outperforming its static counterpart on a risk-adjusted basis.
