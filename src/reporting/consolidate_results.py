import pandas as pd
import os

RESULTS_DIR = "results"

files_to_consolidate = {
    "Baseline CVaR (A)": os.path.join(RESULTS_DIR, "baseline_cvar_performance_metrics.csv"),
    "Regime-Aware CVaR (B)": os.path.join(RESULTS_DIR, "regime_aware_cvar_performance.csv"),
    "Hybrid ML Alpha (C)": os.path.join(RESULTS_DIR, "hybrid_model_performance.csv"),
}

consolidated_metrics = {}

print("--- Consolidating performance metrics ---")

for name, path in files_to_consolidate.items():
    if os.path.exists(path):
        try:
            df = pd.read_csv(path, index_col=0)
            # Assuming the metrics are in the first column
            consolidated_metrics[name] = df.iloc[:, 0]
            print(f"Successfully processed {path}")
        except Exception as e:
            print(f"Error processing {path}: {e}")
    else:
        print(f"Warning: Metric file not found at {path}")

if consolidated_metrics:
    final_df = pd.DataFrame(consolidated_metrics)
    output_path = os.path.join(RESULTS_DIR, "consolidated_performance_metrics.csv")
    final_df.to_csv(output_path)
    print(f"--- Consolidated metrics saved to {output_path} ---")
else:
    print("--- No metrics to consolidate. Exiting. ---")
