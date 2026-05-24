"""Connector interface. Implementations: kalshi.py, polymarket.py.

A connector normalizes each platform into the market dict shape consumed by
scan.py:
  {id, question, volume, liquidity_usd, days_to_resolution,
   yes_price, spread_cents, price_move_pct, volume_7d_avg}
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Connector(ABC):
    name: str = "base"

    @abstractmethod
    def list_markets(self, limit: int = 300) -> list[dict]:
        """Return normalized market dicts. [] on failure."""

    @abstractmethod
    def get_orderbook(self, market_id: str) -> dict:
        """Return {'bids': [...], 'asks': [...]} or {} on failure."""

    @abstractmethod
    def place_order(self, *, market_id: str, side: str, price: float, size: float, dry_run: bool = True) -> dict:
        """Place a limit order. In dry_run, returns a simulated ack without
        touching the network. {} or {'error': ...} on failure."""
