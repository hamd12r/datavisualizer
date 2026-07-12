# 📊 AI Data Analysis Assistant — Track A (Explorer)

A Streamlit application that loads a CSV dataset, answers natural-language
questions, generates a chart, and produces an AI-powered explanation of the
findings.

## Project Structure

```
ai_data_explorer/
│
├── app.py                 # Streamlit UI — run this file
├── modules/
│   ├── data_handler.py    # CSV loading, stats, rule-based Q&A (Steps 1-3)
│   ├── visualizer.py      # Chart generation (Step 4)
│   └── ai_explainer.py    # Single Gemini API call for explanation (Step 5)
├── data/
│   └── dataset.csv        # Sample dataset (used if no file is uploaded)
├── exports/                # Generated chart PNGs are saved here
├── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. (Optional but recommended) Get a free Gemini API key from
   [Google AI Studio](https://aistudio.google.com/apikey) and either:
   - Enter it in the sidebar text box when the app is running, **or**
   - Set it as an environment variable before launching:
     ```bash
     export GEMINI_API_KEY="your_key_here"   # On Windows: set GEMINI_API_KEY=your_key_here
     ```

## Running the App

```bash
streamlit run app.py
```

This opens the app in your browser (default: http://localhost:8501).

## Usage Flow

1. Upload a CSV file (or the app will use the sample `data/dataset.csv`).
2. Review the dataset preview, column details, and summary statistics.
3. Type in the 3 fixed questions provided by the judges and click
   **Get Answers**.
4. Click **Generate Chart & Explanation** to produce a chart and an
   AI-generated explanation of the key insight.
5. Use the **Export Chart as PNG** button to download the chart.

## Notes for Judges

- No manual code modification is needed to run the project.
- If no internet/API key is available, the app still functions using the
  fallback explanation logic, so the full pipeline (load → analyze →
  answer → chart → explain) can be demonstrated offline.
