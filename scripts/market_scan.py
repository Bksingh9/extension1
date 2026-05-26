"""Generic dry-run scanner for any configured market.

Reuses the market-agnostic core (strategies, ATR bracket, Kelly sizer) plus the
market-aware risk gate. Bars come from yfinance via each market's symbol
mapping, so scanning works with no broker keys. Places no orders.

    python3 scripts/market_scan.py --market crypto
    python3 scripts/market_scan.py --market forex
    python3 scripts/market_scan.py --market india --equity 1000000
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src.logging_setup import get_logger  # noqa: E402
from src.markets import get_profile  # noqa: E402
from src.position_sizer import size_position  # noqa: E402
from src.risk_manager import OrderProposal, PortfolioState, check, compute_bracket  # noqa: E402
from src.strategies import best_signal  # noqa: E402

log = get_logger()

_TZ = {"us": ZoneInfo("America/New_York"), "india": ZoneInfo("Asia/Kolkata"),
       "india_fx": ZoneInfo("Asia/Kolkata"), "crypto": ZoneInfo("UTC")}


def _bars(ticker: str, days: int = 200) -> pd.DataFrame | None:
    try:
        import yfinance as yf
        df = yf.download(ticker, period=f"{max(days,200)}d", interval="1d", progress=False, auto_adjust=False)
        if df is None or df.empty:
            return None
        df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
        return df.tail(days)
    except Exception as e:
        log.debug(f"bars failed for {ticker}: {e}")
        return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--market", default="crypto", help="us | india | crypto | forex")
    p.add_argument("--equity", type=float, default=1_000_000.0)
    args = p.parse_args()

    prof = get_profile(args.market)
    rc = prof.risk
    tz = _TZ.get(prof.name, ZoneInfo("UTC"))
    state = PortfolioState(equity=args.equity, cash=args.equity, open_positions={},
                           open_position_count=0, day_pnl_pct=0.0, day_trade_count_5d=0,
                           trading_blocked=False, now_et=datetime.now(tz))
    weights = {"momentum": 1.0, "mean_reversion": 1.0, "breakout": 1.0, "vwap_intraday": 1.0}

    rows = []
    skipped = 0
    for symbol in prof.watchlist:
        bars = _bars(prof.yf_symbol(symbol), days=200)
        if bars is None or bars.empty:
            skipped += 1
            continue
        sig = best_signal(symbol, bars, weights)
        if sig is None:
            continue
        stop, target = compute_bracket(sig.entry, sig.atr, min_stop_pct=rc["min_atr_stop_pct"])
        sizing = size_position(equity=args.equity, entry=sig.entry, stop=stop, recent_trades=[])
        if sizing.qty < 1:
            continue
        prop = OrderProposal(symbol=symbol, strategy=sig.strategy, side="buy", entry=sig.entry,
                             stop=stop, target=target, qty=sizing.qty, notional=sizing.notional)
        decision = check(prop, state, risk_cfg=rc, market=prof.name)
        rows.append((sig, stop, target, sizing, decision))

    rows.sort(key=lambda r: r[0].score, reverse=True)
    cur = prof.currency
    print(f"\n{prof.name} scan ({cur}) — {len(prof.watchlist)} symbols, {skipped} no-data, {len(rows)} signals")
    print(f"{'symbol':12}{'strategy':14}{'entry':>12}{'stop':>12}{'target':>12}{'qty':>8}{'score':>7}  risk")
    print("-" * 92)
    for sig, stop, target, sizing, decision in rows[:15]:
        verdict = "OK" if decision.approved else decision.reason
        print(f"{sig.symbol:12}{sig.strategy:14}{sig.entry:>12.4f}{stop:>12.4f}{target:>12.4f}"
              f"{sizing.qty:>8.0f}{sig.score:>7.2f}  {verdict}")
    if not rows:
        print("(no signals — market closed, no edge, or no data)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
