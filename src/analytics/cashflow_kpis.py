def free_cash_flow(operating_activity, investing_activity):
    """
    FCF = CFO + CFI

    Negative FCF is allowed.
    """
    return operating_activity + investing_activity


def cfo_quality_score(cfo_pat_ratio):
    """
    CFO / PAT quality classification.

    > 1.0      = High Quality
    0.5 - 1.0  = Moderate
    < 0.5      = Accrual Risk
    """

    if cfo_pat_ratio is None:
        return None

    if cfo_pat_ratio > 1.0:
        return "High Quality"

    if cfo_pat_ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def calculate_cfo_pat_ratio(cfo_values, pat_values):
    """
    Average CFO / PAT ratio over available years.
    """

    ratios = []

    for cfo, pat in zip(cfo_values, pat_values):

        if pat is None or pat == 0:
            continue

        ratios.append(cfo / pat)

    if not ratios:
        return None

    return sum(ratios) / len(ratios)


def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity = |CFI| / Sales * 100
    """

    if sales == 0:
        return None

    return (abs(investing_activity) / sales) * 100


def capex_category(capex_intensity_value):
    """
    < 3%      = Asset Light
    3% - 8%   = Moderate
    > 8%      = Capital Intensive
    """

    if capex_intensity_value is None:
        return None

    if capex_intensity_value < 3:
        return "Asset Light"

    if capex_intensity_value <= 8:
        return "Moderate"

    return "Capital Intensive"


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion = FCF / Operating Profit * 100
    """

    if operating_profit == 0:
        return None

    return (fcf / operating_profit) * 100


def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    high_cfo_pat=False
):
    """
    Classifies capital allocation using CFO, CFI and CFF signs.
    """

    cfo_sign = "+" if cfo > 0 else "-"
    cfi_sign = "+" if cfi > 0 else "-"
    cff_sign = "+" if cff > 0 else "-"

    pattern = (
        cfo_sign,
        cfi_sign,
        cff_sign
    )

    if pattern == ("+", "-", "-"):

        if high_cfo_pat:
            return "Shareholder Returns"

        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Mixed"