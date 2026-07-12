import pandas as pd
import numpy as np

def load_data(file):
    """
    Loads a CSV file into a Pandas DataFrame.
    Can handle both file paths (strings) and uploaded file objects.
    """
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        return f"Error loading file: {e}"

def get_basic_info(df):
    """
    Extracts basic dataset info. We calculate missing values 
    before any cleaning is applied.
    """
    # Calculate sum of missing values across the whole dataframe
    total_missing = int(df.isnull().sum().sum())
    
    info = {
        "Total Rows": df.shape[0],
        "Total Columns": df.shape[1],
        "Column Names": df.columns.tolist(),
        "Total Missing Values": total_missing,
        "Data Types": df.dtypes.astype(str).to_dict()
    }
    return info

def clean_data(df):
    """
    Cleans the dataset by dropping completely empty rows and 
    handling missing values to prevent crashes during analysis.
    """
    # 1. Create a strict copy so we don't accidentally overwrite raw_df
    df_cleaned = df.copy()
    
    # 2. Drop rows where ALL columns are entirely empty
    df_cleaned = df_cleaned.dropna(how='all')
    
    # Fill remaining missing numeric values with 0 and text with 'Unknown'
    # (This is a basic cleaning strategy; you can adjust this based on the specific dataset)
    for col in df_cleaned.columns:
        if pd.api.types.is_numeric_dtype(df_cleaned[col]):
            df_cleaned[col] = df_cleaned[col].fillna(0)
        else:
            df_cleaned[col] = df_cleaned[col].fillna('Unknown')
            
    return df_cleaned



def get_statistics(df):
    """
    Calculates key statistics.
    Separates numerical summary and categorical distributions.
    """
    stats = {}
    
    # Get numerical stats and explicitly label the 4 options
    numerical_cols = df.select_dtypes(include=[np.number])
    if not numerical_cols.empty:
        # We rename the rows so it explicitly shows Counts, Mean, Std, and the 5 Box Plot stats
        custom_describe = numerical_cols.describe().rename(index={
            'count': 'Counts',
            'mean': 'Mean',
            'std': 'Std',
            'min': 'Box Plot (Min)',
            '25%': 'Box Plot (25%)',
            '50%': 'Box Plot (Median)',
            '75%': 'Box Plot (75%)',
            'max': 'Box Plot (Max)'
        })
        stats['Numerical Overview'] = custom_describe.to_dict()
        
    # Get frequency/distribution for categorical columns (text data)
    categorical_cols = df.select_dtypes(include=['object'])
    stats["Categorical Overview"] = {}
    for col in categorical_cols.columns:
        # Get the top 5 most frequent items in each text column
        stats["Categorical Overview"][col] = df[col].value_counts().head(5).to_dict()
        
    return stats


def answer_judge_questions(df, question_type):
    """
    Placeholder logic to answer the 3 specific judge questions for Step 3.
    Since we don't know the exact questions yet, we set up a robust structure
    that can easily be modified on the day of the competition.
    """
    # Example Question 1: "Which product generated the highest sales?"
    if question_type == "highest_sales":
        # Assuming we have 'Product' and 'Sales' columns
        if 'Product' in df.columns and 'Sales' in df.columns:
            top_product = df.groupby('Product')['Sales'].sum().idxmax()
            return f"The product that generated the highest sales is {top_product}."
        return "Columns 'Product' and 'Sales' not found in dataset."
        
    # Example Question 2: "What is the average age of customers?"
    elif question_type == "average_age":
        if 'Age' in df.columns:
            avg_age = df['Age'].mean()
            return f"The average age of customers is {avg_age:.1f} years."
        return "Column 'Age' not found in dataset."
        
    # Example Question 3: "Which category appears most frequently?"
    elif question_type == "most_frequent_category":
        if 'Category' in df.columns:
            top_category = df['Category'].value_counts().idxmax()
            return f"The most frequently appearing category is {top_category}."
        return "Column 'Category' not found in dataset."
        
    else:
        return "Question type not recognized."