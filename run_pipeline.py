from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from src.config import GTThresholds
from src.pipeline import process_frame, read_main_export, write_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Screen MAIN Green-Time data for explainable threshold anomalies."
    )
    parser.add_argument("--main", type=Path, required=True, help="MAIN .xlsx or .csv export")
    parser.add_argument("--output", type=Path, default=Path("outputs"), help="Output directory")
    parser.add_argument("--low", type=float, default=0.50, help="Low anomaly multiplier")
    parser.add_argument("--high", type=float, default=1.50, help="High anomaly multiplier")
    parser.add_argument("--severe-low", type=float, default=0.35, help="Severe-low multiplier")
    parser.add_argument("--severe-high", type=float, default=2.00, help="Severe-high multiplier")
    parser.add_argument(
        "--absolute-short",
        type=float,
        default=5.0,
        help="Absolute short-GT guard in seconds",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if not args.main.exists() or not args.main.is_file():
        raise SystemExit(f"MAIN input does not exist or is not a file: {args.main}")

    thresholds = GTThresholds(
        low_multiplier=args.low,
        high_multiplier=args.high,
        severe_low_multiplier=args.severe_low,
        severe_high_multiplier=args.severe_high,
        absolute_short_seconds=args.absolute_short,
    )
    try:
        thresholds.validate()
        frame = read_main_export(args.main)
        result = process_frame(frame, source_name=args.main.name, thresholds=thresholds)
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc)) from exc

    args.output.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
    output = args.output / f"{args.main.stem}_processed_{timestamp}.xlsx"
    write_result(result, output)

    report = result.report.iloc[0]
    print(
        f"Wrote {output} | rows={int(report['Rows'])} "
        f"valid={int(report['GT_Valid'])} anomalies={int(report['GT_Anomalies'])} "
        f"invalid={int(report['GT_Invalid'])} daily_sheets={len(result.daily_frames)}"
    )


if __name__ == "__main__":
    main()
