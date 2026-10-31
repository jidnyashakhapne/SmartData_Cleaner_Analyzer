import pandas as pd

def clean_dataframe(df, remove_duplicates=True, trim_text=True, normalize_missing=True):
    result = df.copy()
    log = []
    before = len(result)

    if normalize_missing:
        changed = 0
        for col in result.select_dtypes(include=["object", "string"]).columns:
            blank_mask = result[col].astype("string").str.strip().eq("")
            changed += int(blank_mask.sum())
            result.loc[blank_mask, col] = pd.NA
        log.append({"operation":"Convert blank strings to missing", "column":"All text columns",
                    "affected_rows":changed, "details":"Whitespace-only values changed to missing."})

    if trim_text:
        affected = 0
        for col in result.select_dtypes(include=["object", "string"]).columns:
            old = result[col].copy()
            result[col] = result[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            affected += int((old != result[col]).fillna(False).sum())
        log.append({"operation":"Trim leading/trailing spaces", "column":"All text columns",
                    "affected_rows":affected, "details":"Text values trimmed; case was not changed."})

    if remove_duplicates:
        duplicate_count = int(result.duplicated().sum())
        result = result.drop_duplicates().copy()
        log.append({"operation":"Remove exact duplicate rows", "column":"All columns",
                    "affected_rows":duplicate_count, "details":"Kept the first occurrence."})

    log.append({"operation":"Row count change", "column":"Dataset",
                "affected_rows":before-len(result),
                "details":f"Rows before: {before}; rows after: {len(result)}."})
    return result, log
