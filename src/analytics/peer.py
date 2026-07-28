import sqlite3
import pandas as pd
import os

DB = "db/nifty100.db"


def calculate_peer_percentiles():

    conn = sqlite3.connect(DB)

    ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
    peers = pd.read_sql("SELECT * FROM peer_groups", conn)

    df = ratios.merge(
        peers[["company_id", "peer_group_name"]],
        on="company_id",
        how="left"
    )

    metrics = [
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "interest_coverage",
        "asset_turnover",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr"
    ]

    rows = []

    for group in df["peer_group_name"].dropna().unique():

        grp = df[df["peer_group_name"] == group]

        for metric in metrics:

            if metric not in grp.columns:
                continue

            ranks = grp[metric].rank(pct=True)

            for i, r in grp.iterrows():

                rows.append({
                    "company_id": r["company_id"],
                    "peer_group_name": group,
                    "metric": metric,
                    "value": r[metric],
                    "percentile_rank": ranks.loc[i],
                    "year": r["year"]
                })

    result = pd.DataFrame(rows)

    result.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    os.makedirs("output", exist_ok=True)

    result.to_excel(
        "output/peer_percentiles.xlsx",
        index=False
    )

    conn.close()

    print(result.head())
    print("Rows:", len(result))


if __name__ == "__main__":
    calculate_peer_percentiles()