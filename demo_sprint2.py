import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    company_id,
    year,
    net_profit_margin_pct,
    operating_profit_margin_pct,
    interest_coverage,
    free_cash_flow_cr,
    earnings_per_share,
    revenue_cagr_5yr,
    pat_cagr_5yr,
    eps_cagr_5yr
FROM financial_ratios
LIMIT 5
"""

df = pd.read_sql_query(query, conn)

print("\nSPRINT 2 FINANCIAL RATIO DEMO")
print("=" * 80)
print(df.to_string(index=False))

conn.close()