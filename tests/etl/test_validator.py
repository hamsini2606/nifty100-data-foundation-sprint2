import pandas as pd

from src.etl.validator import DataValidator


def test_duplicate_pk():

    df = pd.DataFrame({
        "company_id": [1, 2, 2, 3]
    })

    validator = DataValidator()

    validator.check_pk_uniqueness(
        df,
        "company_id",
        "companies"
    )

    assert len(validator.failures) == 1


def test_positive_sales():

    df = pd.DataFrame({
        "sales": [100, -50, 200]
    })

    validator = DataValidator()

    validator.check_positive_sales(df)

    assert len(validator.failures) == 1