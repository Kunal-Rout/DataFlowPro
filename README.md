# DataFlow Pro 📊

**Professional Data Analytics Without Coding**

A modular, production-grade data analysis web app built with Streamlit. Upload any CSV and instantly get interactive visualizations, statistical summaries, correlation analysis, and data cleaning — all without writing a single line of code.

🌐 **Live App**: [dataflow-pro.streamlit.app](https://dataflow-pro.streamlit.app/)

---

## ✨ Features

- **📁 Smart CSV Upload** — instant preview, column analysis, and data quality scoring
- **🧹 Data Cleaning** — 8 missing value strategies, type conversion, deduplication, text standardization
- **📈 Interactive Visualizations** — bar, line, scatter, pie, histogram, and box plots with color scheme selection
- **🔗 Correlation Analysis** — heatmaps, automated strong correlation detection, pairwise variable comparison with trendlines
- **📊 Statistical Summary** — descriptive stats, skewness, kurtosis, missing value analysis, and export options
- **💾 Export** — download cleaned data and statistical reports as CSV

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualizations | Plotly |
| Language | Python 3.11+ |

---

## 📁 Project Structure

```
dataflow-pro/
│
├── app.py              ← Entry point (routing only, ~40 lines)
├── requirements.txt
├── .python-version
├── .gitignore
│
├── .streamlit/
│   ├── config.toml               ← Light theme
│   └── config_dark.toml          ← Dark theme
│
├── src/
│   ├── components/               ← One file per page
│   │   ├── home.py
│   │   ├── upload.py
│   │   ├── cleaning.py
│   │   ├── visualization.py
│   │   ├── correlation.py
│   │   └── statistics.py
│   │
│   ├── utils/                    ← Reusable helpers
│   │   ├── data_helpers.py
│   │   ├── chart_helpers.py
│   │   └── style_helpers.py
│   │
│   └── config/                   ← App-wide constants & settings
│       ├── settings.py
│       └── constants.py
│
├── data/
│   └── sample_data.csv
│
└── tests/
    ├── test_data_helpers.py
    └── test_components.py
```

---

## 🚀 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/Kunal-Rout/DataFlowPro.git
cd DataFlowPro

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run streamlit_app.py
```

Open your browser at `http://localhost:8501`

---

## 📊 Sample Data Format

```csv
Employee_ID,Name,Department,Age,Salary,Performance_Score
1001,John Smith,IT,28,55000,85
1002,Jane Doe,HR,34,75000,92
```

A sample dataset is included at `data/sample_data.csv` to try the app immediately.

---

## 🎯 How to Use

1. **Upload** your CSV file in the Data Upload section
2. **Clean** your data — handle missing values, remove duplicates, convert types
3. **Visualize** — pick a chart type, columns, and color scheme
4. **Correlate** — discover relationships between numeric variables
5. **Summarize** — view full statistical breakdown
6. **Export** — download your cleaned data or statistical report

---

## 📜 License

MIT License — free to use, modify, and distribute.