"""Stocktwits public stream — retail sentiment signal.

Endpoint:
  GET https://api.stocktwits.com/api/2/streams/symbol/{SYMBOL}.json

No key required. Free public access ~200 req/hour. Each message in the
response may carry an entities.sentiment.basic field of "Bullish" or
"Bearish" (or null/missing). We compute a -10..+10 score from the
bull/bear ratio.

Degrades gracefully: returns None on any failure.
"""
from __future__ import annotations

import time
from typing import Optional

from .logging_setup import get_logger

log = get_logger()

URL_FMT = "https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
TIMEOUT = 6
_MIN_INTERVAL = 0.4
_last_call_ts = 0.0


def _throttle() -> None:
    global _last_call_ts
    delta = time.time() - _last_call_ts
    if delta < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - delta)
    _last_call_ts = time.time()


def sentiment_score(symbol: str, min_messages: int = 5) -> Optional[float]:
    """Return -10..+10 score, or None if not enough data."""
    try:
        import requests
    except ImportError:
        return None
    _throttle()
    try:
        r = requests.get(URL_FMT.format(symbol=symbol.upper()), timeout=TIMEOUT)
        if r.status_code != 200:
            return None
        msgs = (r.json() or {}).get("messages", []) or []
    except Exception as e:
        log.debug(f"stocktwits {symbol} failed: {e}")
        return None

    bull = 0
    bear = 0
    for m in msgs:
        ent = (m.get("entities") or {}).get("sentiment") or {}
        basic = ent.get("basic")
        if basic == "Bullish":
            bull += 1
        elif basic == "Bearish":
            bear += 1
    total = bull + bear
    if total < min_messages:
        return None
    ratio = (bull - bear) / total  # in [-1, +1]
    return ratio * 10.0
