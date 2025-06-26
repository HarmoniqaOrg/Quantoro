# Task B: Regime-Aware Model Interpretability Report

## 1. Introduction

This report provides an analysis of the regime-aware enhancement for the CVaR optimization strategy. The goal is to interpret the behavior of the Hidden Markov Model (HMM) used for regime detection and understand how the portfolio strategy adapts to different market conditions as identified by the model.

## 2. Regime Detection Model

- **Model Choice**: Gaussian Hidden Markov Model (HMM).
- **Features Used**: Rolling 22-day volatility of the S&P 500 (SPY).
- **Number of Regimes**: 2 (interpreted as 'Risk-On' and 'Risk-Off').

## 3. Analysis of Detected Regimes

The analysis of the backtest period (2020-2024) reveals distinct characteristics for each regime:

| Regime      | Interpretation | Annualized Volatility | Annualized Return | Days in Regime |
|-------------|----------------|-----------------------|-------------------|----------------|
| **Regime 0**| Risk-Off       | 25.97%                | 15.36%            | 283            |
| **Regime 1**| Risk-On        | 19.33%                | 15.62%            | 974            |

The key differentiator identified by the model is **volatility**. The 'Risk-Off' regime exhibits significantly higher market turbulence. Interestingly, the annualized returns are comparable across both regimes, indicating the model effectively separates periods of high risk from periods of stable growth.

### Regime Timeline Visualization

The following plot visually confirms the model's behavior. 'Risk-Off' periods (shaded in red) align with notable market downturns and spikes in volatility, such as the COVID-19 crash in early 2020 and the market instability throughout 2022.

![Regime Analysis Plot](..\results\img\regime_analysis_plot.png)


## 4. Adaptive Portfolio Strategy

The core of the enhanced strategy is its ability to adapt its risk posture based on the detected regime:

- **During Risk-Off Regimes**: The optimizer adopts a more defensive stance.
  - `max_weight`: Reduced to 3%.
  - `lasso_penalty`: Increased by 50%.
- **During Risk-On Regimes**: The optimizer uses the standard, less restrictive parameters.
  - `max_weight`: 5%.
  - `lasso_penalty`: Standard value.

This dynamic adjustment aims to protect capital during turbulent periods while allowing for more aggressive positioning during stable times.

## 5. Performance Attribution by Regime

*(This section will analyze the strategy's performance within each regime to validate the adaptive approach)*

## 6. Conclusion

Summary of findings on the model's effectiveness and interpretability.
