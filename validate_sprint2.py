import sqlite3
from pathlib import Path
import pandas as pd


DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("=" * 60)
print("SPRINT 2 FINAL VALIDATION")
print("=" * 60)


# 1. Row count
row_count = conn.execute(
    "SELECT COUNT(*) FROM financial_ratios"
).fetchone()[0]

print(f"\n1. Financial Ratios Rows: {row_count}")

if row_count >= 1100:
    print("   PASS")
else:
    print("   FAIL")


# 2. Required columns
required_columns = [
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "interest_coverage",
    "free_cash_flow_cr",
    "capex_cr",
    "earnings_per_share",
    "cash_from_operations_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "debt_to_equity",
    "asset_turnover",
    "roa_pct",
    "net_debt_cr",
    "composite_quality_score"
]

existing_columns = [
    row[1]
    for row in conn.execute(
        "PRAGMA table_info(financial_ratios)"
    ).fetchall()
]

print("\n2. Required Columns:")

missing_columns = []

for column in required_columns:

    if column in existing_columns:
        print(f"   PASS: {column}")
    else:
        print(f"   MISSING: {column}")
        missing_columns.append(column)


# 3. Null-only columns
print("\n3. Null-only Column Check:")

null_only = []

for column in existing_columns:

    if column == "id":
        continue

    total = conn.execute(
        "SELECT COUNT(*) FROM financial_ratios"
    ).fetchone()[0]

    non_null = conn.execute(
        f'SELECT COUNT("{column}") FROM financial_ratios'
    ).fetchone()[0]

    if non_null == 0:

        print(f"   FAIL: {column} is completely NULL")

        null_only.append(column)

    else:

        print(f"   PASS: {column} has {non_null}/{total} values")


# 4. Capital allocation CSV
capital_file = Path(
    "output/capital_allocation.csv"
)

print("\n4. Capital Allocation CSV:")

if capital_file.exists():

    df = pd.read_csv(capital_file)

    print("   PASS")
    print(f"   Rows: {len(df)}")
    print(
        f"   Columns: {list(df.columns)}"
    )

else:

    print("   FAIL: File not found")


# 5. Edge case log
edge_file = Path(
    "output/ratio_edge_cases.log"
)

print("\n5. Edge Case Log:")

if edge_file.exists():

    print("   PASS")

else:

    print("   FAIL: File not found")


# 6. Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if row_count >= 1100:
    print("PASS: Row count requirement")

if not missing_columns:
    print("PASS: Required columns")

else:
    print(
        "WARNING: Missing columns:",
        missing_columns
    )

if not null_only:
    print("PASS: No null-only columns")

else:
    print(
        "WARNING: Null-only columns:",
        null_only
    )

conn.close()