"""Indian-market (NSE) dry-run scan.

Reuses the market-agnostic core (strategies, ATR bracket, Kelly sizer) on NSE
daily bars (yfinance .NS), applies the India price-range gate, and prints
ranked candidates with sized brackets. dry_run only — places no orders.

    MARKET=india TRADING_MODE=dry_run python3 scripts/india_scan.py

For paper/live you also need KITE_API_KEY + KITE_ACCESS_TOKEN; order placement
goes through src/kite_broker.py (bracket emulation is a documented TODO).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from datetime import datetime  # noqa: E402
from zoneinfo import ZoneInfo  # noqa: E402

from src.kite_broker import india_bars_yf  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.position_sizer import size_position  # noqa: E402
from src.risk_manager import OrderProposal, PortfolioState, check, compute_bracket  # noqa: E402
from src.settings import load_india_config  # noqa: E402
from src.strategies import best_signal  # noqa: E402

log = get_logger()
INDIA = load_india_config()
IST = ZoneInfo("Asia/Kolkata")


def main(equity: float = 1_000_000.0) -> int:
    weights = {"momentum": 1.0, "mean_reversion": 1.0, "breakout": 1.0, "vwap_intraday": 1.0}
    rc = INDIA["risk"]
    state = PortfolioState(
        equity=equity, cash=equity, open_positions={}, open_position_count=0,
        day_pnl_pct=0.0, day_trade_count_5d=0, trading_blocked=False,
        now_et=datetime.now(IST),  # field name is legacy; we pass IST-aware now
    )

    rows = []
    skipped = 0
    for symbol in INDIA["watchlist"]:
        bars = india_bars_yf(symbol, days=200)
        if bars is None or bars.empty:
            skipped += 1
            continue
        sig = best_signal(symbol, bars, weights)
        if sig is None:
            continue
        stop, target = compute_bracket(sig.entry, sig.atr, min_stop_pct=rc["min_atr_stop_pct"])
        sizing = size_position(equity=equity, entry=sig.entry, stop=stop, recent_trades=[])
        if sizing.qty < 1:
            continue
        proposal = OrderProposal(
            symbol=symbol, strategy=sig.strategy, side="buy", entry=sig.entry,
            stop=stop, target=target, qty=sizing.qty, notional=sizing.notional,
        )
        decision = check(proposal, state, risk_cfg=rc, market="india")
        rows.append((sig, stop, target, sizing, decision))

    rows.sort(key=lambda r: r[0].score, reverse=True)
    print(f"\nNSE scan — {len(INDIA['watchlist'])} symbols, {skipped} no-data, {len(rows)} signals")
    print(f"{'symbol':12}{'strategy':14}{'entry':>10}{'stop':>10}{'target':>10}{'qty':>7}{'score':>7}  risk")
    print("-" * 84)
    for sig, stop, target, sizing, decision in rows[:15]:
        verdict = "OK" if decision.approved else decision.reason
        print(f"{sig.symbol:12}{sig.strategy:14}{sig.entry:>10.2f}{stop:>10.2f}{target:>10.2f}"
              f"{sizing.qty:>7.0f}{sig.score:>7.2f}  {verdict}")
    if not rows:
        print("(no signals — markets closed, no edge, or no data)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
