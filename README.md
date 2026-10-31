# SmartData Cleaner & Analyzer

A reusable CSV/Excel data profiling, cleaning-preview, exploratory analysis and reporting application built with Python and Streamlit.

## Features
- Upload CSV, XLSX and XLS files.
- Profile columns, inferred types, missing values and distinct counts.
- Preview conservative cleaning: whitespace trimming, blank-to-null conversion and exact duplicate removal.
- Generate generic descriptive insights and interactive charts.
- Download cleaned CSV, multi-sheet Excel report and PDF summary.

## Requirements
- Python 3.10+
- VS Code or another Python editor

## Setup (Windows)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL shown in the terminal.

## Setup (macOS/Linux)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Run the tests
```bash
python -m pytest
```

## Project structure
```text
app.py
modules/                 # profiling, cleaning, analysis, PDF, UI styling
tests/                   # pytest unit tests
.streamlit/config.toml   # theme and toolbar settings
requirements.txt
```

## Cleaning policy
This starter implementation intentionally avoids automatically imputing missing values, converting arbitrary text to numbers, or deleting statistical outliers. Those actions can damage legitimate data. Review data quality findings and add domain-specific rules before applying them.

## Limitations and next improvements
- Column type inference is heuristic; ambiguous dates and numeric strings need user review.
- Universal insights are descriptive. Reliable business KPIs require domain-aware column mapping and business definitions.
- Excel files with multiple sheets currently load the first sheet.
- Large uploads may require chunked processing and file-size limits.
- Add user authentication, configurable cleaning rules, more tests, and deployment hardening before production use.
