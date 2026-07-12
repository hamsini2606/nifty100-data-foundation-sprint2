import sqlite3

conn = sqlite3.connect("db/nifty100.db")

with open("db/schema.sql", "r") as file:
    sql_script = file.read()

conn.executescript(sql_script)

conn.commit()
conn.close()

print("Database created successfully!")