from dataclasses import dataclass


@dataclass(frozen=True)
class GTThresholds:
    low_multiplier: float = 0.50
    high_multiplier: float = 1.50
    severe_low_multiplier: float = 0.35
    severe_high_multiplier: float = 2.00
    absolute_short_seconds: float = 5.0


MAIN_DATE_COLUMN = "DateConverted Hierarchy - Date"
MAIN_TIME_COLUMN = "Time"
MAIN_GT_COLUMN = "Green Time (Sec)"
MAIN_GT_MEAN_COLUMN = "GT_mean"
