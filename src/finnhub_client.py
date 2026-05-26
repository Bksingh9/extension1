"""Thin Finnhub REST client.

Free tier limits: 60 requests/minute. We touch only two endpoints:
  - /company-news?symbol=X&from=YYYY-MM-DD&to=YYYY-MM-DD
  - /calendar/earnings?from=YYYY-MM-DD&to=YYYY-MM-DD&symbol=X

Both endpoints are free; sentiment scoring (premium) is NOT used — we
score the headlines ourselves via Claude (see src/news.py).

All functions degrade gracefully: if no key is configured or a request
fails, they return an empty/neutral value rather than raising.
"""
from __future__ import annotations

import time
from datetime import date, timedelta
from typing import Optional

from .logging_setup import get_logger
from .settings import settings

log = get_logger()

BASE = "https://finnhub.io/api/v1"
TIMEOUT = 6
_MIN_INTERVAL = 1.05  # ~ 60 req/min ceiling
_last_call_ts = 0.0


def _throttle() -> None:
    global _last_call_ts
    delta = time.time() - _last_call_ts
    if delta < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - delta)
    _last_call_ts = time.time()


def _get(path: str, params: dict) -> Optional[dict | list]:
    if not settings.finnhub_api_key:
        return None
    try:
        import requests
    except ImportError:
        return None
    _throttle()
    full_params = {**params, "token": settings.finnhub_api_key}
    try:
        r = requests.get(f"{BASE}{path}", params=full_params, timeout=TIMEOUT)
        if r.status_code == 429:
            log.warning("finnhub rate-limited (429)")
            return None
        if r.status_code >= 400:
            log.warning(f"finnhub {path} returned {r.status_code}: {r.text[:200]}")
            return None
        return r.json()
    except Exception as e:
        log.warning(f"finnhub {path} failed: {e}")
        return None


def company_news(symbol: str, days_back: int = 3, max_items: int = 12) -> list[str]:
    """Return recent headlines for a symbol over the last `days_back` days."""
    today = date.today()
    start = today - timedelta(days=days_back)
    data = _get(
        "/company-news",
        {"symbol": symbol, "from": start.isoformat(), "to": today.isoformat()},
    )
    if not isinstance(data, list):
        return []
    headlines: list[str] = []
    for it in data[:max_items]:
        h = it.get("headline") if isinstance(it, dict) else None
        if h:
            headlines.append(str(h))
    return headlines


def has_earnings_within(symbol: str, days: int = 2) -> bool:
    """True if the symbol has an earnings event in the next `days` days."""
    today = date.today()
    end = today + timedelta(days=days)
    data = _get(
        "/calendar/earnings",
        {"from": today.isoformat(), "to": end.isoformat(), "symbol": symbol},
    )
    if not isinstance(data, dict):
        return False
    items = data.get("earningsCalendar") or []
    return len(items) > 0
