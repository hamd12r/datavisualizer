import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

def ensure_export_dir():
    """Ensures the exports directory exists for saving charts."""
    if not os.path.exists("exports"):
        os.makedirs("exports")

def generate_chart(df, col_x, col_y, chart_type):
    """
    Generates a matplotlib/seaborn chart based on user selection.
    Returns the figure object so Streamlit can render it.
    """
    try:
        # Create a new figure and axis for the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Apply a clean, professional theme
        sns.set_theme(style="whitegrid")

        if chart_type == "Bar Chart":
            # If Y is numeric, calculate the sum. If text, calculate the count.
            if pd.api.types.is_numeric_dtype(df[col_y]):
                plot_data = df.groupby(col_x, as_index=False)[col_y].sum()
            else:
                plot_data = df.groupby(col_x, as_index=False)[col_y].count()
            
            # Sort ascending so the bars scale up neatly
            plot_data = plot_data.sort_values(by=col_y, ascending=True)

            # Generate vertical bars without messy error lines
            ax.bar(plot_data[col_x], plot_data[col_y], color='teal')

            for container in ax.containers:
                ax.bar_label(container, fmt='%g', padding=3, fontsize=10)
            ax.set_title(f"{col_y} by {col_x}", fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha="right")
            
        elif chart_type == "Line Chart":
            # Line charts are best for trends over time
            plt.lineplot(data=df, x=col_x, y=col_y, ax=ax, marker='o', color='b')
            for i in range(len(df)):
                ax.annotate(str(df[col_y].iloc[i]), 
                            (df[col_x].iloc[i], df[col_y].iloc[i]),
                            textcoords="offset points", 
                            xytext=(0, 7), 
                            ha='center', fontsize=9)

            ax.set_title(f"Trend of {col_y} over {col_x}", fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha="right")
            
        elif chart_type == "Scatter Plot":
            # Scatter plots show the relationship between two numerical variables
            plt.scatterplot(data=df, x=col_x, y=col_y, ax=ax, s=100, color='r', alpha=0.7)
            for i in range(len(df)):
                ax.annotate(str(df[col_y].iloc[i]), 
                            (df[col_x].iloc[i], df[col_y].iloc[i]),
                            textcoords="offset points", 
                            xytext=(0, 7), 
                            ha='center', fontsize=9)
            ax.set_title(f"Relationship: {col_x} vs {col_y}", fontsize=14, fontweight='bold')
            
        elif chart_type == "Histogram":
            # Histograms only need one column (col_x) to show distribution
            plt.histplot(data=df, x=col_x, kde=True, ax=ax, color='purple')
            for container in ax.containers:
                ax.bar_label(container, fmt='%g', padding=3, fontsize=10)
            ax.set_title(f"Distribution of {col_x}", fontsize=14, fontweight='bold')

        # Ensure labels are clear and layout is tight so nothing gets cut off
        ax.set_xlabel(col_x, fontsize=12)
        if chart_type != "Histogram":
            ax.set_ylabel(col_y, fontsize=12)
        else:
            ax.set_ylabel("Frequency", fontsize=12)
            
        plt.tight_layout()
        
        return fig
    except Exception as e:
        return f"Error generating chart: {e}"

def save_chart(fig, filename="exported_chart.png"):
    """
    Bonus Feature: Saves the generated figure as a PNG file.
    """
    try:
        ensure_export_dir()
        filepath = os.path.join("exports", filename)
        fig.savefig(filepath, dpi=300, bbox_inches="tight")
        return filepath
    except Exception as e:
        return None