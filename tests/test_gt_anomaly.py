from src.gt_anomaly import classify_green_time


def test_normal_green_time():
    result = classify_green_time(100, 100)
    assert result["GT_Anomaly"] == "No Anomaly"
    assert result["GT_Severity"] == "Normal"


def test_low_anomaly():
    result = classify_green_time(49, 100)
    assert result["GT_Anomaly"] == "Anomaly"


def test_high_anomaly():
    result = classify_green_time(151, 100)
    assert result["GT_Anomaly"] == "Anomaly"


def test_exact_boundaries_are_normal():
    assert classify_green_time(50, 100)["GT_Anomaly"] == "No Anomaly"
    assert classify_green_time(150, 100)["GT_Anomaly"] == "No Anomaly"
