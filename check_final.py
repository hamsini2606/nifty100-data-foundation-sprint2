 
import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "sectors",
    "stock_prices"
]

print("\n========== FINAL DATABASE CHECK ==========\n")

for table in tables:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count} rows")

fk_errors = conn.execute(
    "PRAGMA foreign_key_check"
).fetchall()

print("\nForeign Key Errors:", len(fk_errors))

for error in fk_errors:
    print(f"Error in table {error[0]}: {error[1]}, {error[2]}, {error[3]}")

conn.close()