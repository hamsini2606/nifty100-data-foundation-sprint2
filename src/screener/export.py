import os
import pandas as pd

from src.screener.engine import ScreenerEngine
from src.screener.presets import PRESETS


def export_screener():

    engine = ScreenerEngine()

    os.makedirs("output", exist_ok=True)

    writer = pd.ExcelWriter(
        "output/screener_output.xlsx",
        engine="openpyxl"
    )

    for preset in PRESETS:

        print(f"Running {preset}...")

        df = engine.run_preset(preset)

        df.to_excel(
            writer,
            sheet_name=preset[:31],
            index=False
        )

    writer.close()

    engine.close()

    print("\nExport Complete!")
    print("Saved to output/screener_output.xlsx")


if __name__ == "__main__":
    export_screener()