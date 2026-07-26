from src.analytics.ratios import (
    debt_to_equity,
    interest_coverage_ratio,
    get_icr_label,
    get_icr_warning
)


def test_debt_free_company():
    assert debt_to_equity(0, 100, 100) == 0


def test_debt_to_equity_normal():
    assert debt_to_equity(200, 100, 100) == 1


def test_interest_zero():
    assert interest_coverage_ratio(
        100,
        20,
        0
    ) is None


def test_debt_free_label():
    assert get_icr_label(None) == "Debt Free"


def test_low_interest_coverage_warning():
    assert get_icr_warning(1.0) is True