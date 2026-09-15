from src.phase_flag import evaluate_phase_flag


def test_phase_flag_is_no_when_diagnostics_are_clear():
    assert evaluate_phase_flag(False, False) == "No"


def test_phase_flag_is_yes_for_vehicle_demand_mismatch():
    assert evaluate_phase_flag(True, False) == "Yes"


def test_phase_flag_is_yes_for_signal_group_inconsistency():
    assert evaluate_phase_flag(False, True) == "Yes"


def test_phase_flag_is_yes_when_both_diagnostics_fire():
    assert evaluate_phase_flag(True, True) == "Yes"
