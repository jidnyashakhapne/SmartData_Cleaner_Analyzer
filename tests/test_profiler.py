import pandas as pd
from modules.data_profiler import profile_dataframe

def test_profile_reports_missing_values():
    df = pd.DataFrame({"a": [1, None], "b": ["x", "y"]})
    profile = profile_dataframe(df)
    assert int(profile.loc[profile.column == "a", "missing_count"].iloc[0]) == 1
