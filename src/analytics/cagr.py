def calculate_cagr(start_value, end_value, years):
    """
    CAGR = ((End / Start) ^ (1 / Years) - 1) * 100

    Handles all six edge cases.
    """

    if years <= 0:
        return None, "INVALID_YEARS"

    if start_value is None or end_value is None:
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:
        cagr = (
            ((end_value / start_value) ** (1 / years)) - 1
        ) * 100

        return cagr, None

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "INSUFFICIENT"


def calculate_window_cagr(
    df,
    value_column,
    years
):
    """
    Calculate CAGR using a company-year DataFrame.

    Example:
    calculate_window_cagr(df, "net_profit", 5)
    """

    if len(df) <= years:
        return None, "INSUFFICIENT"

    df = df.sort_values("year")

    start_value = df.iloc[-(years + 1)][value_column]
    end_value = df.iloc[-1][value_column]

    return calculate_cagr(
        start_value,
        end_value,
        years
    )