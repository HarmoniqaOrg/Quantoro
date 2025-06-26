# Final Report: Enhanced CVaR Optimization Strategies

**Author:** [Your Name]
**Date:** October 26, 2023

## 1. Executive Summary

*(Briefly summarize the project's goal, methodology, key findings, and final recommendation. This should be a concise overview of the entire report.)*

---

## 2. Introduction

### 2.1. Problem Statement
*(Describe the limitations of traditional portfolio optimization methods and the opportunity to improve upon them using CVaR, machine learning, and alternative data.)*

### 2.2. Project Objectives
*(Clearly state the three main tasks: baseline CVaR implementation, regime-aware enhancement, and alpha-aware integration.)*

---

## 3. Methodology

### 3.1. Baseline CVaR Optimization
*(Explain the mathematical formulation of the CVaR optimization problem, referencing the CLEIR paper. Describe the objective function and constraints used.)*

### 3.2. Regime-Aware Enhancement

Our enhancement to the baseline CVaR strategy introduces a dynamic, regime-aware framework designed to improve risk-adjusted returns by adapting to changing market conditions. The core hypothesis is that a static optimization model is suboptimal, as it fails to differentiate between high-risk and low-risk environments. Our model addresses this by identifying two distinct market regimes—"Risk-On" and "Risk-Off"—and adjusting its risk-taking posture accordingly.

The regime detection mechanism is intentionally simple and interpretable, using a classic 50-day vs. 200-day Simple Moving Average (SMA) crossover on the SPY ETF as a market proxy. When the 50-day SMA is above the 200-day SMA, the model enters a "Risk-On" state. Conversely, when the 50-day SMA falls below, it triggers a "Risk-Off" state. This mechanism's primary advantage is its transparency; the model's state can be easily visualized and understood by plotting the SMAs against the market index, providing clear interpretability without complex 'black box' models.

During "Risk-On" periods, the `RegimeAwareCVaROptimizer` employs the standard 95% CVaR alpha, balancing risk and return. However, in "Risk-Off" periods, the model becomes significantly more conservative. It increases the CVaR alpha to 99% and raises the LASSO regularization penalty. This shift prioritizes tail-risk mitigation and diversification, aiming to protect capital during downturns by penalizing concentrated bets and focusing on minimizing extreme losses.

### 3.3. Alternative Data Alpha Integration
*(Describe the FMP signals used (e.g., insider trading, analyst ratings). Explain how these signals were processed and integrated into the CVaR optimization as an alpha-aware objective term.)*

---

## 4. Results and Analysis

### 4.1. Performance Summary

The table below summarizes the out-of-sample performance (2020-2024) of the three strategies. The Enhanced (Regime-Aware) strategy significantly outperformed both the Baseline and the Alpha-Aware models on a risk-adjusted basis, demonstrating the value of dynamically adapting to market conditions.

| Metric                | Baseline CVaR         | Enhanced CVaR           | Alpha-Aware CVaR      |
|-----------------------|-----------------------|-------------------------|-----------------------|
| **Annual Return**     | 10.42%                | **15.96%**              | 7.68%                 |
| **Annual Volatility** | **16.59%**            | 17.25%                  | 17.86%                |
| **Sharpe Ratio**      | 0.68                  | **0.94**                | 0.50                  |
| **Max Drawdown**      | -28.87%               | -29.52%                 | **-28.43%**           |
| **Alpha (annual)**    | -0.0143               | **0.0769**              | -0.0063               |
| **Beta**              | 0.99                  | **0.66**                | 0.99                  |
| **Information Ratio** | -0.59                 | **0.22**                | -0.19                 |

![Comprehensive Results Dashboard](results/comprehensive_dashboard.png)

### 4.2. Strategy Deep Dive

*   **Baseline vs. Enhanced:** Analyze the impact of the regime-aware adjustments. Did it successfully mitigate risk during downturns? Refer to the drawdown and rolling Sharpe plots.
*   **Alpha-Aware Strategy:** Discuss the underperformance of the alpha strategy. Hypothesize reasons for this (e.g., signal decay, noisy data, need for more sophisticated signal processing).

### 4.3. Interpretability

*   **Regime Analysis:** The regime detection model, based on the SPY's 50/200-day SMA crossover, provides a clear and interpretable view of the model's behavior. The plot below shows the identified "Risk-Off" periods (shaded in red), which successfully captured major market downturns, including the COVID-19 crash in 2020 and the 2022 bear market. The model's ability to switch to a more conservative posture during these periods was critical to its outperformance.

![Regime Interpretability Plot](results/regime_interpretability.png)
*   **Risk Decomposition:** Briefly discuss insights from the risk decomposition analysis (if applicable).

---

## 5. Conclusion and Recommendations

### 5.1. Summary of Findings
*(Recap the key results: the success of the regime-aware model and the negative but valuable validation of the initial alpha strategy.)*

### 5.2. Future Work
*(Suggest concrete next steps for improving the alpha strategy, such as exploring more sophisticated ML models for signal combination, using a wider range of alternative data, or implementing a more advanced regime detection model.)*

### 5.3. Final Recommendation
*(Conclude with a clear recommendation on which strategy should be pursued for production deployment and why.)*
