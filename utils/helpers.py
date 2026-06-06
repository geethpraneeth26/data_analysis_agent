"""
Shared utility helpers.
"""
import pandas as pd
import numpy as np


def format_number(val) -> str:
    """Pretty-print a number."""
    try:
        f = float(val)
        if f != f:  # NaN
            return "—"
        if f == int(f) and abs(f) < 1e12:
            return f"{int(f):,}"
        return f"{f:,.2f}"
    except Exception:
        return str(val)


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")


def truncate_col_names(cols: list, max_len: int = 30) -> list:
    return [c[:max_len] + "…" if len(c) > max_len else c for c in cols]
