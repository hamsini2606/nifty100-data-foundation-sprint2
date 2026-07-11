import re

def normalize_year(year):
    """
    Convert different year formats into a 4-digit year.
    """

    if year is None:
        return None

    year = str(year).strip()

    if year.isdigit():
        if len(year) == 4:
            return int(year)

        if len(year) == 2:
            return int("20" + year)

    match = re.search(r'(\d{2,4})', year)

    if match:
        value = match.group(1)

        if len(value) == 2:
            return int("20" + value)

        return int(value)

    return None


def normalize_ticker(ticker):
    """
    Normalize stock ticker.
    """

    if ticker is None:
        return None

    return str(ticker).strip().upper()