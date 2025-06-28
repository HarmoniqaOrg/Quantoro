import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import lightgbm as lgb

# --- Configuration ---
RESULTS_DIR = "d:/Quantoro/results"
MODEL_PATH = os.path.join(RESULTS_DIR, "ml_alpha_model.txt")
OUTPUT_PLOT_PATH = os.path.join(RESULTS_DIR, "feature_importance.png")


def plot_feature_importance():
    """Loads the trained model and plots feature importance."""
    print("--- Generating Feature Importance Plot ---")

    # --- Load Model ---
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model file not found at {MODEL_PATH}")
        return

    print(f"Loading model from {MODEL_PATH}")
    model = lgb.Booster(model_file=MODEL_PATH)

    # Load feature names
    import json

    features_path = os.path.join(RESULTS_DIR, "ml_alpha_feature_names.json")
    if os.path.exists(features_path):
        with open(features_path, "r") as f:
            feature_names = json.load(f)
        model.feature_name = feature_names
    else:
        print(
            f"Warning: Feature names file not found at {features_path}. Plot may have generic names."
        )

    # --- Plotting ---
    print(f"Generating and saving plot to {OUTPUT_PLOT_PATH}")
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8))

    # --- Manually Plotting for Robustness ---
    # Get feature importances and names
    importances = model.feature_importance(importance_type="gain")
    feature_names = model.feature_name

    # Create a DataFrame for plotting
    importance_df = (
        pd.DataFrame({"Feature": feature_names, "Importance": importances})
        .sort_values(by="Importance", ascending=False)
        .head(10)
    )

    # Create the plot
    sns.barplot(x="Importance", y="Feature", data=importance_df, ax=ax, palette="viridis")

    ax.set_title("Feature Importance (Top 10 by Gain)", fontsize=18, fontweight="bold")
    ax.set_xlabel("Importance (Gain)", fontsize=12)
    ax.set_ylabel("Features", fontsize=12)
    ax.grid(True, which="major", linestyle="--", linewidth=0.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT_PATH, dpi=300)
    print("--- Plotting Complete ---")


if __name__ == "__main__":
    plot_feature_importance()
