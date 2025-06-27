# Task C: ML Alpha Model - Interpretability Report Framework

## 1. Objective
This document outlines the methodology for interpreting the predictions of the `MLAlphaModel` and understanding the key drivers of the final portfolio construction. The goal is to move beyond a "black box" approach and gain actionable insights into the model's behavior. The primary tool for this analysis will be **SHAP (SHapley Additive exPlanations)**, a game-theoretic approach to explaining the output of any machine learning model.

## 2. Proposed Interpretability Techniques

### a. Global Model Interpretation: What does the model look for?
- **Technique**: Aggregate SHAP Feature Importance.
- **Implementation**: After each model retraining (at every rebalancing date), calculate the mean absolute SHAP value for each feature across the entire training dataset. These values will be logged.
- **Analysis**: By aggregating these importance scores over the full backtest period, we can identify which features are the most influential drivers of alpha predictions *on average*. This provides a high-level understanding of the model's core logic.

### b. Local Prediction Interpretation: Why was a specific stock picked?
- **Technique**: Individual SHAP Force Plots.
- **Implementation**: For specific dates of interest (e.g., a major market turn), we can select a few key stocks (e.g., the highest and lowest alpha-ranked stocks) and generate SHAP force plots for their predictions.
- **Analysis**: A force plot decomposes a single prediction, showing how each feature contributed to pushing the alpha score higher or lower. This allows for a granular analysis, answering questions like, "Why did the model strongly favor Apple on this date?"

### c. Regime-Conditional Feature Importance
- **Technique**: Segmented SHAP Analysis.
- **Implementation**: Group the logged feature importance scores by the market regime ("risk-on" vs. "risk-off") that was active at the time of prediction.
- **Analysis**: This powerful technique can reveal if the model's logic adapts to market conditions. For example, we might discover that momentum features are highly ranked during "risk-on" periods, while value-based FMP signals become more important during "risk-off" periods.

---
***Note on Current Implementation***: *The feature engineering pipeline in the final backtest script currently uses simulated random data. This was a deliberate choice to isolate and debug the complex optimization engine. The interpretability framework outlined above is the intended methodology to be applied once the real feature generation logic is integrated.*