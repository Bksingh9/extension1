"""Five entry strategies. Each is a pure function: (symbol, bars) -> Signal | None.

Bars is a pandas.DataFrame indexed by datetime, with columns:
  open, high, low, close, volume

Stop / target / sizing are NEVER strategy-specific; they are computed by the
risk manager and position sizer downstream.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal, Optional

import pandas as pd

from .indicators import atr, bollinger, ema, macd, rsi, slope, vwap

StrategyName = Literal[
    "momentum",
    "mean_reversion",
    "breakout",
    "vwap_intraday",
    "news_sentiment",
]


@dataclass
class Signal:
    symbol: str
    strategy: StrategyName
    side: Literal["buy", "sell"]
    entry: float
    atr: float
    score: float  # 0.0 .. 1.0; higher is stronger
    notes: str = ""
    horizon: Literal["intraday", "swing"] = "swing"


def _last(series: pd.Series) -> float:
    return float(series.iloc[-1])


def _enough_bars(bars: pd.DataFrame, n: int) -> bool:
    return bars is not None and len(bars) >= n


def momentum(symbol: str, bars: pd.DataFrame) -> Optional[Signal]:
    if not _enough_bars(bars, 60):
        return None
    close, high, low, volume = bars["close"], bars["high"], bars["low"], bars["volume"]

    r = rsi(close, 14)
    line, sig, hist = macd(close)
    e9, e21, e50 = ema(close, 9), ema(close, 21), ema(close, 50)
    a = atr(high, low, close, 14)

    last_close = _last(close)
    prev_high = float(high.iloc[-2])
    avg_vol_20 = float(volume.rolling(20).mean().iloc[-1])
    last_vol = _last(volume)
    last_atr = _last(a)

    if pd.isna(last_atr) or last_atr <= 0:
        return None
    if not (_last(r) > 55):
        return None
    if not (_last(hist) > 0 and float(hist.iloc[-2]) <= 0):
        return None
    if not (_last(e9) > _last(e21) > _last(e50)):
        return None
    if not (last_close > prev_high):
        return None
    if not (avg_vol_20 > 0 and last_vol > 1.5 * avg_vol_20):
        return None

    rsi_term = max(0.0, min(1.0, (_last(r) - 55.0) / 25.0))
    vol_term = max(0.0, min(1.0, (last_vol / avg_vol_20 - 1.5) / 1.5))
    score = 0.5 * rsi_term + 0.5 * vol_term
    return Signal(
        symbol=symbol,
        strategy="momentum",
        side="buy",
        entry=last_close,
        atr=last_atr,
        score=score,
        notes=f"RSI={_last(r):.1f} MACD-hist+ EMA-stack vol={last_vol/avg_vol_20:.1f}x",
        horizon="swing",
    )


def mean_reversion(symbol: str, bars: pd.DataFrame) -> Optional[Signal]:
    if not _enough_bars(bars, 60):
        return None
    close, high, low = bars["close"], bars["high"], bars["low"]
    open_ = bars["open"]
    a = atr(high, low, close, 14)
    upper, mid, lower = bollinger(close, 20, 2.0)
    r = rsi(close, 14)
    e50 = ema(close, 50)

    last_close = _last(close)
    last_atr = _last(a)
    if pd.isna(last_atr) or last_atr <= 0:
        return None

    # Lower-band touch on prior bar, RSI<35 on prior bar, EMA50 slope >= 0,
    # and a green confirmation candle on the latest bar.
    touched_lower = float(low.iloc[-2]) <= float(lower.iloc[-2])
    rsi_oversold = float(r.iloc[-2]) < 35
    e50_slope = slope(e50, 5) >= 0
    green_candle = last_close > float(open_.iloc[-1])

    if not (touched_lower and rsi_oversold and e50_slope and green_candle):
        return None

    distance_from_lower = (last_close - float(lower.iloc[-1])) / last_close
    score = max(0.0, min(1.0, 0.6 + distance_from_lower * 5))
    return Signal(
        symbol=symbol,
        strategy="mean_reversion",
        side="buy",
        entry=last_close,
        atr=last_atr,
        score=score,
        notes=f"BB-lower touch RSI[-2]={float(r.iloc[-2]):.1f} green-confirm",
        horizon="swing",
    )


def breakout(symbol: str, bars: pd.DataFrame) -> Optional[Signal]:
    if not _enough_bars(bars, 30):
        return None
    close, high, low, volume = bars["close"], bars["high"], bars["low"], bars["volume"]
    a = atr(high, low, close, 14)

    resistance_20 = float(high.iloc[-21:-1].max())
    last_close = _last(close)
    last_atr = _last(a)
    avg_vol_20 = float(volume.rolling(20).mean().iloc[-1])
    last_vol = _last(volume)

    if pd.isna(last_atr) or last_atr <= 0 or pd.isna(avg_vol_20) or avg_vol_20 <= 0:
        return None
    if not (last_close > resistance_20):
        return None
    if not (last_vol > 2.0 * avg_vol_20):
        return None

    breakout_strength = (last_close - resistance_20) / resistance_20
    vol_term = min(1.0, (last_vol / avg_vol_20 - 2.0) / 2.0)
    score = max(0.0, min(1.0, 0.5 + breakout_strength * 10 + 0.3 * vol_term))
    return Signal(
        symbol=symbol,
        strategy="breakout",
        side="buy",
        entry=last_close,
        atr=last_atr,
        score=score,
        notes=f"close>{resistance_20:.2f} 20d-high vol={last_vol/avg_vol_20:.1f}x",
        horizon="swing",
    )


def vwap_intraday(symbol: str, bars: pd.DataFrame) -> Optional[Signal]:
    """Operates on intraday bars (1m/5m). Bars must be from the current session."""
    if not _enough_bars(bars, 30):
        return None
    close, high, low, volume = bars["close"], bars["high"], bars["low"], bars["volume"]
    open_ = bars["open"]

    vw = vwap(high, low, close, volume)
    r = rsi(close, 14)
    a = atr(high, low, close, 14)

    last_close = _last(close)
    last_open = _last(open_)
    last_vwap = _last(vw)
    last_atr = _last(a)
    last_rsi = _last(r)
    rsi_min_recent = float(r.iloc[-10:].min())

    if pd.isna(last_atr) or last_atr <= 0 or pd.isna(last_vwap):
        return None
    if not (rsi_min_recent < 45 and last_rsi > rsi_min_recent + 5):
        return None
    if not (last_close > last_vwap and last_open <= last_vwap):
        return None

    score = max(0.0, min(1.0, (last_rsi - rsi_min_recent) / 30.0))
    return Signal(
        symbol=symbol,
        strategy="vwap_intraday",
        side="buy",
        entry=last_close,
        atr=last_atr,
        score=score,
        notes=f"VWAP reclaim RSI {rsi_min_recent:.0f}->{last_rsi:.0f}",
        horizon="intraday",
    )


def news_sentiment_signal(
    symbol: str,
    bars: pd.DataFrame,
    sentiment_score: float,
    has_earnings_within_2d: bool,
    min_score: float = 6.0,
) -> Optional[Signal]:
    """News-driven entry. Requires a technical confirmation from any of the
    other four. Sentiment score is in [-10, +10]; must be >= min_score."""
    if has_earnings_within_2d:
        return None
    if sentiment_score < min_score:
        return None
    confirms: list[Optional[Signal]] = [
        momentum(symbol, bars),
        mean_reversion(symbol, bars),
        breakout(symbol, bars),
    ]
    confirm = next((s for s in confirms if s is not None), None)
    if confirm is None:
        return None
    score = max(0.0, min(1.0, 0.5 + (sentiment_score - 6.0) / 8.0))
    return Signal(
        symbol=symbol,
        strategy="news_sentiment",
        side="buy",
        entry=confirm.entry,
        atr=confirm.atr,
        score=score,
        notes=f"news +{sentiment_score:.1f}, tech={confirm.strategy}",
        horizon="swing",
    )


ALL_STRATEGIES: dict[str, Callable[[str, pd.DataFrame], Optional[Signal]]] = {
    "momentum": momentum,
    "mean_reversion": mean_reversion,
    "breakout": breakout,
    "vwap_intraday": vwap_intraday,
}


def best_signal(symbol: str, bars: pd.DataFrame, weights: dict[str, float]) -> Optional[Signal]:
    """Run all (non-news) strategies on a symbol and return the highest weighted-score signal."""
    candidates: list[Signal] = []
    for name, fn in ALL_STRATEGIES.items():
        sig = fn(symbol, bars)
        if sig is None:
            continue
        weighted = sig.score * float(weights.get(name, 1.0))
        candidates.append(
            Signal(
                symbol=sig.symbol,
                strategy=sig.strategy,
                side=sig.side,
                entry=sig.entry,
                atr=sig.atr,
                score=weighted,
                notes=sig.notes,
                horizon=sig.horizon,
            )
        )
    if not candidates:
        return None
    return max(candidates, key=lambda s: s.score)
