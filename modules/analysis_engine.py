import pandas as pd
import numpy as np

def generate_insights(df):
    insights = [
        f"The dataset contains {len(df):,} rows and {len(df.columns):,} columns.",
        f"There are {int(df.isna().sum().sum()):,} missing cells across all columns.",
        f"There are {int(df.duplicated().sum()):,} exact duplicate rows."
    ]
    numeric = df.select_dtypes(include=np.number)
    if not numeric.empty:
        col = numeric.var(numeric_only=True).fillna(0).idxmax()
        insights.append(f"'{col}' has the largest variance among numeric columns; inspect its spread and units.")
        for c in numeric.columns:
            if numeric[c].notna().any():
                insights.append(f"'{c}' average: {numeric[c].mean():,.2f}; median: {numeric[c].median():,.2f}.")
    categorical = df.select_dtypes(include=["object", "category", "string"])
    for col in categorical.columns[:5]:
        counts = categorical[col].dropna().astype(str).value_counts()
        if not counts.empty:
            insights.append(f"Most frequent value in '{col}' is '{counts.index[0]}' ({counts.iloc[0]:,} records).")
    date_cols = []
    for col in df.columns:
        if any(token in str(col).lower() for token in ["date", "time", "year"]):
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().sum() > 0:
                date_cols.append((col, parsed))
    for col, parsed in date_cols[:2]:
        insights.append(f"'{col}' spans {parsed.min().date()} to {parsed.max().date()} among parseable values.")
    insights.append("These are descriptive findings, not proof of causation. Confirm column meaning and data quality before acting.")
    return insights

def numeric_summary(df):
    numeric = df.select_dtypes(include=np.number)
    if numeric.empty:
        return pd.DataFrame(columns=["column", "count", "mean", "median", "std", "min", "max"])
    result = numeric.describe().T.reset_index().rename(columns={"index":"column"})
    return result
