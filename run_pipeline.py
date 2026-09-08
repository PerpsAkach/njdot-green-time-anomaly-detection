from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.gt_anomaly import add_gt_anomaly_columns


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--main", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    df = pd.read_excel(args.main, engine="openpyxl")
    processed = add_gt_anomaly_columns(df)

    args.output.mkdir(parents=True, exist_ok=True)
    output = args.output / f"{args.main.stem}_processed_{datetime.now():%Y%m%d_%H%M%S}.xlsx"

    report = pd.DataFrame([{
        "Rows": len(processed),
        "GT_Anomalies": int((processed["GT_Anomaly"] == "Anomaly").sum()),
        "GT_Invalid": int((processed["GT_Anomaly"] == "Invalid").sum()),
        "Source_MAIN": args.main.name,
    }])

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        report.to_excel(writer, index=False, sheet_name="RUN_REPORT")
        processed.to_excel(writer, index=False, sheet_name="PROCESSED")

    print(output)


if __name__ == "__main__":
    main()
