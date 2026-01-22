import pandas as pd
import re

def normalize_strings(s):
    """
    Normalize a string: strip, collapse spaces, uppercase remove all except A-Z, 0-9, and spaces.
    """
    if pd.isna(s):
        return s
    
    s = str(s).strip()
    s = s.upper()
    s = re.sub(r"\s+", " ", s)
    s = re.sub
    s = re.sub(r"[^A-Z0-9 ]", "", s)

    return s