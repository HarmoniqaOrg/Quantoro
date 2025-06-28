"""
This module defines the MLAlphaModel and associated data preparation utilities.
"""

import logging
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def build_feature_target_set(
    end_date: pd.Timestamp,
    returns_data: pd.DataFrame,
    fmp_signals: pd.DataFrame,
    lookback_days: int,
    forward_days: int,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Builds feature and target sets for a given date range using merge_asof.

    Args:
        end_date (pd.Timestamp): The final date for the observation window.
        returns_data (pd.DataFrame): DataFrame of daily asset returns.
        fmp_signals (pd.DataFrame): DataFrame of raw FMP signals with 'date' and 'symbol'.
        lookback_days (int): Number of days to look back for feature generation.
        forward_days (int): Number of days to look forward for target generation.

    Returns:
        tuple[pd.DataFrame, pd.Series]: A tuple of (features, target).
    """
    start_date = end_date - pd.DateOffset(days=lookback_days)
    window_returns = returns_data.loc[start_date:end_date]

    # 1. Prepare FMP signals (quarterly)
    fmp = fmp_signals.copy()
    fmp["date"] = pd.to_datetime(fmp["date"])
    fmp = fmp.sort_values("date").set_index("date")

    # 2. Generate daily features and target for each stock
    all_features = []
    all_targets = []
    for stock in window_returns.columns:
        stock_returns = window_returns[[stock]].dropna()
        if stock_returns.empty:
            continue

        # Momentum features
        mom_1m = stock_returns[stock].rolling(21).mean()
        mom_3m = stock_returns[stock].rolling(63).mean()
        mom_12m = stock_returns[stock].rolling(252).mean()

        # Forward returns (target)
        target = stock_returns[stock].shift(-forward_days).rolling(forward_days).sum()

        features = pd.DataFrame({"mom_1m": mom_1m, "mom_3m": mom_3m, "mom_12m": mom_12m})
        features["ticker"] = stock
        features = features.reset_index().rename(columns={"index": "date"})

        # Merge FMP signals using the most recent value
        stock_fmp = fmp[fmp["symbol"] == stock]
        if not stock_fmp.empty:
            features = pd.merge_asof(
                features.sort_values("date"), stock_fmp[["alpha"]], on="date", direction="backward"
            )
        else:
            features["alpha"] = np.nan

        features = features.set_index(["date", "ticker"])
        features = features.rename(columns={"alpha": "fmp_alpha"})

        all_features.append(features)
        all_targets.append(target.rename("target"))

    if not all_features:
        return pd.DataFrame(), pd.Series(dtype=np.float64)

    # 3. Combine and clean final dataset
    X = pd.concat(all_features)
    y = pd.concat(all_targets).loc[X.index]

    final_data = X.join(y).dropna()

    X_final = final_data.drop(columns=["target"])
    y_final = final_data["target"]

    return X_final, y_final


class MLAlphaModel:
    """
    Generates alpha signals using a LightGBM model.
    """

    def __init__(self, lookahead_period: int = 63, lgbm_params: dict = None):
        self.lookahead_period = lookahead_period
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []

        if lgbm_params is None:
            self.lgbm_params = {
                "objective": "regression_l1",
                "metric": "rmse",
                "n_estimators": 1000,
                "learning_rate": 0.05,
                "feature_fraction": 0.8,
                "bagging_fraction": 0.8,
                "bagging_freq": 1,
                "lambda_l1": 0.1,
                "lambda_l2": 0.1,
                "num_leaves": 31,
                "verbose": -1,
                "n_jobs": -1,
                "seed": 42,
                "boosting_type": "gbdt",
            }
        else:
            self.lgbm_params = lgbm_params

    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series):
        if X_train.empty:
            logger.warning("Training data is empty. Skipping model training.")
            self.model = None
            return

        self.feature_names = X_train.columns.tolist()
        X_scaled = self.scaler.fit_transform(X_train)

        self.model = lgb.LGBMRegressor(**self.lgbm_params)
        self.model.fit(X_scaled, y_train, feature_name=self.feature_names)
        logger.info("Successfully trained LightGBM model.")

    def predict_alpha(self, X_pred: pd.DataFrame) -> pd.Series:
        if self.model is None:
            logger.warning("Model not trained. Returning zero alpha.")
            return pd.Series(0, index=X_pred.index.get_level_values("ticker").unique())

        if X_pred.empty:
            logger.warning("Prediction feature set is empty. Returning empty alpha scores.")
            return pd.Series(dtype=np.float64)

        # Align columns and scale
        X_pred_aligned = X_pred.reindex(columns=self.feature_names, fill_value=0)
        X_pred_scaled = self.scaler.transform(X_pred_aligned)

        # Predict and post-process
        predictions = self.model.predict(X_pred_scaled)
        alpha_series = pd.Series(predictions, index=X_pred_aligned.index)

        # Extract latest prediction for each ticker
        latest_alpha = alpha_series.groupby("ticker").last()

        ranked_alpha = latest_alpha.rank(pct=True)
        scaled_alpha = (ranked_alpha - 0.5) * 2

        return scaled_alpha
