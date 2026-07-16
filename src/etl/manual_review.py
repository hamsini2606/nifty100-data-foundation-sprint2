import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"


def manual_review():

    conn = sqlite3.connect(DB_PATH)

    print("\n========== MANUAL DATA REVIEW ==========\n")

    # 1. Randomly select 5 companies
    companies = pd.read_sql_query(
        """
        SELECT *
        FROM companies
        ORDER BY RANDOM()
        LIMIT 5
        """,
        conn
    )

    print("----- 5 RANDOM COMPANIES -----")
    print(companies.to_string(index=False))

    # 2. Year coverage
    print("\n----- YEAR COVERAGE -----")

    year_coverage = pd.read_sql_query(
        """
        SELECT
            company_id,
            COUNT(DISTINCT year) AS years_available,
            MIN(year) AS first_year,
            MAX(year) AS last_year
        FROM financial_ratios
        GROUP BY company_id
        ORDER BY years_available
        """,
        conn
    )

    print(
        year_coverage.to_string(index=False)
    )

    # 3. Companies with less than 5 years
    print(
        "\n----- COMPANIES WITH LESS THAN 5 YEARS -----"
    )

    less_than_five = year_coverage[
        year_coverage["years_available"] < 5
    ]

    if less_than_five.empty:

        print(
            "PASS: No companies have less than 5 years"
        )

    else:

        print(
            less_than_five.to_string(
                index=False
            )
        )

    # 4. Check missing company IDs
    print(
        "\n----- MISSING COMPANY IDs -----"
    )

    missing_ids = pd.read_sql_query(
        """
        SELECT COUNT(*) AS missing_count
        FROM financial_ratios fr
        LEFT JOIN companies c
        ON fr.company_id = c.company_id
        WHERE c.company_id IS NULL
        """,
        conn
    )

    print(missing_ids)

    # 5. Check duplicate company-year records
    print(
        "\n----- DUPLICATE COMPANY-YEAR RECORDS -----"
    )

    duplicates = pd.read_sql_query(
        """
        SELECT
            company_id,
            year,
            COUNT(*) AS count
        FROM financial_ratios
        GROUP BY company_id, year
        HAVING COUNT(*) > 1
        """,
        conn
    )

    if duplicates.empty:

        print(
            "PASS: No duplicate company-year records"
        )

    else:

        print(
            duplicates.to_string(
                index=False
            )
        )

    conn.close()

    print(
        "\n========== MANUAL REVIEW COMPLETE =========="
    )


if __name__ == "__main__":

    manual_review()