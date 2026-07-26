import sqlite3

connection = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "sectors",
    "stock_prices"
]

for table in tables:

    print("\n" + "=" * 60)
    print(f"TABLE: {table}")
    print("=" * 60)

    columns = connection.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    for column in columns:
        print(column)

connection.close()