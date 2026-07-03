import pandas as pd


def _parse_dates(series_str, errors="coerce", utc=True):
    try:
        return pd.to_datetime(
            series_str,
            format="mixed",
            errors=errors,
            utc=utc
        )
    except TypeError:
        return pd.to_datetime(
            series_str,
            errors=errors,
            utc=utc
        )


def detect_date_columns(df):
    date_cols = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            continue
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_cols.append(str(col))
            continue
        sample = df[col].dropna().head(100).astype(str)
        if sample.empty:
            continue
        parsed = _parse_dates(sample)
        if parsed.notna().mean() >= 0.8:
            parsed_years = parsed.dt.year.dropna()
            if len(parsed_years) > 0:
                avg_year = parsed_years.mean()
                if avg_year < 1900 or avg_year > 2100:
                    continue
            date_cols.append(str(col))
    return date_cols


def is_date_column(series, threshold=0.8):
    if len(series) == 0:
        return False
    if pd.api.types.is_datetime64_any_dtype(series):
        return True
    if pd.api.types.is_numeric_dtype(series):
        return False
    s = series.dropna().head(100).astype(str)
    if len(s) == 0:
        return False
    parsed = _parse_dates(s)
    rate = parsed.notna().sum() / len(s)
    if rate >= threshold:
        parsed_years = parsed.dt.year.dropna()
        if len(parsed_years) > 0:
            avg_year = parsed_years.mean()
            if avg_year < 1900 or avg_year > 2100:
                return False
        return True
    return False
