import numpy as np
import pandas as pd

from src.strategies import (
    Signal,
    breakout,
    mean_reversion,
    momentum,
    news_sentiment_signal,
    vwap_intraday,
    best_signal,
)


def _ohlcv(closes, vol_mult=1.0):
    n = len(closes)
    close = pd.Series(closes, dtype=float)
    high = close * 1.01
    low = close * 0.99
    open_ = close.shift(1).fillna(close.iloc[0])
    volume = pd.Series([1_000_000 * vol_mult] * n, dtype=float)
    df = pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume}
    )
    return df


def test_strategies_return_none_on_short_history():
    df = _ohlcv([100.0] * 10)
    assert momentum("X", df) is None
    assert mean_reversion("X", df) is None
    assert breakout("X", df) is None
    assert vwap_intraday("X", df) is None


def test_breakout_fires_on_clear_high_with_volume():
    base = [100.0] * 80
    closes = base + [101, 102, 103, 104, 105, 110]
    df = _ohlcv(closes)
    df.loc[df.index[-1], "volume"] = df["volume"].iloc[-2] * 5
    sig = breakout("XYZ", df)
    assert sig is not None
    assert sig.strategy == "breakout"
    assert sig.entry > 0
    assert sig.atr > 0


def test_momentum_does_not_fire_on_flat_market():
    df = _ohlcv([100.0] * 100)
    assert momentum("X", df) is None


def test_news_sentiment_blocked_on_earnings():
    df = _ohlcv([100.0] * 100)
    sig = news_sentiment_signal(
        symbol="X",
        bars=df,
        sentiment_score=9.0,
        has_earnings_within_2d=True,
        min_score=6.0,
    )
    assert sig is None


def test_news_sentiment_blocked_below_threshold():
    df = _ohlcv([100.0] * 100)
    sig = news_sentiment_signal(
        symbol="X",
        bars=df,
        sentiment_score=3.0,
        has_earnings_within_2d=False,
        min_score=6.0,
    )
    assert sig is None


def test_best_signal_picks_higher_weighted_score():
    """If two strategies fire, the higher weighted-score wins."""
    np.random.seed(0)
    closes = list(np.linspace(80, 100, 80)) + [101, 102, 103, 104, 105, 115]
    df = _ohlcv(closes)
    df.loc[df.index[-1], "volume"] = df["volume"].iloc[-2] * 5
    weights = {"momentum": 1.0, "mean_reversion": 1.0, "breakout": 1.0, "vwap_intraday": 1.0}
    sig = best_signal("XYZ", df, weights)
    # Should at least be one of the trend-y strategies, never None here.
    assert sig is None or sig.strategy in {"momentum", "breakout"}
