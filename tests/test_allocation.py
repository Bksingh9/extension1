import pytest

from src.allocation import decide, remaining_exposure_budget


def test_high_confidence_bull_uses_full_allocation():
    d = decide("BULL", 0.85)
    assert d.effective_label == "BULL"
    assert d.target_exposure_pct == 0.95
    assert d.reason == "ok"


def test_low_confidence_falls_back_to_neutral():
    d = decide("EUPHORIA", 0.50)
    assert d.effective_label == "NEUTRAL"
    assert d.target_exposure_pct == 0.60
    assert "low_confidence" in d.reason


def test_unknown_label_falls_back_to_neutral():
    d = decide("FOMO", 0.99)
    assert d.effective_label == "NEUTRAL"
    assert d.target_exposure_pct == 0.60


def test_crash_uses_minimal_allocation():
    d = decide("CRASH", 0.90)
    assert d.target_exposure_pct == 0.10


def test_remaining_budget_positive_when_under_cap():
    # equity 100k, BULL cap 95% = 95k, current 10k -> 85k remaining
    rem = remaining_exposure_budget(100_000, 10_000, "BULL", 0.85)
    assert rem == pytest.approx(85_000)


def test_remaining_budget_zero_when_over_cap():
    # NEUTRAL cap 60% = 60k, current 80k -> 0 (clamped, never negative)
    rem = remaining_exposure_budget(100_000, 80_000, "NEUTRAL", 0.85)
    assert rem == 0.0


def test_remaining_budget_uses_neutral_on_low_confidence():
    # Confidence below 0.60 -> NEUTRAL cap 60%, even if label was BULL
    rem = remaining_exposure_budget(100_000, 0, "BULL", 0.50)
    assert rem == pytest.approx(60_000)
