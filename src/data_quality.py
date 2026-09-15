from __future__ import annotations

import pandas as pd

from .config import (
    MAIN_DATE_COLUMN,
    MAIN_GT_COLUMN,
    MAIN_GT_MEAN_COLUMN,
    MAIN_TIME_COLUMN,
)


def summarize_main_data_quality(frame: pd.DataFrame) -> dict[str, int]:
    """Return non-destructive quality indicators for a MAIN export.

    These metrics identify review conditions only. They do not infer controller
    faults or impute missing operational values.
    """
    metrics = {
        "Missing_GT": 0,
        "Missing_GT_mean": 0,
        "Missing_Date": 0,
        "Missing_Time": 0,
        "Duplicate_Date_Time": 0,
    }

    if MAIN_GT_COLUMN in frame.columns:
        metrics["Missing_GT"] = int(frame[MAIN_GT_COLUMN].isna().sum())
    if MAIN_GT_MEAN_COLUMN in frame.columns:
        metrics["Missing_GT_mean"] = int(frame[MAIN_GT_MEAN_COLUMN].isna().sum())
    if MAIN_DATE_COLUMN in frame.columns:
        metrics["Missing_Date"] = int(frame[MAIN_DATE_COLUMN].isna().sum())
    if MAIN_TIME_COLUMN in frame.columns:
        metrics["Missing_Time"] = int(frame[MAIN_TIME_COLUMN].isna().sum())

    if MAIN_DATE_COLUMN in frame.columns and MAIN_TIME_COLUMN in frame.columns:
        complete = frame[[MAIN_DATE_COLUMN, MAIN_TIME_COLUMN]].dropna()
        metrics["Duplicate_Date_Time"] = int(
            complete.duplicated(
                subset=[MAIN_DATE_COLUMN, MAIN_TIME_COLUMN], keep=False
            ).sum()
        )

    return metrics
