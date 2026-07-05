from __future__ import annotations

import pandas as pd


def format_number(value, suffix=""):
    """Format large numbers for human reading.

    Examples:
    - 13000000000 -> 13.00 Mrd
    - 2500000000 -> 2.50 Mrd
    - 450000000 -> 450.0 M
    - 12000 -> 12.0 k
    """
    if pd.isna(value):
        return ""
    try:
        value = float(value)
    except Exception:
        return str(value)

    sign = "-" if value < 0 else ""
    value = abs(value)

    if value >= 1_000_000_000:
        return f"{sign}{value / 1_000_000_000:.2f} Mrd{suffix}"
    if value >= 1_000_000:
        return f"{sign}{value / 1_000_000:.1f} M{suffix}"
    if value >= 1_000:
        return f"{sign}{value / 1_000:.1f} k{suffix}"
    if value == int(value):
        return f"{sign}{int(value)}{suffix}"
    return f"{sign}{value:.2f}{suffix}"


def format_percent(value):
    if pd.isna(value):
        return ""
    try:
        return f"{float(value):.1f}%"
    except Exception:
        return str(value)


def add_readable_columns(frame, money_columns=None, percent_columns=None):
    money_columns = money_columns or []
    percent_columns = percent_columns or []
    readable = frame.copy()
    for col in money_columns:
        if col in readable.columns:
            readable[f"{col}_readable"] = readable[col].apply(format_number)
    for col in percent_columns:
        if col in readable.columns:
            readable[f"{col}_readable"] = readable[col].apply(format_percent)
    return readable
