import pandas as pd
import re

def normalize_strings(s, keep_replacement_char=False, keep_question_mark=False, sort_tokens=False):
    """
    Normalize a string: strip, collapse spaces, uppercase remove all except A-Z, 0-9, and spaces.
    Optionally sort tokens to reduce ordering inconsistencies.
    """
    if pd.isna(s):
        return s
    
    s = str(s).strip()
    s = s.upper()
    s = re.sub(r"\s+", " ", s)

    extra = ""
    if keep_replacement_char:
        extra += "\uFFFD"
    if keep_question_mark:
        extra += "?"

    # Remove anything not in A-Z, 0-9, space, or the requested extras.
    base = "A-Z0-9 Ñ"
    pattern = f"[^{base}{extra}]"
    s = re.sub(pattern, "", s)

    if sort_tokens:
        tokens = s.split()
        tokens = sorted(tokens)
        s = " ".join(tokens)


    return s