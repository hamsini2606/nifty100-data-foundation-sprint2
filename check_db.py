import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("Tables:")
print(tables)

conn.close()