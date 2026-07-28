import sqlite3

conn=sqlite3.connect("db/nifty100.db")

print("="*50)

print("Financial Ratios")
print(conn.execute(
"SELECT COUNT(*) FROM financial_ratios"
).fetchone())

print()

print("Peer Percentiles")
print(conn.execute(
"SELECT COUNT(*) FROM peer_percentiles"
).fetchone())

print()

print("Tables")

for t in conn.execute(
"SELECT name FROM sqlite_master WHERE type='table'"
):
    print(t[0])

conn.close()

print("\nSprint 3 Validation Complete")