"""Alpha Vantage TIME_SERIES_DAILY fallback for OHLCV bars.

Free tier: 5 requests/minute, 500/day. Used only when the primary broker
(Alpaca) and yfinance both fail. Requires ALPHA_VANTAGE_API_KEY in .env.

Returns a pandas.DataFrame with columns: open, high, low, close, volume.
"""
from __future__ import annotations

import time

from .logging_setup import get_logger
from .settings import settings

log = get_logger()

BASE = "https://www.alphavantage.co/query"
TIMEOUT = 10
_MIN_INTERVAL = 12.5  # ~5 req/min ceiling
_last_call_ts = 0.0


def _throttle() -> None:
    global _last_call_ts
    delta = time.time() - _last_call_ts
    if delta < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - delta)
    _last_call_ts = time.time()


def get_daily_bars(symbol: str, days: int = 200):
    """Return last `days` daily bars, or None on failure."""
    if not settings.alpha_vantage_api_key:
        return None
    try:
        import pandas as pd
        import requests
    except ImportError:
        return None
    _throttle()
    try:
        r = requests.get(
            BASE,
            params={
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "outputsize": "compact" if days <= 100 else "full",
                "apikey": settings.alpha_vantage_api_key,
                "datatype": "json",
            },
            timeout=TIMEOUT,
        )
        if r.status_code >= 400:
            return None
        data = r.json() or {}
    except Exception as e:
        log.debug(f"alpha_vantage {symbol} failed: {e}")
        return None

    series = data.get("Time Series (Daily)")
    if not isinstance(series, dict) or not series:
        if "Note" in data or "Information" in data:
            log.warning(f"alpha_vantage throttled or limited: {data.get('Note') or data.get('Information')}")
        return None

    rows = []
    for date_str, vals in series.items():
        try:
            rows.append(
                {
                    "date": date_str,
                    "open": float(vals["1. open"]),
                    "high": float(vals["2. high"]),
                    "low": float(vals["3. low"]),
                    "close": float(vals["4. close"]),
                    "volume": float(vals["5. volume"]),
                }
            )
        except (KeyError, ValueError):
            continue
    import pandas as pd
    if not rows:
        return None
    df = pd.DataFrame(rows).sort_values("date").set_index("date")
    return df.tail(days)
