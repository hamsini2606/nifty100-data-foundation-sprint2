import pandas as pd
from src.etl.validator import DataValidator

df = pd.DataFrame({
    "company_id": [1, 2, 2, 4],
    "Sales": [100, -50, 300, 200]
})

validator = DataValidator()

validator.validate_pk(df, "company_id", "companies")
validator.validate_positive_sales(df)

validator.save_report()

print(validator.failures)