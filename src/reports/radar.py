import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

try:
    df = pd.read_sql("""
        SELECT company_id,
               year,
               net_profit_margin_pct,
               operating_profit_margin_pct,
               asset_turnover,
               revenue_cagr_5yr,
               pat_cagr_5yr,
               interest_coverage,
               composite_quality_score
        FROM financial_ratios
    """, conn)
except:
    print("Required columns not found.")
    exit()

os.makedirs("reports/radar_charts", exist_ok=True)

metrics = [
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "asset_turnover",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "interest_coverage",
    "composite_quality_score"
]

angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False)
angles = np.concatenate((angles,[angles[0]]))

for _, row in df.iterrows():

    values=[]

    for m in metrics:
        if m in df.columns:
            values.append(0 if pd.isna(row[m]) else row[m])

    values.append(values[0])

    fig=plt.figure(figsize=(5,5))
    ax=plt.subplot(111,polar=True)

    ax.plot(angles,values)
    ax.fill(angles,values,alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics,fontsize=7)

    plt.title(str(row["company_id"]))

    plt.savefig(
        f"reports/radar_charts/{row['company_id']}_{row['year']}.png",
        dpi=120
    )

    plt.close()

conn.close()

print("Radar charts generated.")