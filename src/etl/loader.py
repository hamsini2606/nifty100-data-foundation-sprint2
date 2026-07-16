import sqlite3
from pathlib import Path
import pandas as pd


DB_PATH = "db/nifty100.db"
RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    audit = []

    # -----------------------------
    # 1. COMPANIES
    # -----------------------------

    companies_df = pd.read_excel(
        RAW_DIR / "Companies.xlsx"
    )

    companies = pd.DataFrame({
        "company_id": companies_df["Ticker"].str.upper(),
        "company_name": companies_df["Company"],
        "ticker": companies_df["Ticker"].str.upper(),
        "sector": None
    })

    companies.to_sql(
        "companies",
        conn,
        if_exists="append",
        index=False
    )

    audit.append({
        "table": "companies",
        "rows_loaded": len(companies),
        "rows_rejected": 0,
        "status": "SUCCESS"
    })

    print(
        f"Companies loaded: {len(companies)}"
    )

    # Get valid company IDs
    valid_company_ids = set(
        companies["company_id"]
    )

    # -----------------------------
    # 2. FINANCIAL RATIOS
    # -----------------------------

    df = pd.read_excel(
        RAW_DIR / "financial_ratios.xlsx"
    )

    original_count = len(df)

    df = df[
        df["company_id"].isin(
            valid_company_ids
        )
    ]

    rejected = original_count - len(df)

    df.to_sql(
        "financial_ratios",
        conn,
        if_exists="append",
        index=False
    )

    audit.append({
        "table": "financial_ratios",
        "rows_loaded": len(df),
        "rows_rejected": rejected,
        "status": "SUCCESS"
    })

    print(
        f"Financial ratios loaded: {len(df)}"
    )

    # -----------------------------
    # 3. MARKET CAP
    # -----------------------------

    df = pd.read_excel(
        RAW_DIR / "market_cap.xlsx"
    )

    original_count = len(df)

    df = df[
        df["company_id"].isin(
            valid_company_ids
        )
    ]

    rejected = original_count - len(df)

    df.to_sql(
        "market_cap",
        conn,
        if_exists="append",
        index=False
    )

    audit.append({
        "table": "market_cap",
        "rows_loaded": len(df),
        "rows_rejected": rejected,
        "status": "SUCCESS"
    })

    print(
        f"Market cap loaded: {len(df)}"
    )

    # -----------------------------
    # 4. PEER GROUPS
    # -----------------------------

    df = pd.read_excel(
        RAW_DIR / "peer_groups.xlsx"
    )

    original_count = len(df)

    df = df[
        df["company_id"].isin(
            valid_company_ids
        )
    ]

    rejected = original_count - len(df)

    df.to_sql(
        "peer_groups",
        conn,
        if_exists="append",
        index=False
    )

    audit.append({
        "table": "peer_groups",
        "rows_loaded": len(df),
        "rows_rejected": rejected,
        "status": "SUCCESS"
    })

    print(
        f"Peer groups loaded: {len(df)}"
    )

    # -----------------------------
    # 5. SECTORS
    # -----------------------------

    df = pd.read_excel(
        RAW_DIR / "sectors.xlsx"
    )

    original_count = len(df)

    df = df[
        df["company_id"].isin(
            valid_company_ids
        )
    ]

    rejected = original_count - len(df)

    df.to_sql(
        "sectors",
        conn,
        if_exists="append",
        index=False
    )

    audit.append({
        "table": "sectors",
        "rows_loaded": len(df),
        "rows_rejected": rejected,
        "status": "SUCCESS"
    })

    print(
        f"Sectors loaded: {len(df)}"
    )

    # -----------------------------
    # 6. STOCK PRICES
    # -----------------------------

    df = pd.read_excel(
        RAW_DIR / "stock_prices.xlsx"
    )

    original_count = len(df)

    df = df[
        df["company_id"].isin(
            valid_company_ids
        )
    ]

    rejected = original_count - len(df)

    df.to_sql(
        "stock_prices",
        conn,
        if_exists="append",
        index=False
    )

    audit.append({
        "table": "stock_prices",
        "rows_loaded": len(df),
        "rows_rejected": rejected,
        "status": "SUCCESS"
    })

    print(
        f"Stock prices loaded: {len(df)}"
    )

    # -----------------------------
    # FINAL CHECK
    # -----------------------------

    conn.commit()

    fk_errors = conn.execute(
        "PRAGMA foreign_key_check"
    ).fetchall()

    print(
        f"\nForeign Key Errors: {len(fk_errors)}"
    )

    conn.close()

    audit_df = pd.DataFrame(audit)

    audit_df.to_csv(
        OUTPUT_DIR / "load_audit.csv",
        index=False
    )

    print(
        "\nLoad audit saved to:"
    )

    print(
        "output/load_audit.csv"
    )


if __name__ == "__main__":

    load_data()