import sqlite3
import pandas as pd


DB_PATH = "db/nifty100.db"


def load_data():

    conn = sqlite3.connect(DB_PATH)

    print("Loading Profit & Loss...")

    profit_loss = pd.read_excel(
        "data/raw/profitandloss.xlsx",
        sheet_name="Profit & Loss",
        header=1
    )

    print("P&L columns:")
    print(profit_loss.columns.tolist())

    profit_loss.to_sql(
        "profit_loss_raw",
        conn,
        if_exists="replace",
        index=False
    )

    print("Loading Cash Flow...")

    cash_flow = pd.read_excel(
        "data/raw/cashflow.xlsx",
        header=1
    )

    print("Cash Flow columns:")
    print(cash_flow.columns.tolist())

    cash_flow.to_sql(
        "cash_flow_raw",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("\nData loaded successfully!")
    print(f"Profit & Loss rows: {len(profit_loss)}")
    print(f"Cash Flow rows: {len(cash_flow)}")


if __name__ == "__main__":
    load_data()