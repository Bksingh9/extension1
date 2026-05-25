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

from src.kite_broker import india_bars_yf  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.position_sizer import size_position  # noqa: E402
from src.risk_manager import compute_bracket  # noqa: E402
from src.settings import load_india_config  # noqa: E402
from src.strategies import best_signal  # noqa: E402

log = get_logger()
INDIA = load_india_config()


def in_price_range(price: float) -> bool:
    return INDIA["risk"]["min_price"] <= price <= INDIA["risk"]["max_price"]


def main(equity: float = 1_000_000.0) -> int:
    weights = {"momentum": 1.0, "mean_reversion": 1.0, "breakout": 1.0, "vwap_intraday": 1.0}
    candidates = []
    skipped = 0
    for symbol in INDIA["watchlist"]:
        bars = india_bars_yf(symbol, days=200)
        if bars is None or bars.empty:
            skipped += 1
            continue
        sig = best_signal(symbol, bars, weights)
        if sig is None:
            continue
        if not in_price_range(sig.entry):
            continue
        stop, target = compute_bracket(sig.entry, sig.atr)
        sizing = size_position(equity=equity, entry=sig.entry, stop=stop, recent_trades=[])
        if sizing.qty < 1:
            continue
        candidates.append((sig, stop, target, sizing))

    candidates.sort(key=lambda c: c[0].score, reverse=True)
    print(f"\nNSE scan — {len(INDIA['watchlist'])} symbols, {skipped} no-data, {len(candidates)} candidates")
    print(f"{'symbol':12}{'strategy':16}{'entry':>10}{'stop':>10}{'target':>10}{'qty':>8}{'score':>8}")
    print("-" * 74)
    for sig, stop, target, sizing in candidates[:10]:
        print(f"{sig.symbol:12}{sig.strategy:16}{sig.entry:>10.2f}{stop:>10.2f}{target:>10.2f}{sizing.qty:>8.0f}{sig.score:>8.2f}")
    if not candidates:
        print("(no candidates — markets closed, no edge, or no data)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
