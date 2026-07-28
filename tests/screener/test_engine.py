from src.screener.engine import ScreenerEngine


def test_engine_loads():
    engine = ScreenerEngine()
    df = engine.load_data()
    assert len(df) > 0
    engine.close()


def test_filter_returns_dataframe():
    engine = ScreenerEngine()
    df = engine.load_data()
    filtered = engine.apply_filters(df)
    assert filtered is not None
    engine.close()