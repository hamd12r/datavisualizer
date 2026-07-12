import google.generativeai as genai
import os

def get_model(api_key):
    """Configures and returns the Gemini model."""
    genai.configure(api_key=api_key)
    # Using 'gemini-1.5-flash-latest' is the most stable approach to avoid 404s
    return genai.GenerativeModel('gemini-1.5-flash-latest')

def answer_question(api_key, data_summary, user_question):
    """
    Answers a specific user question using the AI based on the dataset summary.
    """
    try:
        model = get_model(api_key)
        
        prompt = f"""
        You are an expert Data Analyst. Given the following dataset summary:
        {data_summary}
        
        Answer the following question about the dataset professionally and concisely:
        {user_question}
        
        If the answer cannot be determined from the summary, state that clearly.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def get_chart_explanation(api_key, chart_type, col_x, col_y, data_summary):
    """
    Generates a concise explanation of a generated chart.
    """
    try:
        model = get_model(api_key)
        
        prompt = f"""
        You are a data interpretation expert. A user has generated a {chart_type}
        visualizing {col_y} versus {col_x}.
        
        Here is a brief statistical summary of the data used in the chart:
        {data_summary}
        
        Provide a 2-3 sentence explanation of what this chart shows and 
        any interesting trends the user should notice. Be professional and 
        insightful.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Explanation Error: {str(e)}"