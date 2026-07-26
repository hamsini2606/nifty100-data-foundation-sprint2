import sqlite3

DB_PATH = "db/nifty100.db"


REQUIRED_COLUMNS = {
    "return_on_equity_pct": "REAL",
    "return_on_capital_employed_pct": "REAL",
    "debt_to_equity": "REAL",
    "high_leverage_flag": "INTEGER",
    "asset_turnover": "REAL",
    "roa_pct": "REAL",
    "net_debt_cr": "REAL",

    "icr_label": "TEXT",
    "icr_warning_flag": "INTEGER",

    "revenue_cagr_3yr": "REAL",
    "revenue_cagr_3yr_flag": "TEXT",
    "revenue_cagr_5yr": "REAL",
    "revenue_cagr_5yr_flag": "TEXT",
    "revenue_cagr_10yr": "REAL",
    "revenue_cagr_10yr_flag": "TEXT",

    "pat_cagr_3yr": "REAL",
    "pat_cagr_3yr_flag": "TEXT",
    "pat_cagr_5yr": "REAL",
    "pat_cagr_5yr_flag": "TEXT",
    "pat_cagr_10yr": "REAL",
    "pat_cagr_10yr_flag": "TEXT",

    "eps_cagr_3yr": "REAL",
    "eps_cagr_3yr_flag": "TEXT",
    "eps_cagr_5yr": "REAL",
    "eps_cagr_5yr_flag": "TEXT",
    "eps_cagr_10yr": "REAL",
    "eps_cagr_10yr_flag": "TEXT",

    "composite_quality_score": "REAL"
}


def upgrade_schema():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "PRAGMA table_info(financial_ratios)"
    )

    existing_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    added = 0

    for column, data_type in REQUIRED_COLUMNS.items():

        if column not in existing_columns:

            sql = f"""
            ALTER TABLE financial_ratios
            ADD COLUMN {column} {data_type}
            """

            cursor.execute(sql)

            print(
                f"Added column: {column}"
            )

            added += 1

    conn.commit()

    conn.close()

    print(
        f"\nSchema upgrade complete. "
        f"Columns added: {added}"
    )


if __name__ == "__main__":

    upgrade_schema()