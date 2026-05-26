"""Bar-by-bar backtester with transaction costs and out-of-sample split.

Walks daily bars (yfinance) for a market's watchlist, fires the strategies on
each window, simulates the universal ATR bracket exit, then reports BOTH gross
and net-of-cost stats, split into in-sample (first 70%) and out-of-sample
(last 30%). OOS is the honest number.

Usage:
    python3 scripts/backtest.py --days 1000
    python3 scripts/backtest.py --market crypto --days 1000
    python3 scripts/backtest.py --market india --strategy momentum
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src.costs import after_tax_expectancy, net_r  # noqa: E402
from src.markets import get_profile  # noqa: E402
from src.risk_manager import compute_bracket  # noqa: E402
from src.strategies import ALL_STRATEGIES, best_signal  # noqa: E402


def _bars(ticker: str, days: int) -> pd.DataFrame:
    import yfinance as yf
    df = yf.download(ticker, period=f"{days+50}d", interval="1d", progress=False, auto_adjust=False)
    if df is None or df.empty:
        return pd.DataFrame()
    df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
    return df.tail(days)


def _simulate_trade(bars, entry_idx, entry, stop, target, max_hold_days=30):
    risk = entry - stop
    for j in range(entry_idx + 1, min(entry_idx + 1 + max_hold_days, len(bars))):
        h = float(bars["high"].iloc[j]); l = float(bars["low"].iloc[j])
        if l <= stop:
            return ((stop - entry) / risk, "stop")
        if h >= target:
            return ((target - entry) / risk, "target")
    last = float(bars["close"].iloc[min(entry_idx + max_hold_days, len(bars) - 1)])
    return ((last - entry) / risk, "time")


def _trade_record(market_min_stop, bars, i, sig):
    stop, target = compute_bracket(sig.entry, sig.atr, min_stop_pct=market_min_stop)
    gross, _ = _simulate_trade(bars, i, sig.entry, stop, target)
    return sig.strategy, sig.entry, stop, gross


def run(days: int, only_strategy: str | None, market: str) -> int:
    profile = get_profile(market)
    cm = profile.costs
    min_stop = profile.risk.get("min_atr_stop_pct", 0.005)
    weights = {k: (1.0 if (only_strategy is None or k == only_strategy) else 0.0) for k in ALL_STRATEGIES}

    # (gross_r, net_r) split by in/out-of-sample, per strategy.
    buckets = {"is": defaultdict(list), "oos": defaultdict(list)}
    total = 0

    for symbol in profile.watchlist:
        bars = _bars(profile.yf_symbol(symbol), days)
        if bars.empty or len(bars) < 80:
            continue
        split_idx = int(len(bars) * 0.70)
        i = 80
        while i < len(bars) - 1:
            window = bars.iloc[: i + 1]
            sig = best_signal(symbol, window, weights)
            if sig is None:
                i += 1
                continue
            strat, entry, stop, gross = _trade_record(min_stop, bars, i, sig)
            nr = net_r(gross, entry, stop, cm)
            bucket = "is" if i < split_idx else "oos"
            buckets[bucket][strat].append((gross, nr))
            total += 1
            i += 5

    print(f"\nBacktest — market={profile.name} ({profile.currency}), {total} signals, "
          f"{days}d, {len(profile.watchlist)} symbols")
    print(f"cost model: {cm.roundtrip_fraction()*100:.2f}% round-trip"
          + (f" + {cm.tax_pct*100:.0f}% tax (no loss offset)" if cm.tax_pct else ""))

    for label in ("is", "oos"):
        rows = buckets[label]
        print(f"\n[{'IN-SAMPLE' if label=='is' else 'OUT-OF-SAMPLE'}]")
        hdr = f"{'strategy':16}{'n':>5}{'win%':>8}{'grossR':>9}{'netR':>9}{'afterTax':>10}"
        print(hdr); print("-" * len(hdr))
        for name, pairs in sorted(rows.items()):
            if not pairs:
                continue
            gross = [g for g, _ in pairs]; nets = [n for _, n in pairs]
            wr = sum(1 for n in nets if n > 0) / len(nets) * 100
            at = after_tax_expectancy(nets, cm)
            print(f"{name:16}{len(nets):>5}{wr:>7.1f}%{sum(gross)/len(gross):>9.2f}"
                  f"{sum(nets)/len(nets):>9.2f}{at:>10.2f}")
        if not rows:
            print("(no signals)")

    print("\nNote: OUT-OF-SAMPLE net/after-tax expectancy is the honest number. "
          "If it is <= 0, do not deploy capital on this market/strategy.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=1000)
    p.add_argument("--strategy", type=str, default=None)
    p.add_argument("--market", type=str, default="us", help="us | india | crypto | forex")
    args = p.parse_args()
    return run(args.days, args.strategy, args.market)


if __name__ == "__main__":
    raise SystemExit(main())
