"""End-to-end test of the HMM regime engine on synthetic data.

We construct a 3-segment synthetic price series (calm uptrend, then a
high-vol drawdown, then calm uptrend again). The HMM should produce
distinct states for the calm and volatile segments.
"""
import numpy as np
import pandas as pd
import pytest

from src.regime import RegimeAssessment, fit, load, save


def _synthetic_bars(seed=0):
    """Two regimes with clearly different vol & drift, repeated."""
    rng = np.random.default_rng(seed)
    parts = []
    # calm uptrend
    parts.append(rng.normal(0.001, 0.005, size=120))
    # volatile drawdown
    parts.append(rng.normal(-0.003, 0.025, size=80))
    # calm uptrend
    parts.append(rng.normal(0.001, 0.006, size=120))
    # high-vol blowup
    parts.append(rng.normal(-0.005, 0.030, size=80))
    # final calm
    parts.append(rng.normal(0.001, 0.005, size=100))
    rets = np.concatenate(parts)
    close = 100 * np.exp(np.cumsum(rets))
    high = close * (1 + np.abs(rng.normal(0, 0.004, size=len(close))))
    low = close * (1 - np.abs(rng.normal(0, 0.004, size=len(close))))
    open_ = np.r_[close[0], close[:-1]]
    volume = rng.integers(500_000, 2_000_000, size=len(close)).astype(float)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume}
    )


def test_fit_predict_round_trip(tmp_path):
    bars = _synthetic_bars(seed=1)
    model = fit(bars)
    assert len(model.state_to_label) == 5
    assert set(model.state_to_label.values()) == {"CRASH", "BEAR", "NEUTRAL", "BULL", "EUPHORIA"}

    # Save and load round-trip.
    p = tmp_path / "regime.joblib"
    save(model, path=p)
    loaded = load(path=p)
    assert loaded is not None
    assert loaded.state_to_label == model.state_to_label

    # Predict_current returns a valid assessment.
    from src.features import build_features
    feats = build_features(bars)
    a = loaded.predict_current(feats)
    assert isinstance(a, RegimeAssessment)
    assert a.label in {"CRASH", "BEAR", "NEUTRAL", "BULL", "EUPHORIA"}
    assert 0.0 <= a.confidence <= 1.0
    assert sum(a.distribution.values()) == pytest.approx(1.0, abs=0.05)


def test_transition_matrix_rows_sum_to_one():
    bars = _synthetic_bars(seed=2)
    model = fit(bars)
    tm = model.transition_matrix()
    row_sums = tm.sum(axis=1)
    for s in row_sums:
        assert s == pytest.approx(1.0, abs=1e-6)


def test_load_returns_none_when_missing(tmp_path):
    assert load(path=tmp_path / "no_such_file.joblib") is None


def test_fit_raises_with_too_few_bars():
    short = pd.DataFrame(
        {
            "open": [100] * 30,
            "high": [101] * 30,
            "low": [99] * 30,
            "close": [100] * 30,
            "volume": [1_000_000] * 30,
        }
    )
    with pytest.raises(ValueError):
        fit(short)
