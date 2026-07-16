import pandas as pd


class DataValidator:

    def __init__(self):
        self.failures = []

    def add_failure(self, rule, severity, table, message):
        self.failures.append({
            "rule": rule,
            "severity": severity,
            "table": table,
            "message": message
        })

    def check_pk_uniqueness(self, df, column, table):
        duplicates = df[df[column].duplicated(keep=False)]

        if not duplicates.empty:
            self.add_failure(
                "DQ-01",
                "CRITICAL",
                table,
                f"Duplicate values found in {column}"
            )

    def check_company_year_unique(self, df, table):
        if "company_id" in df.columns and "year" in df.columns:
            duplicates = df[
                df.duplicated(
                    subset=["company_id", "year"],
                    keep=False
                )
            ]

            if not duplicates.empty:
                self.add_failure(
                    "DQ-02",
                    "CRITICAL",
                    table,
                    "Duplicate company_id and year combination"
                )

    def check_foreign_keys(self, df, company_ids, table):
        if "company_id" in df.columns:
            invalid = df[
                ~df["company_id"].isin(company_ids)
            ]

            if not invalid.empty:
                self.add_failure(
                    "DQ-03",
                    "CRITICAL",
                    table,
                    "Invalid company_id found"
                )

    def check_balance_sheet(self, df):
        required = [
            "total_assets",
            "total_liabilities",
            "equity"
        ]

        if all(col in df.columns for col in required):
            calculated = (
                df["total_liabilities"] +
                df["equity"]
            )

            difference = (
                abs(df["total_assets"] - calculated)
                /
                df["total_assets"].replace(0, 1)
            )

            if (difference > 0.01).any():
                self.add_failure(
                    "DQ-04",
                    "WARNING",
                    "balancesheet",
                    "Balance sheet difference exceeds 1%"
                )

    def check_opm(self, df):
        required = [
            "sales",
            "operating_profit",
            "opm_percentage"
        ]

        if all(col in df.columns for col in required):
            calculated_opm = (
                df["operating_profit"]
                /
                df["sales"]
                *
                100
            )

            difference = abs(
                calculated_opm -
                df["opm_percentage"]
            )

            if (difference > 1).any():
                self.add_failure(
                    "DQ-05",
                    "WARNING",
                    "profitandloss",
                    "OPM does not match calculated value"
                )

    def check_positive_sales(self, df):
        if "sales" in df.columns:
            invalid = df[df["sales"] <= 0]

            if not invalid.empty:
                self.add_failure(
                    "DQ-06",
                    "WARNING",
                    "profitandloss",
                    "Sales must be positive"
                )

    def check_net_cash(self, df):
        required = [
            "borrowings",
            "investments",
            "cash"
        ]

        if all(col in df.columns for col in required):
            net_cash = (
                df["borrowings"]
                -
                df["investments"]
                -
                df["cash"]
            )

            if net_cash.isnull().any():
                self.add_failure(
                    "DQ-07",
                    "WARNING",
                    "balancesheet",
                    "Net cash contains null values"
                )

    def check_tax_rate(self, df):
        required = [
            "tax",
            "profit_before_tax"
        ]

        if all(col in df.columns for col in required):
            tax_rate = (
                df["tax"]
                /
                df["profit_before_tax"]
                *
                100
            )

            invalid = df[
                (tax_rate < -100) |
                (tax_rate > 100)
            ]

            if not invalid.empty:
                self.add_failure(
                    "DQ-08",
                    "WARNING",
                    "profitandloss",
                    "Invalid tax rate"
                )

    def check_dividend_cap(self, df):
        required = [
            "dividend",
            "net_profit"
        ]

        if all(col in df.columns for col in required):
            invalid = df[
                df["dividend"] > df["net_profit"]
            ]

            if not invalid.empty:
                self.add_failure(
                    "DQ-09",
                    "WARNING",
                    "profitandloss",
                    "Dividend exceeds net profit"
                )

    def check_url(self, df):
        if "url" in df.columns:
            invalid = df[
                df["url"].notna() &
                ~df["url"]
                .astype(str)
                .str.startswith(
                    ("http://", "https://")
                )
            ]

            if not invalid.empty:
                self.add_failure(
                    "DQ-10",
                    "WARNING",
                    "documents",
                    "Invalid URL format"
                )

    def check_eps_sign(self, df):
        required = [
            "eps",
            "net_profit"
        ]

        if all(col in df.columns for col in required):
            invalid = df[
                (
                    (df["net_profit"] > 0) &
                    (df["eps"] < 0)
                )
                |
                (
                    (df["net_profit"] < 0) &
                    (df["eps"] > 0)
                )
            ]

            if not invalid.empty:
                self.add_failure(
                    "DQ-11",
                    "WARNING",
                    "profitandloss",
                    "EPS sign does not match net profit"
                )

    def check_mandatory_fields(self, df, columns, table):
        for column in columns:
            if column in df.columns:
                if df[column].isnull().any():
                    self.add_failure(
                        "DQ-12",
                        "CRITICAL",
                        table,
                        f"Null values found in {column}"
                    )

    def check_year_coverage(self, df, table):
        if "year" in df.columns:
            if df["year"].nunique() < 5:
                self.add_failure(
                    "DQ-13",
                    "WARNING",
                    table,
                    "Less than 5 years of data"
                )

    def check_duplicate_ticker(self, df):
        if "ticker" in df.columns:
            if df["ticker"].duplicated().any():
                self.add_failure(
                    "DQ-14",
                    "CRITICAL",
                    "companies",
                    "Duplicate ticker found"
                )

    def save_report(
        self,
        path="output/validation_failures.csv"
    ):
        report = pd.DataFrame(self.failures)
        report.to_csv(path, index=False)

        print(
            f"Validation report saved to {path}"
        )