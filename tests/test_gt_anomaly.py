import math

import pandas as pd
import pytest

from src.config import GTThresholds
from src.gt_anomaly import add_gt_anomaly_columns, classify_green_time


def test_normal_green_time():
    result = classify_green_time(100, 100)
    assert result["GT_Anomaly"] == "No Anomaly"
    assert result["GT_Severity"] == "Normal"
    assert result["GT_Ratio"] == pytest.approx(1.0)
    assert result["GT_Reason"] == "within_thresholds"


def test_low_anomaly():
    result = classify_green_time(49, 100)
    assert result["GT_Anomaly"] == "Anomaly"
    assert result["GT_Severity"] == "Anomaly-Low"
    assert result["GT_Reason"] == "low_ratio"


def test_high_anomaly():
    result = classify_green_time(151, 100)
    assert result["GT_Anomaly"] == "Anomaly"
    assert result["GT_Severity"] == "Anomaly-High"
    assert result["GT_Reason"] == "high_ratio"


def test_exact_anomaly_boundaries_are_normal():
    assert classify_green_time(50, 100)["GT_Anomaly"] == "No Anomaly"
    assert classify_green_time(150, 100)["GT_Anomaly"] == "No Anomaly"


def test_severity_boundaries_and_absolute_short_guard():
    assert classify_green_time(34.9, 100)["GT_Severity"] == "Severe-Low"
    assert classify_green_time(35, 100)["GT_Severity"] == "Anomaly-Low"
    assert classify_green_time(200, 100)["GT_Severity"] == "Anomaly-High"
    assert classify_green_time(200.1, 100)["GT_Severity"] == "Severe-High"
    assert classify_green_time(5, 1000)["GT_Severity"] == "Severe-Low"


def test_invalid_values_return_reason_codes():
    cases = [
        ("bad", 100, "non_numeric"),
        (math.nan, 100, "non_finite"),
        (-1, 100, "negative_green_time"),
        (10, 0, "non_positive_baseline"),
    ]
    for gt, mean, reason in cases:
        result = classify_green_time(gt, mean)
        assert result["GT_Anomaly"] == "Invalid"
        assert result["GT_Reason"] == reason
        assert math.isnan(result["GT_Ratio"])


def test_custom_thresholds_are_applied():
    thresholds = GTThresholds(
        low_multiplier=0.60,
        high_multiplier=1.40,
        severe_low_multiplier=0.40,
        severe_high_multiplier=1.80,
        absolute_short_seconds=3,
    )
    assert classify_green_time(55, 100, thresholds)["GT_Severity"] == "Anomaly-Low"
    assert classify_green_time(145, 100, thresholds)["GT_Severity"] == "Anomaly-High"


def test_invalid_threshold_configuration_is_rejected():
    bad = GTThresholds(low_multiplier=0.30, severe_low_multiplier=0.40)
    with pytest.raises(ValueError, match="severe_low_multiplier"):
        classify_green_time(100, 100, bad)


def test_dataframe_enrichment_preserves_input_and_index():
    source = pd.DataFrame(
        {
            "Green Time (Sec)": [100, 49],
            "GT_mean": [100, 100],
        },
        index=[10, 20],
    )
    result = add_gt_anomaly_columns(source)

    assert list(source.columns) == ["Green Time (Sec)", "GT_mean"]
    assert list(result.index) == [10, 20]
    assert result.loc[10, "GT_Severity"] == "Normal"
    assert result.loc[20, "GT_Severity"] == "Anomaly-Low"


def test_dataframe_enrichment_rejects_missing_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        add_gt_anomaly_columns(pd.DataFrame({"Green Time (Sec)": [10]}))
