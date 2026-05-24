"""Kalshi REST connector (US-regulated event exchange).

Endpoints (current schema as of 2026-05; verify against docs):
  GET {base}/markets?status=open&limit=...   -> active markets
  GET {base}/markets/{ticker}/orderbook
  POST {base}/portfolio/orders               -> place order (auth required)

Base URLs:
  demo: https://demo-api.kalshi.co/trade-api/v2   (mock funds; markets often empty)
  prod: https://api.elections.kalshi.com/trade-api/v2

Market fields are now string-typed:
  volume_fp, volume_24h_fp           (float-as-string)
  liquidity_dollars                  (USD string)
  yes_bid_dollars, yes_ask_dollars   (0..1 USD string)
  close_time                         (ISO 8601)

Auth (for order placement only): API key id + RSA-PSS request signing
(KALSHI_API_KEY_ID, KALSHI_PRIVATE_KEY). Read-only market discovery needs no
auth. Live order placement is a marked TODO. Degrades to [] on any failure.

Toggle demo/prod via the `demo` arg or KALSHI_DEMO env (default demo=true).
"""
from __future__ import annotations

import os
from datetime import datetime, timezone

try:
    from .base import Connector
except ImportError:
    from base import Connector

DEMO_BASE = "https://demo-api.kalshi.co/trade-api/v2"
PROD_BASE = "https://api.elections.kalshi.com/trade-api/v2"
TIMEOUT = 8


def _f(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def _mid(bid: float, ask: float) -> float:
    if bid > 0 and ask > 0:
        return (bid + ask) / 2.0
    return ask or bid or 0.0


def _days_to(close_time) -> float:
    if not close_time:
        return 9999.0
    try:
        dt = datetime.fromisoformat(str(close_time).replace("Z", "+00:00"))
        return max(0.0, (dt - datetime.now(timezone.utc)).total_seconds() / 86400.0)
    except Exception:
        return 9999.0


def normalize_kalshi_market(m: dict) -> dict:
    """Map a raw Kalshi market object to the scan.py market dict shape."""
    yes_bid = _f(m.get("yes_bid_dollars"))
    yes_ask = _f(m.get("yes_ask_dollars"))
    return {
        "id": m.get("ticker", ""),
        "question": m.get("title", ""),
        "volume": _f(m.get("volume_fp")),
        "liquidity_usd": _f(m.get("liquidity_dollars")),
        "days_to_resolution": _days_to(m.get("close_time")),
        "yes_price": _mid(yes_bid, yes_ask),
        "spread_cents": abs(yes_ask - yes_bid) if (yes_bid > 0 and yes_ask > 0) else 0.0,
        "price_move_pct": 0.0,
        "volume_7d_avg": _f(m.get("volume_24h_fp")),
        "platform": "kalshi",
    }


class KalshiConnector(Connector):
    name = "kalshi"

    def __init__(self, demo: bool | None = None) -> None:
        if demo is None:
            demo = os.getenv("KALSHI_DEMO", "true").lower() == "true"
        self.base = DEMO_BASE if demo else PROD_BASE
        self.key_id = os.getenv("KALSHI_API_KEY_ID", "")
        self.private_key = os.getenv("KALSHI_PRIVATE_KEY", "")

    def _get(self, path: str, params: dict | None = None):
        try:
            import requests
        except ImportError:
            return None
        try:
            r = requests.get(f"{self.base}{path}", params=params or {}, timeout=TIMEOUT)
            if r.status_code >= 400:
                return None
            return r.json()
        except Exception:
            return None

    def list_markets(self, limit: int = 300) -> list[dict]:
        data = self._get("/markets", {"limit": limit, "status": "open"})
        if not isinstance(data, dict):
            return []
        return [normalize_kalshi_market(m) for m in (data.get("markets", []) or [])]

    def get_orderbook(self, market_id: str) -> dict:
        data = self._get(f"/markets/{market_id}/orderbook")
        return data if isinstance(data, dict) else {}

    def place_order(self, *, market_id: str, side: str, price: float, size: float, dry_run: bool = True) -> dict:
        if dry_run:
            return {"status": "dry_run", "market_id": market_id, "side": side, "price": price, "size": size}
        # TODO: real signed POST /portfolio/orders. Requires KALSHI_PRIVATE_KEY
        # RSA-PSS request signing — verify against your Kalshi client version.
        return {"error": "live_order_not_implemented", "hint": "wire signed POST per references/platforms.md"}
