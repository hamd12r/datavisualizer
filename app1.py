"""
app.py
-------
Main Streamlit entry point for the AI Data Analysis Assistant.
Run with:  streamlit run app.py
"""

import os
import io
import streamlit as st
import pandas as pd

from modules.data_handler import load_dataset, get_dataset_info, get_summary_stats, answer_question
from modules.visualizer import recommend_chart, generate_chart, get_column_options, CHART_TYPES
from modules.ai_explainer import explain_result

st.set_page_config(page_title="AI Data Analysis Assistant", page_icon="📊", layout="wide")

st.title("📊 AI Data Analysis Assistant")
st.caption("Upload a CSV, ask questions, generate a chart, and get an AI-powered explanation.")

# ---------- Sidebar: dark mode toggle (bonus feature) ----------
with st.sidebar:
    st.header("⚙️ Settings")
    dark_mode = st.toggle("Dark mode", value=False)
    st.markdown("---")
    st.markdown("**API Key**")
    api_key_input = st.text_input("Gemini API Key (optional)", type="password",
                                   help="If left blank, a fallback explanation is used instead of a live AI call.")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

if dark_mode:
    st.markdown(
        """
        <style>
        .stApp { background-color: #0e1117; color: #fafafa; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---------- Step 1: Load Dataset ----------
uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

default_path = os.path.join("data", "dataset.csv")
if uploaded_file is not None:
    df = load_dataset(uploaded_file)
elif os.path.exists(default_path):
    st.info("No file uploaded — using the sample dataset in data/dataset.csv")
    df = load_dataset(default_path)
else:
    df = None

if df is not None:
    st.success("Dataset loaded successfully!")

    with st.expander("📋 Dataset Preview", expanded=True):
        st.dataframe(df.head(10), use_container_width=True)

    # ---------- Step 1 & 2: Info + Stats ----------
    info = get_dataset_info(df)
    stats = get_summary_stats(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", info["rows"])
    col2.metric("Columns", info["columns"])
    col3.metric("Missing Values", sum(info["missing_values"].values()))

    with st.expander("🔍 Column Details"):
        detail_df = pd.DataFrame({
            "Column": info["column_names"],
            "Data Type": [info["dtypes"][c] for c in info["column_names"]],
            "Missing Values": [info["missing_values"][c] for c in info["column_names"]],
        })
        st.dataframe(detail_df, use_container_width=True)

    with st.expander("📈 Summary Statistics"):
        st.json(stats)

    st.markdown("---")

    # ---------- Step 3: Answer Fixed Questions ----------
    st.subheader("❓ Ask Questions (Judges' 3 Fixed Questions)")
    st.caption("Rule-based logic answers these — no LLM call is used here.")

    q1 = st.text_input("Question 1", placeholder="e.g. Which product generated the highest sales?")
    q2 = st.text_input("Question 2", placeholder="e.g. What is the average age of customers?")
    q3 = st.text_input("Question 3", placeholder="e.g. Which category appears most frequently?")

    if st.button("Get Answers"):
        for i, q in enumerate([q1, q2, q3], start=1):
            if q.strip():
                answer = answer_question(df, q)
                st.write(f"**Q{i}: {q}**")
                st.success(answer)

    st.markdown("---")

    # ---------- Step 4 & 5: Chart + AI Explanation ----------
    st.subheader("📊 Chart & AI Explanation")

    numeric_cols, categorical_cols = get_column_options(df)
    all_cols = df.columns.tolist()
    rec = recommend_chart(df)

    if rec["chart_type"]:
        st.markdown(
            f"**🤖 Recommended:** {rec['chart_type']} chart — "
            f"X: `{rec['x_col']}`" + (f", Y: `{rec['y_col']}`" if rec["y_col"] else "")
        )
        st.caption(rec["reason"])
    else:
        st.warning(rec["reason"])

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        chart_type = st.selectbox(
            "Chart type",
            CHART_TYPES,
            index=CHART_TYPES.index(rec["chart_type"]) if rec["chart_type"] in CHART_TYPES else 0,
        )
    with col_b:
        x_col = st.selectbox(
            "X axis",
            all_cols,
            index=all_cols.index(rec["x_col"]) if rec["x_col"] in all_cols else 0,
        )
    with col_c:
        y_options = ["(none / count)"] + all_cols
        default_y = rec["y_col"] if rec["y_col"] in all_cols else "(none / count)"
        y_choice = st.selectbox("Y axis", y_options, index=y_options.index(default_y))
        y_col = None if y_choice == "(none / count)" else y_choice

    if st.button("Generate Chart & Explanation"):
        with st.spinner("Generating chart..."):
            fig, chart_path = generate_chart(df, chart_type, x_col, y_col)
            st.pyplot(fig)

        with st.spinner("Generating AI explanation..."):
            explanation = explain_result(chart_type, stats, context_note=f"Chart: {chart_type} of X={x_col}, Y={y_col}")
            st.info(explanation)

        # Bonus: export chart as PNG
        with open(chart_path, "rb") as f:
            st.download_button("⬇️ Export Chart as PNG", f, file_name="chart.png", mime="image/png")

else:
    st.warning("Please upload a CSV file to begin, or place a sample file at data/dataset.csv")
