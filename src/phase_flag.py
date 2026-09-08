def evaluate_phase_flag(vehicle_demand_mismatch: bool, signal_group_inconsistency: bool) -> str:
    """Return a separate diagnostic flag for phase/signal-group consistency."""
    return "Yes" if vehicle_demand_mismatch or signal_group_inconsistency else "No"
