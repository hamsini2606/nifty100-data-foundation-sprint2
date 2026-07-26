import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

columns = cursor.execute(
    "PRAGMA table_info(financial_ratios)"
).fetchall()

print("KPI NULL CHECK")
print("=" * 40)

for column in columns:

    column_name = column[1]

    if column_name == "id":
        continue

    result = cursor.execute(
        f"""
        SELECT
            COUNT(*) AS total,
            COUNT("{column_name}") AS non_null
        FROM financial_ratios
        """
    ).fetchone()

    total, non_null = result

    print(
        f"{column_name}: "
        f"{non_null}/{total} populated"
    )

conn.close()