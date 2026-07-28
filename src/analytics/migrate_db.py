"""
Database Migration
Adds Sprint 2 KPI columns to financial_ratios table.
"""

import sqlite3


DB_PATH = "db/nifty100.db"


COLUMNS = {

    "net_profit_margin_pct": "REAL",

    "operating_profit_margin_pct": "REAL",

    "return_on_equity_pct": "REAL",

    "return_on_capital_employed_pct": "REAL",

    "return_on_assets_pct": "REAL",

    "debt_to_equity": "REAL",

    "high_leverage_flag": "INTEGER",

    "interest_coverage": "REAL",

    "icr_label": "TEXT",

    "icr_warning_flag": "INTEGER",

    "net_debt_cr": "REAL",

    "asset_turnover": "REAL",

    "free_cash_flow_cr": "REAL",

    "capex_cr": "REAL",

    "earnings_per_share": "REAL",

    "book_value_per_share": "REAL",

    "dividend_payout_ratio_pct": "REAL",

    "total_debt_cr": "REAL",

    "cash_from_operations_cr": "REAL",

    "revenue_cagr_5yr": "REAL",

    "revenue_cagr_5yr_flag": "TEXT",

    "pat_cagr_5yr": "REAL",

    "pat_cagr_5yr_flag": "TEXT",

    "eps_cagr_5yr": "REAL",

    "eps_cagr_5yr_flag": "TEXT",

    "composite_quality_score": "REAL"
}


def migrate_database():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    # Check whether table exists
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='financial_ratios'
    """)

    table_exists = cursor.fetchone()

    if table_exists is None:

        print(
            "ERROR: financial_ratios table does not exist."
        )

        connection.close()

        return

    # Get existing columns
    cursor.execute(
        "PRAGMA table_info(financial_ratios)"
    )

    existing_columns = {
        row[1]
        for row in cursor.fetchall()
    }

    # Add missing columns
    for column_name, data_type in COLUMNS.items():

        if column_name not in existing_columns:

            sql = f"""
                ALTER TABLE financial_ratios
                ADD COLUMN {column_name} {data_type}
            """

            cursor.execute(sql)

            print(
                f"Added column: {column_name}"
            )

    connection.commit()

    connection.close()

    print(
        "\nDatabase migration completed successfully."
    )


if __name__ == "__main__":
    migrate_database()