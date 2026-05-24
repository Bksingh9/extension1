"""Alpaca broker wrapper with three modes:

- dry_run: no network calls. Synthetic state. Used for offline tests and
  CI smoke-tests. This is the default.
- paper:   real Alpaca paper-trading endpoint. Requires keys in .env.
- live:    real money. Hard-gated. Requires TRADING_MODE=live AND
           ALLOW_LIVE=true AND `memory/go-live.md` to exist with the exact
           string "GO LIVE CONFIRMED" on its own line.

Bracket orders are always submitted with stop AND target legs.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

import pandas as pd

from .audit import record_event
from .logging_setup import get_logger
from .settings import ROOT, settings

log = get_logger()

GO_LIVE_FILE = ROOT / "memory" / "go-live.md"
GO_LIVE_PHRASE = "GO LIVE CONFIRMED"


class MissingCredentialsError(RuntimeError):
    """Raised when paper/live mode is selected but Alpaca keys are absent."""


@dataclass
class Account:
    equity: float
    cash: float
    trading_blocked: bool


@dataclass
class Position:
    symbol: str
    qty: float
    avg_entry_price: float
    market_value: float
    unrealized_pl: float


def _live_gate_ok() -> bool:
    if not settings.allow_live:
        return False
    if not GO_LIVE_FILE.exists():
        return False
    return GO_LIVE_PHRASE in GO_LIVE_FILE.read_text(encoding="utf-8")


class DryRunBroker:
    """In-memory broker for offline runs. Equity defaults to $100k."""

    def __init__(self, starting_equity: float = 100_000.0) -> None:
        self._equity = starting_equity
        self._cash = starting_equity
        self._positions: dict[str, Position] = {}
        self._orders: list[dict[str, Any]] = []

    def account(self) -> Account:
        return Account(equity=self._equity, cash=self._cash, trading_blocked=False)

    def positions(self) -> list[Position]:
        return list(self._positions.values())

    def submit_bracket(
        self,
        *,
        symbol: str,
        qty: float,
        entry: float,
        stop: float,
        target: float,
        side: str = "buy",
    ) -> dict[str, Any]:
        order = {
            "symbol": symbol,
            "qty": qty,
            "entry": entry,
            "stop": stop,
            "target": target,
            "side": side,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "mode": "dry_run",
        }
        self._orders.append(order)
        notional = qty * entry
        self._cash -= notional
        self._positions[symbol] = Position(
            symbol=symbol, qty=qty, avg_entry_price=entry, market_value=notional, unrealized_pl=0.0
        )
        record_event("dry_run_order", order, symbol=symbol)
        log.info(f"[DRY] bracket {side} {qty} {symbol} @ {entry} stop {stop} target {target}")
        return order

    def close_all(self) -> int:
        n = len(self._positions)
        for p in list(self._positions.values()):
            self._cash += p.market_value
        self._positions.clear()
        record_event("dry_run_close_all", {"closed": n})
        return n

    def get_bars(self, symbol: str, days: int = 200, timeframe: str = "1Day") -> pd.DataFrame:
        # No fake data — callers must use yfinance fallback in dry_run.
        return pd.DataFrame()


class AlpacaBroker:
    """Thin wrapper over alpaca-py for paper or live."""

    def __init__(self) -> None:
        if settings.is_live and not _live_gate_ok():
            raise RuntimeError(
                "live mode blocked: ALLOW_LIVE must be true AND memory/go-live.md "
                "must contain 'GO LIVE CONFIRMED'"
            )

        if not settings.alpaca_api_key or not settings.alpaca_secret_key:
            raise MissingCredentialsError(
                f"TRADING_MODE={settings.trading_mode} needs ALPACA_API_KEY and "
                "ALPACA_SECRET_KEY in .env. Generate a PAPER key at "
                "https://app.alpaca.markets (toggle 'Paper Trading' first), then set:\n"
                "  ALPACA_API_KEY=...\n"
                "  ALPACA_SECRET_KEY=...\n"
                "  ALPACA_BASE_URL=https://paper-api.alpaca.markets\n"
                "  TRADING_MODE=paper"
            )

        from alpaca.trading.client import TradingClient
        from alpaca.data.historical import StockHistoricalDataClient

        paper = not settings.is_live
        self._tc = TradingClient(
            api_key=settings.alpaca_api_key,
            secret_key=settings.alpaca_secret_key,
            paper=paper,
        )
        self._dc = StockHistoricalDataClient(
            api_key=settings.alpaca_api_key,
            secret_key=settings.alpaca_secret_key,
        )

    def account(self) -> Account:
        a = self._tc.get_account()
        return Account(
            equity=float(a.equity),
            cash=float(a.cash),
            trading_blocked=bool(a.trading_blocked),
        )

    def positions(self) -> list[Position]:
        out: list[Position] = []
        for p in self._tc.get_all_positions():
            out.append(
                Position(
                    symbol=p.symbol,
                    qty=float(p.qty),
                    avg_entry_price=float(p.avg_entry_price),
                    market_value=float(p.market_value),
                    unrealized_pl=float(p.unrealized_pl),
                )
            )
        return out

    def submit_bracket(
        self,
        *,
        symbol: str,
        qty: float,
        entry: float,
        stop: float,
        target: float,
        side: str = "buy",
    ) -> dict[str, Any]:
        from alpaca.trading.requests import (
            LimitOrderRequest,
            StopLossRequest,
            TakeProfitRequest,
        )
        from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass

        req = LimitOrderRequest(
            symbol=symbol,
            qty=int(qty),
            side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
            time_in_force=TimeInForce.DAY,
            limit_price=round(entry, 2),
            order_class=OrderClass.BRACKET,
            take_profit=TakeProfitRequest(limit_price=round(target, 2)),
            stop_loss=StopLossRequest(stop_price=round(stop, 2)),
        )
        order = self._tc.submit_order(req)
        record_event(
            "broker_order_submitted",
            {
                "id": str(getattr(order, "id", "")),
                "symbol": symbol,
                "qty": qty,
                "entry": entry,
                "stop": stop,
                "target": target,
                "mode": settings.trading_mode,
            },
            symbol=symbol,
        )
        return {"id": str(getattr(order, "id", "")), "symbol": symbol, "qty": qty}

    def close_all(self) -> int:
        # Cancels orders and liquidates positions. Operator-only via FLATTEN.
        self._tc.cancel_orders()
        closed = self._tc.close_all_positions(cancel_orders=True)
        return len(list(closed))

    def get_bars(self, symbol: str, days: int = 200, timeframe: str = "1Day") -> pd.DataFrame:
        from alpaca.data.requests import StockBarsRequest
        from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

        unit = TimeFrame.Day if timeframe == "1Day" else TimeFrame(5, TimeFrameUnit.Minute)
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=days * 2)  # buffer for non-trading days
        req = StockBarsRequest(symbol_or_symbols=symbol, timeframe=unit, start=start, end=end)
        bars = self._dc.get_stock_bars(req)
        df = bars.df
        if df.empty:
            return df
        if "symbol" in df.index.names:
            df = df.xs(symbol, level="symbol")
        df = df.rename(columns=str.lower)
        return df.tail(days)


def get_broker():
    if settings.is_dry:
        return DryRunBroker()
    return AlpacaBroker()
