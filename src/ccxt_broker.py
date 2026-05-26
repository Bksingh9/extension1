"""Crypto broker via ccxt (unified API across exchanges). 24/7 market.

Conforms to the Account / Position / submit_bracket interface in src/broker.py.

IMPORTANT:
- The operator must pick an exchange they can LEGALLY use in their jurisdiction
  (`CCXT_EXCHANGE`, `CCXT_API_KEY`, `CCXT_SECRET`). India: crypto is legal but
  taxed 30% + 1% TDS/transfer with no loss offset — keep turnover low (the cost
  model in config/crypto.json reflects this).
- The single ccxt SDK interaction is isolated and clearly flagged; verify
  method names against your installed ccxt version. Native brackets are not
  universal across exchanges, so live bracket placement (entry + reduce-only
  stop/target, or OCO where supported) is a documented TODO.
- Research bars use yfinance (`{SYM}-USD`) so scanning works without keys.

Degrades gracefully: missing creds raise MissingCredentialsError (handled by
the caller); dry_run returns a DryRunBroker.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from .audit import record_event
from .broker import Account, MissingCredentialsError, Position
from .logging_setup import get_logger
from .settings import settings

log = get_logger()


def crypto_bars_yf(symbol: str, days: int = 200) -> pd.DataFrame | None:
    """Daily crypto bars via yfinance using the -USD suffix. None on failure."""
    try:
        import yfinance as yf
        df = yf.download(f"{symbol}-USD", period=f"{max(days, 200)}d", interval="1d",
                         progress=False, auto_adjust=False)
        if df is None or df.empty:
            return None
        df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
        return df.tail(days)
    except Exception as e:
        log.debug(f"yfinance crypto fetch failed for {symbol}: {e}")
        return None


class CcxtBroker:
    """Thin wrapper over a ccxt exchange for spot crypto."""

    def __init__(self) -> None:
        if not settings.ccxt_api_key or not settings.ccxt_secret:
            raise MissingCredentialsError(
                "market=crypto needs CCXT_API_KEY and CCXT_SECRET in .env for a "
                f"legally-usable exchange (CCXT_EXCHANGE={settings.ccxt_exchange}). "
                "Set:\n  CCXT_EXCHANGE=...\n  CCXT_API_KEY=...\n  CCXT_SECRET=...\n"
                "  MARKET=crypto\n  TRADING_MODE=paper"
            )
        import ccxt

        klass = getattr(ccxt, settings.ccxt_exchange)
        self._ex = klass({"apiKey": settings.ccxt_api_key, "secret": settings.ccxt_secret,
                          "enableRateLimit": True})

    def account(self) -> Account:
        bal = self._ex.fetch_balance()
        total = bal.get("total", {}) if isinstance(bal, dict) else {}
        usd = float(total.get("USDT", total.get("USD", 0.0)) or 0.0)
        return Account(equity=usd, cash=usd, trading_blocked=False)

    def positions(self) -> list[Position]:
        out: list[Position] = []
        bal = self._ex.fetch_balance()
        total = bal.get("total", {}) if isinstance(bal, dict) else {}
        for asset, qty in total.items():
            if asset in ("USDT", "USD") or not qty:
                continue
            out.append(Position(symbol=asset, qty=float(qty), avg_entry_price=0.0,
                                market_value=0.0, unrealized_pl=0.0))
        return out

    def submit_bracket(self, *, symbol: str, qty: float, entry: float, stop: float,
                       target: float, side: str = "buy") -> dict[str, Any]:
        record_event("ccxt_order_intent",
                     {"symbol": symbol, "qty": qty, "entry": entry, "stop": stop,
                      "target": target, "mode": settings.trading_mode, "exchange": settings.ccxt_exchange},
                     symbol=symbol)
        if settings.trading_mode != "live":
            return {"status": "dry_run", "symbol": symbol, "qty": qty, "entry": entry,
                    "stop": stop, "target": target}
        # TODO: live limit entry + reduce-only stop/target (or OCO where the
        # exchange supports it). Verify against your ccxt version + exchange.
        return {"error": "live_ccxt_order_not_implemented",
                "hint": "wire limit entry + reduce-only stop/target per your exchange"}

    def get_bars(self, symbol: str, days: int = 200, timeframe: str = "1Day") -> pd.DataFrame:
        df = crypto_bars_yf(symbol, days=days)
        return df if df is not None else pd.DataFrame()


def get_crypto_broker():
    if settings.is_dry:
        from .broker import DryRunBroker
        return DryRunBroker()
    return CcxtBroker()
