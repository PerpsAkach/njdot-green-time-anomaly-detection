from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GTThresholds:
    """Configuration for explainable Green-Time screening.

    Multipliers are ratios of observed Green Time to the row-level ``GT_mean``
    baseline. Validation prevents contradictory or physically invalid settings.
    """

    low_multiplier: float = 0.50
    high_multiplier: float = 1.50
    severe_low_multiplier: float = 0.35
    severe_high_multiplier: float = 2.00
    absolute_short_seconds: float = 5.0

    def validate(self) -> None:
        if self.absolute_short_seconds < 0:
            raise ValueError("absolute_short_seconds must be non-negative")
        if not 0 < self.severe_low_multiplier < self.low_multiplier < 1:
            raise ValueError(
                "expected 0 < severe_low_multiplier < low_multiplier < 1"
            )
        if not 1 < self.high_multiplier < self.severe_high_multiplier:
            raise ValueError(
                "expected 1 < high_multiplier < severe_high_multiplier"
            )


DEFAULT_THRESHOLDS = GTThresholds()
DEFAULT_THRESHOLDS.validate()

MAIN_DATE_COLUMN = "DateConverted Hierarchy - Date"
MAIN_TIME_COLUMN = "Time"
MAIN_GT_COLUMN = "Green Time (Sec)"
MAIN_GT_MEAN_COLUMN = "GT_mean"
MAIN_REQUIRED_COLUMNS = (MAIN_GT_COLUMN, MAIN_GT_MEAN_COLUMN)
