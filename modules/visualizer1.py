"""
visualizer.py
--------------
Responsible for Step 4: generating at least one meaningful chart
(bar, pie, line, histogram, or scatter) with proper titles, axis
labels, readable colors, and a clean layout. Charts are saved to
the exports/ folder (PNG export bonus feature).
"""

import os
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np

matplotlib.use("Agg")  # safe for Streamlit / headless rendering

EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2",
          "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]


def _save(fig, filename="chart.png"):
    path = os.path.join(EXPORT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    return path


def auto_generate_chart(df: pd.DataFrame, filename="chart.png"):
    """
    Automatically picks a sensible chart type based on the dataset's
    column types and generates it:
      - categorical + numeric  -> bar chart (sum of numeric by category)
      - only categorical       -> bar chart of value counts
      - only numeric           -> histogram of the first numeric column
    Returns (matplotlib Figure, saved_file_path, chart_type).
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    fig, ax = plt.subplots(figsize=(8, 5))

    if categorical_cols and numeric_cols:
        cat_col, num_col = categorical_cols[0], numeric_cols[0]
        grouped = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False).head(10)
        ax.bar(grouped.index.astype(str), grouped.values, color=COLORS[: len(grouped)])
        ax.set_title(f"Total {num_col} by {cat_col}", fontsize=14, fontweight="bold")
        ax.set_xlabel(cat_col, fontsize=11)
        ax.set_ylabel(num_col, fontsize=11)
        plt.xticks(rotation=30, ha="right")
        chart_type = "bar"

    elif categorical_cols:
        cat_col = categorical_cols[0]
        counts = df[cat_col].value_counts().head(10)
        ax.bar(counts.index.astype(str), counts.values, color=COLORS[: len(counts)])
        ax.set_title(f"Distribution of {cat_col}", fontsize=14, fontweight="bold")
        ax.set_xlabel(cat_col, fontsize=11)
        ax.set_ylabel("Count", fontsize=11)
        plt.xticks(rotation=30, ha="right")
        chart_type = "bar"

    elif numeric_cols:
        num_col = numeric_cols[0]
        ax.hist(df[num_col].dropna(), bins=20, color=COLORS[0], edgecolor="white")
        ax.set_title(f"Distribution of {num_col}", fontsize=14, fontweight="bold")
        ax.set_xlabel(num_col, fontsize=11)
        ax.set_ylabel("Frequency", fontsize=11)
        chart_type = "histogram"

    else:
        ax.text(0.5, 0.5, "No suitable columns found for charting",
                ha="center", va="center")
        chart_type = "none"

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()

    path = _save(fig, filename)
    return fig, path, chart_type
