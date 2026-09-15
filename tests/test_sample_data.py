from pathlib import Path

from src.pipeline import process_frame, read_main_export


def test_sanitized_sample_has_stable_expected_results():
    path = Path("sample_data/main_sanitized.csv")
    result = process_frame(read_main_export(path), source_name=path.name)
    report = result.report.iloc[0]

    assert report["Rows"] == 12
    assert report["GT_Valid"] == 10
    assert report["GT_Invalid"] == 2
    assert report["GT_Anomalies"] == 3
    assert report["GT_Normal"] == 7
    assert report["Severe_Low"] == 1
    assert report["Anomaly_Low"] == 1
    assert report["Anomaly_High"] == 0
    assert report["Severe_High"] == 1
    assert report["GT_Anomaly_Rate"] == 0.3
    assert len(result.daily_frames) == 3
