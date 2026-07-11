import pandas as pd
from pathlib import Path

from normaliser import normalize_year, normalize_ticker


def load_excel(file_path):

    df = pd.read_excel(file_path)

    df["Ticker"] = df["Ticker"].apply(normalize_ticker)
    df["Year"] = df["Year"].apply(normalize_year)

    return df


if __name__ == "__main__":

    df = load_excel("data/raw/companies.xlsx")

    print(df)