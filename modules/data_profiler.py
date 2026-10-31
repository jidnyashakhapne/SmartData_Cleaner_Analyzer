import pandas as pd
import numpy as np

def infer_type(series):
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    non_null = series.dropna()
    if len(non_null):
        parsed = pd.to_datetime(non_null.astype(str), errors="coerce")
        if parsed.notna().mean() >= 0.8:
            return "possible_datetime"
    return "categorical/text"

def profile_dataframe(df):
    rows = []
    total = max(len(df), 1)
    for col in df.columns:
        s = df[col]
        missing = int(s.isna().sum())
        rows.append({
            "column": str(col),
            "inferred_type": infer_type(s),
            "missing_count": missing,
            "missing_percent": round(missing / total * 100, 2),
            "unique_count": int(s.nunique(dropna=True)),
            "duplicate_values": int(s.notna().sum() - s.nunique(dropna=True)),
            "sample_values": ", ".join(map(str, s.dropna().astype(str).head(3).tolist()))
        })
    return pd.DataFrame(rows)
