import sqlite3
import logging
from pathlib import Path

import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    interest_coverage_ratio,
    get_icr_label,
    get_icr_warning
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capital_allocation_pattern
)

from src.analytics.cagr import calculate_cagr


DB_PATH = "db/nifty100.db"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=OUTPUT_DIR / "ratio_edge_cases.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def clean_year(year):
    """
    Convert:
    Mar 2014 -> 2014
    Mar-14  -> 2014
    Dec 2012 -> 2012
    TTM      -> None
    """

    year = str(year).strip()

    if year.upper() == "TTM":
        return None

    try:

        if "-" in year:

            last_part = year.split("-")[-1]

            if len(last_part) == 2:
                return 2000 + int(last_part)

        parts = year.split()

        for part in parts:

            if len(part) == 4 and part.isdigit():
                return int(part)

    except Exception:

        return None

    return None


def calculate_company_cagr(
    company_df,
    value_column,
    years
):
    """
    Calculate CAGR using exact year difference.
    """

    df = company_df.copy()

    df["year_num"] = df["year"].apply(clean_year)

    df = df.dropna(
        subset=["year_num", value_column]
    )

    df = df.sort_values("year_num")

    if df.empty:
        return None, "INSUFFICIENT"

    end_row = df.iloc[-1]

    end_year = int(end_row["year_num"])

    target_year = end_year - years

    start_rows = df[
        df["year_num"] == target_year
    ]

    if start_rows.empty:
        return None, "INSUFFICIENT"

    start_value = start_rows.iloc[0][value_column]

    end_value = end_row[value_column]

    return calculate_cagr(
        start_value,
        end_value,
        years
    )


def build_cagr_data(pnl):

    cagr_results = {}

    for company_id, company_df in pnl.groupby("company_id"):

        cagr_results[company_id] = {}

        for metric in [
            "sales",
            "net_profit",
            "eps"
        ]:

            for years in [3, 5, 10]:

                value, flag = calculate_company_cagr(
                    company_df,
                    metric,
                    years
                )

                cagr_results[company_id][
                    f"{metric}_{years}yr"
                ] = value

                cagr_results[company_id][
                    f"{metric}_{years}yr_flag"
                ] = flag

    return cagr_results


def generate_capital_allocation(cashflow, pnl):

    print("Generating capital allocation file...")

    merged = pd.merge(
        cashflow,
        pnl[
            [
                "company_id",
                "year",
                "net_profit"
            ]
        ],
        on=[
            "company_id",
            "year"
        ],
        how="left"
    )

    output = []

    for _, row in merged.iterrows():

        cfo = row["operating_activity"]

        cfi = row["investing_activity"]

        cff = row["financing_activity"]

        pat = row["net_profit"]

        if pd.isna(cfo):
            cfo = 0

        if pd.isna(cfi):
            cfi = 0

        if pd.isna(cff):
            cff = 0

        if pd.isna(pat):
            pat = 0

        # Sign logic
        cfo_sign = "+" if cfo > 0 else "-"

        cfi_sign = "+" if cfi > 0 else "-"

        cff_sign = "+" if cff > 0 else "-"

        # CFO/PAT quality
        high_cfo_pat = False

        if pat != 0:

            cfo_pat_ratio = cfo / pat

            high_cfo_pat = cfo_pat_ratio > 1.0

        pattern_label = capital_allocation_pattern(
            cfo,
            cfi,
            cff,
            high_cfo_pat
        )

        output.append({

            "company_id": row["company_id"],

            "year": row["year"],

            "cfo_sign": cfo_sign,

            "cfi_sign": cfi_sign,

            "cff_sign": cff_sign,

            "pattern_label": pattern_label

        })

    result = pd.DataFrame(output)

    result.to_csv(
        OUTPUT_DIR / "capital_allocation.csv",
        index=False
    )

    print(
        "Created:",
        OUTPUT_DIR / "capital_allocation.csv"
    )


def run_engine():

    print("Starting Sprint 2 Engine...")

    conn = sqlite3.connect(DB_PATH)

    pnl = pd.read_sql_query(
        "SELECT * FROM profit_loss_raw",
        conn
    )

    cashflow = pd.read_sql_query(
        "SELECT * FROM cash_flow_raw",
        conn
    )

    print(
        "P&L records:",
        len(pnl)
    )

    print(
        "Cash Flow records:",
        len(cashflow)
    )

    # Remove TTM from annual calculations
    pnl = pnl[
        pnl["year"].astype(str).str.upper() != "TTM"
    ]

    cashflow = cashflow[
        cashflow["year"].astype(str).str.upper() != "TTM"
    ]

    # Build CAGR dictionary
    print("Calculating CAGR metrics...")

    cagr_data = build_cagr_data(pnl)

    # Merge P&L + Cash Flow
    merged = pd.merge(
        pnl,
        cashflow,
        on=[
            "company_id",
            "year"
        ],
        how="left"
    )

    output = []

    for _, row in merged.iterrows():

        sales = row["sales"]

        net_profit = row["net_profit"]

        operating_profit = row["operating_profit"]

        other_income = row["other_income"]

        interest = row["interest"]

        cfo = row["operating_activity"]

        cfi = row["investing_activity"]

        if pd.isna(cfo):
            cfo = 0

        if pd.isna(cfi):
            cfi = 0

        npm = net_profit_margin(
            net_profit,
            sales
        )

        opm = operating_profit_margin(
            operating_profit,
            sales
        )

        icr = interest_coverage_ratio(
            operating_profit,
            other_income,
            interest
        )

        fcf = free_cash_flow(
            cfo,
            cfi
        )

        company_id = row["company_id"]

        cagr = cagr_data.get(
            company_id,
            {}
        )

        output.append({

            "company_id": company_id,

            "year": row["year"],

            "net_profit_margin_pct": npm,

            "operating_profit_margin_pct": opm,

            "interest_coverage": icr,

            "icr_label": get_icr_label(icr),

            "icr_warning_flag": get_icr_warning(icr),

            "free_cash_flow_cr": fcf,

            "capex_cr": abs(cfi),

            "earnings_per_share": row["eps"],

            "dividend_payout_ratio_pct": row["dividend_payout"],

            "cash_from_operations_cr": cfo,

            "revenue_cagr_3yr": cagr.get(
                "sales_3yr"
            ),

            "revenue_cagr_3yr_flag": cagr.get(
                "sales_3yr_flag"
            ),

            "revenue_cagr_5yr": cagr.get(
                "sales_5yr"
            ),

            "revenue_cagr_5yr_flag": cagr.get(
                "sales_5yr_flag"
            ),

            "revenue_cagr_10yr": cagr.get(
                "sales_10yr"
            ),

            "revenue_cagr_10yr_flag": cagr.get(
                "sales_10yr_flag"
            ),

            "pat_cagr_3yr": cagr.get(
                "net_profit_3yr"
            ),

            "pat_cagr_3yr_flag": cagr.get(
                "net_profit_3yr_flag"
            ),

            "pat_cagr_5yr": cagr.get(
                "net_profit_5yr"
            ),

            "pat_cagr_5yr_flag": cagr.get(
                "net_profit_5yr_flag"
            ),

            "pat_cagr_10yr": cagr.get(
                "net_profit_10yr"
            ),

            "pat_cagr_10yr_flag": cagr.get(
                "net_profit_10yr_flag"
            ),

            "eps_cagr_3yr": cagr.get(
                "eps_3yr"
            ),

            "eps_cagr_3yr_flag": cagr.get(
                "eps_3yr_flag"
            ),

            "eps_cagr_5yr": cagr.get(
                "eps_5yr"
            ),

            "eps_cagr_5yr_flag": cagr.get(
                "eps_5yr_flag"
            ),

            "eps_cagr_10yr": cagr.get(
                "eps_10yr"
            ),

            "eps_cagr_10yr_flag": cagr.get(
                "eps_10yr_flag"
            )

        })

    result_df = pd.DataFrame(output)

    print(
        "Calculated rows:",
        len(result_df)
    )

    # Save result
    result_df.to_sql(
        "financial_ratios",
        conn,
        if_exists="replace",
        index=False
    )

    # Generate capital allocation CSV
    generate_capital_allocation(
        cashflow,
        pnl
    )

    conn.close()

    print(
        "financial_ratios table populated!"
    )


if __name__ == "__main__":

    run_engine()