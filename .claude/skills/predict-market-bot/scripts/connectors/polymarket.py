"""Polymarket CLOB connector (crypto-native, settles on Polygon).

Endpoints (verify against current docs):
  GET https://clob.polymarket.com/markets        -> markets
  GET https://clob.polymarket.com/book?token_id= -> orderbook
  POST order placement requires EIP-712 signed orders via py-clob-client.

Auth: orders are EIP-712 signed with a Polygon wallet key (POLYMARKET_PK) plus
API creds (POLYMARKET_API_KEY/SECRET/PASSPHRASE). Signing is non-trivial; use
the official py-clob-client. This connector reads public market data without a
key and degrades to [] on failure; live order placement is left as a marked
TODO to wire with py-clob-client.
"""
from __future__ import annotations

import os

try:
    from .base import Connector
except ImportError:
    from base import Connector

CLOB_BASE = "https://clob.polymarket.com"
TIMEOUT = 8


class PolymarketConnector(Connector):
    name = "polymarket"

    def __init__(self) -> None:
        self.pk = os.getenv("POLYMARKET_PK", "")
        self.api_key = os.getenv("POLYMARKET_API_KEY", "")

    def _get(self, path: str, params: dict | None = None):
        try:
            import requests
        except ImportError:
            return None
        try:
            r = requests.get(f"{CLOB_BASE}{path}", params=params or {}, timeout=TIMEOUT)
            if r.status_code >= 400:
                return None
            return r.json()
        except Exception:
            return None

    def list_markets(self, limit: int = 300) -> list[dict]:
        data = self._get("/markets")
        rows = data.get("data", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        out: list[dict] = []
        for m in rows[:limit]:
            tokens = m.get("tokens", []) or []
            yes_price = 0.0
            for t in tokens:
                if str(t.get("outcome", "")).lower() == "yes":
                    try:
                        yes_price = float(t.get("price", 0.0))
                    except (TypeError, ValueError):
                        yes_price = 0.0
            out.append(
                {
                    "id": m.get("condition_id", m.get("question_id", "")),
                    "question": m.get("question", ""),
                    "volume": m.get("volume", 0) or 0,
                    "liquidity_usd": m.get("liquidity", 0) or 0,
                    "days_to_resolution": _days_to(m.get("end_date_iso")),
                    "yes_price": yes_price,
                    "spread_cents": 0.0,
                    "price_move_pct": 0.0,
                    "volume_7d_avg": m.get("volume", 0) or 0,
                    "platform": "polymarket",
                }
            )
        return out

    def get_orderbook(self, market_id: str) -> dict:
        data = self._get("/book", {"token_id": market_id})
        return data if isinstance(data, dict) else {}

    def place_order(self, *, market_id: str, side: str, price: float, size: float, dry_run: bool = True) -> dict:
        if dry_run:
            return {"status": "dry_run", "market_id": market_id, "side": side, "price": price, "size": size}
        # TODO: EIP-712 signed order via py-clob-client. Requires POLYMARKET_PK.
        return {"error": "live_order_not_implemented", "hint": "use py-clob-client per references/platforms.md"}


def _days_to(end_iso) -> float:
    if not end_iso:
        return 9999.0
    try:
        from datetime import datetime, timezone
        dt = datetime.fromisoformat(str(end_iso).replace("Z", "+00:00"))
        return max(0.0, (dt - datetime.now(timezone.utc)).total_seconds() / 86400.0)
    except Exception:
        return 9999.0
