# src/reporting/generate_final_report.py

import pandas as pd
from markdown_pdf import MarkdownPdf, Section
import os

# --- Configuration ---
RESULTS_DIR = 'results'
DOCS_DIR = 'docs'
IMG_DIR = os.path.join(RESULTS_DIR, 'img')
METRICS_FILE = os.path.join(RESULTS_DIR, 'consolidated_performance_metrics.csv')
TASK_B_SUMMARY_FILE = os.path.join(DOCS_DIR, 'task_b_method_summary.md')
TASK_B_REPORT_FILE = os.path.join(DOCS_DIR, 'task_b_interpretability_report.md')
PERFORMANCE_PLOT = os.path.join(IMG_DIR, 'performance_comparison.png')
REGIME_PLOT = os.path.join(IMG_DIR, 'regime_analysis_plot.png')
OUTPUT_PDF = 'report.pdf'

# --- Helper Functions ---
def read_file_content(file_path):
    """Reads the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def format_metrics_table(file_path):
    """Reads a CSV and formats it as a Markdown table."""
    df = pd.read_csv(file_path, index_col=0)
    return df.to_markdown()

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
The baseline strategy implements the CVaR optimization as described in the CLEIR paper. The portfolio is rebalanced quarterly to minimize the 95% Conditional Value-at-Risk of the tracking error against an equal-weight benchmark. The optimization is subject to constraints including a 5% maximum weight per asset and a 10 bps transaction cost.
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
This project successfully demonstrated an end-to-end quantitative research workflow. The baseline CVaR model provided a solid foundation. The regime-aware enhancement (Task B) proved effective, showcasing how a simple HMM can identify high-volatility periods and allow the strategy to adapt defensively. The alpha-aware model (Task C) showed the potential of integrating alternative data, though its performance indicates that more sophisticated signal combination and risk management are required to fully exploit its potential.

Key learnings include the importance of robust data pipelines, the challenges of feature engineering for financial markets, and the necessity of a rigorous backtesting framework. The results highlight that while complexity can add value, simple, interpretable models often provide the most robust performance enhancements.
"""

# --- Generate PDF ---
print(f"Generating PDF report: {OUTPUT_PDF}...")

# Assemble all markdown content
full_markdown = "\n\n".join([
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
    reflections
])

pdf = MarkdownPdf(toc_level=2)
pdf.add_section(Section(full_markdown, toc=False))
pdf.save(OUTPUT_PDF)

print("Report generated successfully.")
