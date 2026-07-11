import pandas as pd


class DataValidator:

    def __init__(self):
        self.failures = []

    def add_failure(self, rule, severity, table, message):
        self.failures.append({
            "Rule": rule,
            "Severity": severity,
            "Table": table,
            "Message": message
        })

    def validate_pk(self, df, column, table):
        duplicates = df[df[column].duplicated()]

        if not duplicates.empty:
            self.add_failure(
                "DQ-01",
                "CRITICAL",
                table,
                f"Duplicate values found in {column}"
            )

    def validate_positive_sales(self, df):
        if "Sales" in df.columns:
            if (df["Sales"] <= 0).any():
                self.add_failure(
                    "DQ-06",
                    "WARNING",
                    "profitandloss",
                    "Sales should be positive"
                )

    def save_report(self):
        report = pd.DataFrame(self.failures)
        report.to_csv("output/validation_failures.csv", index=False)
        print("Validation report saved.")