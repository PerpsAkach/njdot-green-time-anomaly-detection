import pandas as pd

from src.data_quality import summarize_main_data_quality


def test_data_quality_metrics_count_missing_and_duplicate_time_keys():
    frame = pd.DataFrame(
        {
            "DateConverted Hierarchy - Date": ["2026-01-01", "2026-01-01", None],
            "Time": ["08:00", "08:00", None],
            "Green Time (Sec)": [10, None, 30],
            "GT_mean": [20, 20, None],
        }
    )

    metrics = summarize_main_data_quality(frame)

    assert metrics == {
        "Missing_GT": 1,
        "Missing_GT_mean": 1,
        "Missing_Date": 1,
        "Missing_Time": 1,
        "Duplicate_Date_Time": 2,
    }


def test_data_quality_metrics_are_safe_when_optional_columns_are_absent():
    metrics = summarize_main_data_quality(
        pd.DataFrame({"Green Time (Sec)": [10], "GT_mean": [20]})
    )
    assert metrics["Missing_GT"] == 0
    assert metrics["Missing_GT_mean"] == 0
    assert metrics["Missing_Date"] == 0
    assert metrics["Missing_Time"] == 0
    assert metrics["Duplicate_Date_Time"] == 0
