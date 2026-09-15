from __future__ import annotations

import numpy as np
import pandas as pd

from .config import DEFAULT_THRESHOLDS, MAIN_GT_COLUMN, MAIN_GT_MEAN_COLUMN, GTThresholds


def _invalid(reason: str) -> dict:
    return {
        "GT_Anomaly": "Invalid",
        "GT_Severity": "Invalid",
        "GT_Ratio": np.nan,
        "GT_Low_Threshold": np.nan,
        "GT_High_Threshold": np.nan,
        "GT_Reason": reason,
    }


def classify_green_time(
    green_time,
    gt_mean,
    thresholds: GTThresholds = DEFAULT_THRESHOLDS,
) -> dict:
    """Classify one observed Green-Time value against its row-level baseline.

    Boundary semantics are intentional: values exactly at the low/high anomaly
    thresholds are normal; severe-high is strictly greater than its threshold;
    the absolute-short guard is inclusive.
    """
    thresholds.validate()

    try:
        gt = float(green_time)
        mean = float(gt_mean)
    except (TypeError, ValueError):
        return _invalid("non_numeric")

    if not np.isfinite(gt) or not np.isfinite(mean):
        return _invalid("non_finite")
    if gt < 0:
        return _invalid("negative_green_time")
    if mean <= 0:
        return _invalid("non_positive_baseline")

    low = thresholds.low_multiplier * mean
    high = thresholds.high_multiplier * mean
    severe_low = thresholds.severe_low_multiplier * mean
    severe_high = thresholds.severe_high_multiplier * mean
    ratio = gt / mean

    if gt <= thresholds.absolute_short_seconds or gt < severe_low:
        severity = "Severe-Low"
        reason = "absolute_short_or_severe_low_ratio"
    elif gt > severe_high:
        severity = "Severe-High"
        reason = "severe_high_ratio"
    elif gt < low:
        severity = "Anomaly-Low"
        reason = "low_ratio"
    elif gt > high:
        severity = "Anomaly-High"
        reason = "high_ratio"
    else:
        severity = "Normal"
        reason = "within_thresholds"

    return {
        "GT_Anomaly": "No Anomaly" if severity == "Normal" else "Anomaly",
        "GT_Severity": severity,
        "GT_Ratio": ratio,
        "GT_Low_Threshold": low,
        "GT_High_Threshold": high,
        "GT_Reason": reason,
    }


def add_gt_anomaly_columns(
    df: pd.DataFrame,
    thresholds: GTThresholds = DEFAULT_THRESHOLDS,
) -> pd.DataFrame:
    """Return a copy of ``df`` with explainable Green-Time screening columns."""
    thresholds.validate()
    required = {MAIN_GT_COLUMN, MAIN_GT_MEAN_COLUMN}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    result = pd.DataFrame(
        [
            classify_green_time(gt, mean, thresholds)
            for gt, mean in zip(df[MAIN_GT_COLUMN], df[MAIN_GT_MEAN_COLUMN])
        ],
        index=df.index,
    )
    return pd.concat([df.copy(), result], axis=1)
