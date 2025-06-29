# src/reporting/generate_final_report.py

import pandas as pd
from markdown_pdf import MarkdownPdf, Section
import os
from .utils import read_file_content, format_metrics_table

# --- Configuration ---
RESULTS_DIR = "results"
DOCS_DIR = "docs"

METRICS_FILE = os.path.join(RESULTS_DIR, "consolidated_performance_metrics.csv")
TASK_B_SUMMARY_FILE = os.path.join(DOCS_DIR, "task_b_method_summary.md")
TASK_B_REPORT_FILE = os.path.join(DOCS_DIR, "task_b_interpretability_report.md")
PERFORMANCE_PLOT = os.path.join(RESULTS_DIR, "comprehensive_performance_comparison.png")
REGIME_PLOT = os.path.join(RESULTS_DIR, "regime_interpretability.png")
OUTPUT_PDF = "report.pdf"


# --- Report Content Assembly ---
print("Assembling final report...")

# Title Page
report_title = "# Alpha Pods Take-Home Assignment Report"
author_line = "**Candidate:** Pierre-Louis Blossier | **Date:** 2025-06-26"

# Introduction
intro_text = """
## Introduction
This report details the methodology and results for the three tasks in the Alpha Pods take-home assignment. The project progresses from replicating a baseline CVaR optimization strategy to enhancing it with a machine learning-based regime-aware framework, and finally, incorporating alternative data to generate alpha.
"""

# Task A: Baseline CVaR Index
task_a_summary = """
## Task A: Baseline CVaR Index

As required by the assignment, this section details the results of the baseline CVaR model reproduced from the CLEIR paper.

### Performance Plot
The plot below compares the cumulative returns of the Baseline CVaR index against the equal-weighted benchmark over the full 2010-2024 period.

![Baseline CVaR Performance vs. Benchmarks](results/task_a_performance_comparison.png)

### Key Output Files for Verification
To facilitate a thorough review, the following key output files for Task A are located in the `results/` directory. These files provide full transparency into the backtest execution and results.

*   `baseline_cvar_performance_metrics.csv`: A table containing the final required performance metrics (Annual Return, Volatility, Sharpe Ratio, 95% CVaR, Max Drawdown, and Turnover).
*   `baseline_cvar_index.csv`: The daily index values of the CVaR-optimized portfolio from 2010 to 2024.
*   `baseline_daily_returns.csv`: The daily returns of the final portfolio strategy.
*   `baseline_daily_weights.csv`: The daily weights of each asset in the portfolio.
*   `baseline_cvar_rebalance_weights_2010-2024.csv`: The target weights determined at each quarterly rebalance.
*   `equal_weighted_daily_returns.csv`: The daily returns of the equal-weighted benchmark.
*   `equal_weighted_daily_weights.csv`: The daily weights of the equal-weighted benchmark.
"""

# Task B: Regime-Aware Enhancement
task_b_summary = read_file_content(TASK_B_SUMMARY_FILE)

# Task C: Alpha in the Wild
task_c_summary = """
## Task C: Alpha-Aware Strategy
This strategy enhances the CVaR optimizer by incorporating alpha signals derived from alternative data. We sourced fundamental signals (e.g., P/E ratio, ROE, Market Cap) from the Financial Modeling Prep (FMP) API. These signals were combined into a single alpha score for each asset. The optimizer's objective function was modified to not only minimize CVaR but also to maximize the portfolio's exposure to these positive alpha signals, effectively tilting the portfolio towards stocks with stronger fundamental characteristics.
"""

# Consolidated Results
results_header = "## Consolidated Performance Metrics (2020-2024)"
metrics_table = format_metrics_table(METRICS_FILE)
performance_plot_md = f"\n![Performance Comparison]({PERFORMANCE_PLOT})"

# Detailed Analysis for Task B
regime_analysis_header = "## Task B: Regime Model Interpretability"
regime_plot_md = f"\n![Regime Analysis]({REGIME_PLOT})"

# Reflections
reflections = """
## Reflections & Conclusion
This project successfully demonstrated an end-to-end quantitative research workflow. The baseline CVaR model provided a solid foundation. The regime-aware enhancement (Task B) proved effective, showcasing how a simple SMA crossover can identify high-volatility periods and allow the strategy to adapt defensively. The alpha-aware model (Task C) showed the potential of integrating alternative data, though its performance indicates that more sophisticated signal combination and risk management are required to fully exploit its potential.

Key learnings include the importance of robust data pipelines, the challenges of feature engineering for financial markets, and the necessity of a rigorous backtesting framework. The results highlight that while complexity can add value, simple, interpretable models often provide the most robust performance enhancements.
"""

# --- Generate PDF ---
print(f"Generating PDF report: {OUTPUT_PDF}...")

# Assemble all markdown content
full_markdown = "\n\n".join(
    [
        report_title,
        author_line,
        intro_text,
        results_header,
        metrics_table,
        performance_plot_md,
        task_a_summary,
        task_b_summary,
        regime_analysis_header,
        regime_plot_md,
        task_c_summary,
        reflections,
    ]
)

pdf = MarkdownPdf(toc_level=2)
pdf.add_section(Section(full_markdown, toc=False))
pdf.save(OUTPUT_PDF)

print("Report generated successfully.")
