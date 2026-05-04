import numpy as np
import pandas as pd

from src.features import HMM_FEATURES, build_features, select_hmm_matrix


def _bars(n=200, seed=0):
    rng = np.random.default_rng(seed)
    rets = rng.normal(0, 0.01, size=n)
    close = 100 * np.exp(np.cumsum(rets))
    high = close * (1 + np.abs(rng.normal(0, 0.005, size=n)))
    low = close * (1 - np.abs(rng.normal(0, 0.005, size=n)))
    open_ = np.r_[close[0], close[:-1]]
    volume = rng.integers(500_000, 2_000_000, size=n).astype(float)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume}
    )


def test_build_features_drops_warmup_rows():
    bars = _bars(200)
    feats = build_features(bars)
    # vol_60 / mom_60 / atr_14 require ~60 bars of history.
    assert len(feats) > 0
    assert len(feats) < len(bars)
    assert not feats.isna().any().any()


def test_build_features_columns_present():
    bars = _bars(200)
    feats = build_features(bars)
    for col in HMM_FEATURES:
        assert col in feats.columns


def test_select_hmm_matrix_shape_matches_features():
    bars = _bars(200)
    feats = build_features(bars)
    x = select_hmm_matrix(feats)
    assert x.shape[0] == len(feats)
    assert x.shape[1] == len(HMM_FEATURES)


def test_build_features_empty_input():
    feats = build_features(pd.DataFrame())
    assert feats.empty
