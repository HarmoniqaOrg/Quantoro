# Task B: SMA Crossover Model Interpretability Report

## 1. Introduction

This report provides an analysis of the regime-aware enhancement for the CVaR optimization strategy. The goal is to interpret the behavior of the Simple Moving Average (SMA) Crossover model used for regime detection and understand how the portfolio strategy adapts to different market conditions.

## 2. Regime Detection Model

- **Model Choice**: 50-day vs. 200-day SMA Crossover on the SPY ETF.
- **Signal**: 'Risk-On' (Regime 1) is signaled when the 50-day SMA is above the 200-day SMA. 'Risk-Off' (Regime 0) is signaled otherwise.
- **Interpretability**: This model is highly transparent. The regime is determined by a clear, verifiable market signal, avoiding 'black box' complexity.

## 3. Regime Timeline Visualization

The following plot visually confirms the model's behavior. 'Risk-Off' periods (shaded in red) align with notable market downturns, such as the COVID-19 crash in early 2020 and the market instability throughout 2022, validating the signal's effectiveness.

![Regime Analysis Plot](..\results\img\regime_analysis_plot.png)

## 4. Adaptive Portfolio Strategy

The core of the enhanced strategy is its ability to adapt its risk posture based on the detected regime:

- **During Risk-Off Regimes**: The optimizer adopts a more defensive stance to preserve capital.
  - `cvar_alpha`: Increased to 0.99 (more risk-averse).
  - `lasso_penalty`: Reduced to 0.5 (encourages more diversification).
  - `max_weight`: Reduced to 0.04 (prevents concentration).
- **During Risk-On Regimes**: The optimizer uses a more aggressive stance to pursue growth.
  - `cvar_alpha`: Standard 0.95.
  - `lasso_penalty`: Increased to 2.0 (encourages concentration in high-conviction assets).
  - `max_weight`: Standard 0.05.

This dynamic adjustment is the key to the strategy's improved risk-adjusted performance.

## 5. Conclusion

The SMA Crossover model provides a simple yet effective signal for switching between risk-on and risk-off portfolio strategies. Its clear interpretability and proven alignment with major market shifts make it a robust foundation for the enhanced CVaR optimization.
