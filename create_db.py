import sqlite3

conn = sqlite3.connect("db/nifty100.db")

with open("db/schema.sql", "r") as file:
    schema = file.read()

conn.executescript(schema)
conn.commit()
conn.close()

print("Database recreated successfully")