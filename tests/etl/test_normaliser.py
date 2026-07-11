from src.etl.normaliser import normalize_year, normalize_ticker

def test_year():
    assert normalize_year("FY22") == 2022
    assert normalize_year("23") == 2023
    assert normalize_year("2024") == 2024
    assert normalize_year(None) is None

def test_ticker():
    assert normalize_ticker("tcs") == "TCS"
    assert normalize_ticker(" infy ") == "INFY"
    assert normalize_ticker(None) is None