import pandas as pd


def normalize(series):
    if series.isna().all():
        return pd.Series([0] * len(series), index=series.index)

    mn = series.min()
    mx = series.max()

    if pd.isna(mn) or pd.isna(mx) or mx == mn:
        return pd.Series([50] * len(series), index=series.index)

    return ((series - mn) / (mx - mn) * 100).fillna(0)


def calculate_composite_score(df):

    score = pd.Series(0.0, index=df.index)

    metrics = [
        ("return_on_equity_pct", 0.15),
        ("operating_profit_margin_pct", 0.10),
        ("revenue_cagr_5yr", 0.10),
        ("pat_cagr_5yr", 0.10),
        ("free_cash_flow_cr", 0.15),
        ("interest_coverage", 0.05),
        ("asset_turnover", 0.10),
    ]

    for col, weight in metrics:
        if col in df.columns:
            score += normalize(df[col]) * weight

    return score.round(2)