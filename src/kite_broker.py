"""Zerodha Kite Connect broker for the Indian market (NSE).

Conforms to the same Account / Position / submit_bracket interface as
src/broker.py:AlpacaBroker so the rest of the pipeline is broker-agnostic.

IMPORTANT — SDK surface and bracket emulation:
- The official client is `kiteconnect` (pip install kiteconnect). Auth uses an
  api_key + a daily access_token (obtained via the login flow). The single SDK
  interaction points are isolated and clearly marked; verify against your
  installed kiteconnect version (https://kite.trade/docs/connect/v3/).
- Kite DISCONTINUED native bracket orders (BO) in 2020. A bracket is therefore
  emulated with a LIMIT entry plus a GTT OCO (one-cancels-other) pair for
  stop/target. Live placement of that is left as a marked TODO — wire it with
  your account. dry_run is fully functional offline.

Everything degrades gracefully: missing creds raise MissingCredentialsError
(caught by the routine), and bars fall back to yfinance (.NS) so scanning
works without a Kite subscription.
"""
from __future__ import annotations

from typing import Any, Optional

import pandas as pd

from .audit import record_event
from .broker import Account, MissingCredentialsError, Position
from .logging_setup import get_logger
from .settings import load_india_config, settings

log = get_logger()
INDIA = load_india_config()


def india_bars_yf(symbol: str, days: int = 200) -> Optional[pd.DataFrame]:
    """Daily NSE bars via yfinance using the .NS suffix. None on failure."""
    try:
        import yfinance as yf
        ticker = f"{symbol}{INDIA['yfinance_suffix']}"
        df = yf.download(ticker, period=f"{max(days, 200)}d", interval="1d", progress=False, auto_adjust=False)
        if df is None or df.empty:
            return None
        df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
        return df.tail(days)
    except Exception as e:
        log.debug(f"yfinance NSE fetch failed for {symbol}: {e}")
        return None


class KiteBroker:
    """Thin wrapper over kiteconnect for NSE equities."""

    def __init__(self) -> None:
        if not settings.kite_api_key or not settings.kite_access_token:
            raise MissingCredentialsError(
                "market=india needs KITE_API_KEY and KITE_ACCESS_TOKEN in .env. "
                "Get them from a Kite Connect app at https://kite.trade and the "
                "daily login flow, then set:\n"
                "  KITE_API_KEY=...\n"
                "  KITE_ACCESS_TOKEN=...\n"
                "  MARKET=india\n"
                "  TRADING_MODE=paper"
            )
        from kiteconnect import KiteConnect

        self._kite = KiteConnect(api_key=settings.kite_api_key)
        self._kite.set_access_token(settings.kite_access_token)

    def account(self) -> Account:
        m = self._kite.margins()
        equity_block = m.get("equity", {}) if isinstance(m, dict) else {}
        net = float(equity_block.get("net", 0.0) or 0.0)
        available = equity_block.get("available", {}) or {}
        cash = float(available.get("cash", net) or net)
        return Account(equity=net, cash=cash, trading_blocked=False)

    def positions(self) -> list[Position]:
        out: list[Position] = []
        data = self._kite.positions()
        net = data.get("net", []) if isinstance(data, dict) else []
        for p in net:
            qty = float(p.get("quantity", 0) or 0)
            if qty == 0:
                continue
            out.append(
                Position(
                    symbol=p.get("tradingsymbol", ""),
                    qty=qty,
                    avg_entry_price=float(p.get("average_price", 0.0) or 0.0),
                    market_value=float(p.get("value", 0.0) or 0.0),
                    unrealized_pl=float(p.get("unrealised", p.get("pnl", 0.0)) or 0.0),
                )
            )
        return out

    def submit_bracket(
        self, *, symbol: str, qty: float, entry: float, stop: float, target: float, side: str = "buy"
    ) -> dict[str, Any]:
        # Live bracket emulation (LIMIT entry + GTT OCO for stop/target) is a
        # TODO — Kite removed native BO. Verify GTT API against your SDK version.
        record_event(
            "kite_order_intent",
            {"symbol": symbol, "qty": qty, "entry": entry, "stop": stop, "target": target, "mode": settings.trading_mode},
            symbol=symbol,
        )
        if settings.trading_mode != "live":
            return {"status": "dry_run", "symbol": symbol, "qty": qty, "entry": entry, "stop": stop, "target": target}
        return {"error": "live_kite_order_not_implemented", "hint": "wire LIMIT entry + GTT OCO per kite.trade docs"}

    def get_bars(self, symbol: str, days: int = 200, timeframe: str = "1Day") -> pd.DataFrame:
        df = india_bars_yf(symbol, days=days)
        return df if df is not None else pd.DataFrame()


def get_india_broker():
    if settings.is_dry:
        from .broker import DryRunBroker
        return DryRunBroker()
    return KiteBroker()
