from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_assets
)


def test_npm_normal():
    assert net_profit_margin(100, 1000) == 10


def test_npm_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_opm_normal():
    assert operating_profit_margin(200, 1000) == 20


def test_roe_negative_equity():
    assert return_on_equity(100, -150, 100) is None


def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None