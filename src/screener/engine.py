import sqlite3
import pandas as pd
import yaml
from src.screener.presets import PRESETS
from src.screener.composite import calculate_composite_score


DB_PATH = "db/nifty100.db"
CONFIG_PATH = "config/screener_config.yaml"


class ScreenerEngine:

    def __init__(self):

        with open(CONFIG_PATH, "r") as f:
            self.config = yaml.safe_load(f)

        self.conn = sqlite3.connect(DB_PATH)
     

    def load_data(self):

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        try:
            market = pd.read_sql(
                "SELECT * FROM market_cap",
                self.conn
            )

            ratios = ratios.merge(
                market,
                on=["company_id", "year"],
                how="left"
            )

        except Exception:
            pass

        return ratios

    def apply_filters(self, df, filters=None):

        if filters is None:
            filters = self.config["filters"]


        result = df.copy()

        mapping = {
            "roe_min": ("return_on_equity_pct", ">="),
            "debt_to_equity_max": ("debt_to_equity", "<="),
            "free_cash_flow_min": ("free_cash_flow_cr", ">="),
            "revenue_cagr_5yr_min": ("revenue_cagr_5yr", ">="),
            "pat_cagr_5yr_min": ("pat_cagr_5yr", ">="),
            "operating_profit_margin_min": ("operating_profit_margin_pct", ">="),
            "pe_ratio_max": ("pe_ratio", "<="),
            "pb_ratio_max": ("pb_ratio", "<="),
            "dividend_yield_min": ("dividend_yield_pct", ">="),
            "interest_coverage_min": ("interest_coverage", ">="),
            "market_cap_min": ("market_cap_crore", ">="),
            "net_profit_min": ("net_profit_margin_pct", ">="),
            "eps_cagr_5yr_min": ("eps_cagr_5yr", ">="),
            "asset_turnover_min": ("asset_turnover", ">="),
            "sales_min": ("sales", ">=")
        }

        for key, value in filters.items():

            if key not in mapping:
                continue

            column, operator = mapping[key]

            if column not in result.columns:
                continue

            if operator == ">=":
                result = result[result[column].fillna(-999999) >= value]

            else:
                result = result[result[column].fillna(999999) <= value]

        if "composite_quality_score" not in result.columns:
            result["composite_quality_score"] = calculate_composite_score(result)

        result = result.sort_values(
            by="composite_quality_score",
            ascending=False
        )

        return result

    def close(self):
        self.conn.close()
    def run_preset(self, preset_name):
       

       if preset_name not in PRESETS:
        raise ValueError("Invalid preset")

       df = self.load_data()

       return self.apply_filters(df, PRESETS[preset_name])    


if __name__ == "__main__":

    engine = ScreenerEngine()

    df = engine.load_data()

    for preset in PRESETS:

     print("=" * 60)

     print(preset.upper())

     result = engine.run_preset(preset)

     print(result[["company_id", "year"]].head())
     print("Companies:", len(result))