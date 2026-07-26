def safe_divide(numerator, denominator):
    if denominator is None or denominator == 0:
        return None

    return numerator / denominator


def net_profit_margin(net_profit, sales):
    """
    NPM = Net Profit / Sales * 100
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    OPM = Operating Profit / Sales * 100
    """

    if sales == 0:
        return None

    return (operating_profit / sales) * 100


def opm_mismatch(computed_opm, source_opm, threshold=1.0):
    """
    Returns True if computed OPM differs from source OPM by > 1 percentage point.
    """

    if computed_opm is None or source_opm is None:
        return False

    return abs(computed_opm - source_opm) > threshold


def return_on_equity(net_profit, equity_capital, reserves):
    """
    ROE = Net Profit / (Equity Capital + Reserves) * 100

    Return None for zero or negative equity.
    """

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return (net_profit / total_equity) * 100


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings
):
    """
    ROCE = EBIT /
    (Equity Capital + Reserves + Borrowings) * 100
    """

    capital_employed = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital_employed == 0:
        return None

    return (ebit / capital_employed) * 100


def return_on_assets(net_profit, total_assets):
    """
    ROA = Net Profit / Total Assets * 100
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


def debt_to_equity(
    borrowings,
    equity_capital,
    reserves
):
    """
    D/E = Borrowings / Total Equity

    Debt-free companies return 0.
    """

    if borrowings == 0:
        return 0

    total_equity = equity_capital + reserves

    if total_equity == 0:
        return None

    return borrowings / total_equity


def high_leverage_flag(debt_equity, broad_sector):
    """
    Flag D/E > 5 except Financials sector.
    """

    if debt_equity is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_equity > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    ICR = (Operating Profit + Other Income) / Interest
    """

    if interest == 0:
        return None

    return (
        operating_profit + other_income
    ) / interest


def get_icr_label(icr):
    """
    Debt-free label for companies with zero interest.
    """

    if icr is None:
        return "Debt Free"

    return None


def get_icr_warning(icr):
    """
    ICR below 1.5 indicates risk.
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    """
    Net Debt = Borrowings - Investments
    """

    return borrowings - investments


def asset_turnover(sales, total_assets):
    """
    Asset Turnover = Sales / Total Assets
    """

    if total_assets == 0:
        return None

    return sales / total_assets