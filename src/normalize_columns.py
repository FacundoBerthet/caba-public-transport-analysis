import pandas as pd
import re

def normalize_columns(index_cols):
    """
    Normalize column names: strip, lowercase, replace spaces with _, remove special characters except _.
    """

    series_cols = (
        pd.Series(index_cols)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )

    return pd.Index(series_cols)