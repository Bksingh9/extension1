"""Kalshi REST connector (US-regulated event exchange).

Endpoints (verify against current docs — Kalshi has revised paths over time):
  GET {base}/markets            -> active markets
  GET {base}/markets/{ticker}/orderbook
  POST {base}/portfolio/orders  -> place order (auth required)

Base URLs:
  demo: https://demo-api.kalshi.co/trade-api/v2
  prod: https://api.elections.kalshi.com/trade-api/v2

Auth: API key id + RSA-signed request headers (KALSHI_API_KEY_ID,
KALSHI_PRIVATE_KEY). Signing is non-trivial; see references/platforms.md.
This connector degrades to [] when creds are absent or requests fail. The
signing/auth is intentionally left as a clearly-marked TODO so you wire it
against your installed Kalshi client version.
"""
from __future__ import annotations

import os

try:
    from .base import Connector
except ImportError:
    from base import Connector

DEMO_BASE = "https://demo-api.kalshi.co/trade-api/v2"
PROD_BASE = "https://api.elections.kalshi.com/trade-api/v2"
TIMEOUT = 8


class KalshiConnector(Connector):
    name = "kalshi"

    def __init__(self, demo: bool = True) -> None:
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
        out: list[dict] = []
        for m in data.get("markets", []) or []:
            yes = m.get("yes_bid")
            yes_price = (yes / 100.0) if isinstance(yes, (int, float)) else 0.0
            out.append(
                {
                    "id": m.get("ticker", ""),
                    "question": m.get("title", ""),
                    "volume": m.get("volume", 0),
                    "liquidity_usd": m.get("liquidity", 0) / 100.0 if m.get("liquidity") else 0,
                    "days_to_resolution": _days_to(m.get("close_time")),
                    "yes_price": yes_price,
                    "spread_cents": _spread_cents(m.get("yes_bid"), m.get("yes_ask")),
                    "price_move_pct": 0.0,
                    "volume_7d_avg": m.get("volume", 0),
                    "platform": "kalshi",
                }
            )
        return out

    def get_orderbook(self, market_id: str) -> dict:
        data = self._get(f"/markets/{market_id}/orderbook")
        return data if isinstance(data, dict) else {}

    def place_order(self, *, market_id: str, side: str, price: float, size: float, dry_run: bool = True) -> dict:
        if dry_run:
            return {"status": "dry_run", "market_id": market_id, "side": side, "price": price, "size": size}
        # TODO: real signed POST /portfolio/orders. Requires KALSHI_PRIVATE_KEY
        # RSA-PSS request signing — verify against your Kalshi client version.
        return {"error": "live_order_not_implemented", "hint": "wire signed POST per references/platforms.md"}


def _days_to(close_time) -> float:
    if not close_time:
        return 9999.0
    try:
        from datetime import datetime, timezone
        dt = datetime.fromisoformat(str(close_time).replace("Z", "+00:00"))
        return max(0.0, (dt - datetime.now(timezone.utc)).total_seconds() / 86400.0)
    except Exception:
        return 9999.0


def _spread_cents(bid, ask) -> float:
    if isinstance(bid, (int, float)) and isinstance(ask, (int, float)):
        return abs(ask - bid) / 100.0
    return 0.0
