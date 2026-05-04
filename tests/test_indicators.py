import numpy as np
import pandas as pd

from src.indicators import atr, bollinger, ema, macd, rsi, vwap


def _series(values):
    return pd.Series(values, dtype=float)


def test_ema_matches_pandas_reference():
    s = _series(range(50))
    out = ema(s, span=10)
    expected = s.ewm(span=10, adjust=False).mean()
    assert np.allclose(out, expected)


def test_rsi_in_range_0_100():
    np.random.seed(0)
    s = _series(np.cumsum(np.random.randn(200)) + 100)
    out = rsi(s, 14)
    assert out.min() >= 0
    assert out.max() <= 100


def test_macd_hist_equals_line_minus_signal():
    np.random.seed(1)
    s = _series(np.cumsum(np.random.randn(300)) + 100)
    line, sig, hist = macd(s)
    assert np.allclose((line - sig).iloc[-50:], hist.iloc[-50:])


def test_bollinger_bands_ordered():
    np.random.seed(2)
    s = _series(np.cumsum(np.random.randn(100)) + 100)
    upper, mid, lower = bollinger(s, 20, 2.0)
    valid = upper.dropna().tail(50)
    assert (upper.tail(50) >= mid.tail(50)).all()
    assert (mid.tail(50) >= lower.tail(50)).all()


def test_atr_non_negative():
    np.random.seed(3)
    n = 100
    close = pd.Series(np.cumsum(np.random.randn(n)) + 100, dtype=float)
    high = close + np.random.rand(n)
    low = close - np.random.rand(n)
    a = atr(high, low, close, 14).dropna()
    assert (a >= 0).all()


def test_vwap_monotonic_with_constant_price():
    n = 50
    close = pd.Series([100.0] * n)
    high = close + 1
    low = close - 1
    volume = pd.Series([1000.0] * n)
    v = vwap(high, low, close, volume)
    assert np.allclose(v.dropna(), 100.0)
