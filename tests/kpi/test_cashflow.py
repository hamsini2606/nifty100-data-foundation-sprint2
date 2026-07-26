from src.analytics.cashflow_kpis import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)


def test_free_cash_flow():

    assert free_cash_flow(
        100,
        -40
    ) == 60


def test_negative_free_cash_flow():

    assert free_cash_flow(
        50,
        -100
    ) == -50


def test_capex_intensity():

    assert capex_intensity(
        -50,
        1000
    ) == 5


def test_fcf_conversion_zero_profit():

    assert fcf_conversion_rate(
        100,
        0
    ) is None


def test_capital_allocation():

    result = capital_allocation_pattern(
        100,
        -50,
        -20
    )

    assert result == "Reinvestor"