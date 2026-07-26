from pathlib import Path
import pandas as pd


raw_folder = Path("data/raw")

target_words = [
    "cash",
    "profit",
    "loss",
    "document"
]


def find_header_row(file_path):
    """
    Find the row containing the actual column headers.
    """

    preview = pd.read_excel(
        file_path,
        header=None,
        nrows=10
    )

    for index, row in preview.iterrows():

        values = [
            str(value).strip().lower()
            for value in row.tolist()
        ]

        row_text = " ".join(values)

        if (
            "company_id" in row_text
            or "company id" in row_text
            or "sales" in row_text
            or "revenue" in row_text
            or "net profit" in row_text
            or "cash" in row_text
        ):
            return index

    return 0


for file_path in raw_folder.glob("*.xlsx"):

    filename = file_path.name.lower()

    if any(word in filename for word in target_words):

        print("\n" + "=" * 80)
        print(f"FILE: {file_path.name}")
        print("=" * 80)

        try:

            header_row = find_header_row(file_path)

            df = pd.read_excel(
                file_path,
                header=header_row
            )

            print("HEADER ROW:", header_row)
            print("SHAPE:", df.shape)

            print("\nCOLUMNS:")
            print(df.columns.tolist())

            print("\nFIRST 3 ROWS:")
            print(df.head(3).to_string())

        except Exception as error:

            print("ERROR:", error)