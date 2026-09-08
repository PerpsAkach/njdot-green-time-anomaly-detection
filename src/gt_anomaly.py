from __future__ import annotations

import numpy as np
import pandas as pd

LOW_MULTIPLIER = 0.50
HIGH_MULTIPLIER = 1.50
SEVERE_LOW_MULTIPLIER = 0.35
SEVERE_HIGH_MULTIPLIER = 2.00
ABSOLUTE_SHORT_SECONDS = 5.0


def classify_green_time(green_time, gt_mean) -> dict:
    try:
        gt = float(green_time)
        mean = float(gt_mean)
    except (TypeError, ValueError):
        return {"GT_Anomaly": "Invalid", "GT_Severity": "Invalid", "GT_Ratio": np.nan}

    if not np.isfinite(gt) or not np.isfinite(mean) or gt < 0 or mean <= 0:
        return {"GT_Anomaly": "Invalid", "GT_Severity": "Invalid", "GT_Ratio": np.nan}

    low = LOW_MULTIPLIER * mean
    high = HIGH_MULTIPLIER * mean
    severe_low = SEVERE_LOW_MULTIPLIER * mean
    severe_high = SEVERE_HIGH_MULTIPLIER * mean

    if gt <= ABSOLUTE_SHORT_SECONDS or gt < severe_low:
        severity = "Severe-Low"
    elif gt > severe_high:
        severity = "Severe-High"
    elif gt < low:
        severity = "Anomaly-Low"
    elif gt > high:
        severity = "Anomaly-High"
    else:
        severity = "Normal"

    return {
        "GT_Anomaly": "No Anomaly" if severity == "Normal" else "Anomaly",
        "GT_Severity": severity,
        "GT_Ratio": gt / mean,
        "GT_Low_Threshold": low,
        "GT_High_Threshold": high,
    }


def add_gt_anomaly_columns(df: pd.DataFrame) -> pd.DataFrame:
    required = {"Green Time (Sec)", "GT_mean"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = pd.DataFrame(
        [classify_green_time(gt, mean) for gt, mean in zip(df["Green Time (Sec)"], df["GT_mean"])],
        index=df.index,
    )
    return pd.concat([df.copy(), result], axis=1)
