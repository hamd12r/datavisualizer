import streamlit as st
import pandas as pd
import os

# Import our custom modules
from modules import data_handler, visualizer, ai_explainer

st.set_page_config(
    page_title="AI Data Explorer",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("⚙️ Configuration")
st.sidebar.write("Upload your dataset and configure the AI.")

# 1. API Key Input (Securely hidden)
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key to enable AI explanations.")

# 2. File Uploader (Bonus Feature)
uploaded_file = st.sidebar.file_uploader("Upload CSV Dataset", type=["csv"])

st.title("🚀 AI Data Analysis Assistant")
st.markdown("Welcome to the AI Data Explorer! Upload a dataset on the left to begin your analysis.")

if uploaded_file is not None:
    # --- PHASE 1: DATA HANDLING ---
    with st.spinner("Loading and cleaning data..."):
        # Load and clean
        raw_df = data_handler.load_data(uploaded_file)
        
        if isinstance(raw_df, str): # Error handling check
            st.error(raw_df)
        else:
            df = data_handler.clean_data(raw_df)
            st.success(f"Dataset successfully loaded and cleaned! ({len(df)} rows ready for analysis)")


            st.header("Dataset Overview & Statistics")
            
            with st.expander("📋 Dataset Preview",):
                st.dataframe(df.head(5), use_container_width=True)
            
            info = data_handler.get_basic_info(df)
            # stats = get_summary_stats(df)

            with st.expander("📋 Dataset Preview", expanded=True):
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Rows", info['Total Rows'])
                col2.metric("Total Columns", info['Total Columns'])
                col3.metric("Missing Values", info['Total Missing Values'])
                

            st.subheader("Numerical Overview")
            stats = data_handler.get_statistics(df)


            if "Numerical Overview" in stats:
                    df_stats = pd.DataFrame(stats["Numerical Overview"])
                    
                    # Add selection options for the metrics
                    metric_option = st.selectbox("Select Statistic Type:", ["Select stat","Counts", "Mean", "Std", "Box Plot Metrics"])
                    
                    if metric_option == "Select stat":
                        st.write('')
                    if metric_option == "Counts":
                        st.dataframe(df_stats.loc[['Counts']])
                    elif metric_option == "Mean":
                        st.dataframe(df_stats.loc[['Mean']])
                    elif metric_option == "Std":
                        st.dataframe(df_stats.loc[['Std']])
                    elif metric_option == "Box Plot Metrics":
                        box_plot_rows = [r for r in df_stats.index if "Box Plot" in r]
                        st.dataframe(df_stats.loc[box_plot_rows])
            else:
                    st.write("No numerical columns found in this dataset.")


            st.divider()

            # --- PHASE 2: JUDGE QUESTIONS ---
            st.header("We Can Answer Your Questions in Data")
            st.markdown("Enter a question and click 'Ask AI' to get an answer based on your dataset.")
            
            # Replaced selectbox with text_input for dynamic user questions
            question = st.text_input(
                "Ask a question about your dataset:", 
                placeholder="e.g., Which product generated the highest sales?"
            )
            
            if st.button("Ask AI"):
                if question:
                    with st.spinner("AI is analyzing the data..."):
                        # Create a quick summary to give the AI context
                        data_summary = df.describe().to_string()
                        
                        # Call the new AI function
                        ai_answer = ai_explainer.answer_question(api_key, data_summary, question)
                        st.info(f"**AI Answer:** {ai_answer}")
                else:
                    st.warning("Please enter a question first!")


            st.divider()

            # --- PHASE 3: VISUALIZATION ---
            st.header("Step 4: Generate Chart")
            st.markdown("Configure your visualization settings below.")
            
            # Form to select chart options
            chart_col1, chart_col2, chart_col3 = st.columns(3)
            with chart_col1:
                chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram"])
            with chart_col2:
                x_col = st.selectbox("X-Axis Column", df.columns)
            with chart_col3:
                # Exclude strings for Y-axis generally, but let the user decide
                y_col = st.selectbox("Y-Axis Column (Not needed for Histogram)", df.columns)

            # Generate Chart Button
            if st.button("Generate Chart & Analyze"):
                fig = visualizer.generate_chart(df, x_col, y_col, chart_type)
                
                if isinstance(fig, str): # Error check
                    st.error(fig)
                else:
                    st.pyplot(fig)
                    
                    # Bonus Feature: Export Chart
                    filepath = visualizer.save_chart(fig)
                    if filepath:
                        with open(filepath, "rb") as file:
                            st.download_button(
                                label="Download Chart as PNG",
                                data=file,
                                file_name="ai_analysis_chart.png",
                                mime="image/png"
                            )

                    # --- PHASE 4: AI EXPLANATION ---
                    st.header("Step 5: Explain the Result (AI)")
                    with st.spinner("Asking AI for an explanation..."):
                        # We pass a snippet of the data related to the chosen columns to the AI
                        data_summary = df[[x_col, y_col]].describe().to_string() if chart_type != "Histogram" else df[[x_col]].describe().to_string()
                        
                        explanation = ai_explainer.get_chart_explanation(
                            api_key=api_key, 
                            chart_type=chart_type, 
                            col_x=x_col, 
                            col_y=y_col, 
                            data_summary=data_summary
                        )
                        
                        st.success(explanation)
else:
    # Show instructions if no file is uploaded yet
    st.info("👈 Please upload a CSV file from the sidebar to start the analysis.")