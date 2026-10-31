import pandas as pd
from modules.data_cleaner import clean_dataframe

def test_cleaner_trims_and_removes_exact_duplicates():
    df = pd.DataFrame({"name": [" A ", "A", "B"], "value": [1, 1, 2]})
    cleaned, log = clean_dataframe(df)
    assert len(cleaned) == 2
    assert cleaned.iloc[0]["name"] == "A"
