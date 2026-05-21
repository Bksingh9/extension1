"""Simple bar-by-bar backtester.

For each symbol in the watchlist, walk daily bars from yfinance, fire all
strategies on each day's data window, simulate the universal bracket exit,
and aggregate stats. Used to gate strategy admission per memory/strategy.md §9.

Usage:
    python3 scripts/backtest.py --days 1000
    python3 scripts/backtest.py --days 500 --strategy momentum
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src.risk_manager import compute_bracket  # noqa: E402
from src.settings import config  # noqa: E402
from src.strategies import ALL_STRATEGIES, best_signal  # noqa: E402


def _bars(symbol: str, days: int) -> pd.DataFrame:
    import yfinance as yf
    df = yf.download(symbol, period=f"{days+50}d", interval="1d", progress=False, auto_adjust=False)
    if df is None or df.empty:
        return pd.DataFrame()
    df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
    return df.tail(days)


def _simulate_trade(bars: pd.DataFrame, entry_idx: int, entry: float, stop: float, target: float, max_hold_days: int = 30) -> tuple[float, str]:
    """Return (R-multiple, exit_reason). Walk forward; first touch wins."""
    risk = entry - stop
    for j in range(entry_idx + 1, min(entry_idx + 1 + max_hold_days, len(bars))):
        h = float(bars["high"].iloc[j])
        l = float(bars["low"].iloc[j])
        if l <= stop:
            return ((stop - entry) / risk, "stop")
        if h >= target:
            return ((target - entry) / risk, "target")
    last = float(bars["close"].iloc[min(entry_idx + max_hold_days, len(bars) - 1)])
    return ((last - entry) / risk, "time")


def run(days: int, only_strategy: str | None) -> int:
    weights = {k: 1.0 for k in ALL_STRATEGIES}
    if only_strategy:
        weights = {k: (1.0 if k == only_strategy else 0.0) for k in ALL_STRATEGIES}

    by_strategy: dict[str, list[float]] = defaultdict(list)
    total_signals = 0

    for symbol in config["watchlist"]:
        bars = _bars(symbol, days)
        if bars.empty or len(bars) < 80:
            continue
        # Walk forward, recompute on each day window of >= 80 bars.
        i = 80
        while i < len(bars) - 1:
            window = bars.iloc[: i + 1]
            sig = best_signal(symbol, window, weights)
            if sig is None:
                i += 1
                continue
            stop, target = compute_bracket(sig.entry, sig.atr)
            r, _ = _simulate_trade(bars, i, sig.entry, stop, target)
            by_strategy[sig.strategy].append(r)
            total_signals += 1
            # Skip ahead by a few bars to avoid overlap in the same setup.
            i += 5

    try:
        import empyrical as ep  # noqa
        have_empyrical = True
    except ImportError:
        have_empyrical = False

    print(f"\nBacktest results — {total_signals} signals, {days} days, watchlist={len(config['watchlist'])}")
    header = f"{'strategy':16}{'n':>6}{'win%':>9}{'avg R':>9}{'std R':>9}{'sharpe':>9}{'sortino':>10}{'best':>8}{'worst':>8}"
    print(header)
    print("-" * len(header))
    for name, rs in sorted(by_strategy.items()):
        if not rs:
            continue
        s = pd.Series(rs)
        wins = (s > 0).sum()
        wr = wins / len(s) * 100
        ar = s.mean()
        std = s.std()
        if have_empyrical and len(s) >= 5:
            import empyrical as ep
            # Treat each trade R as a daily-like return for Sharpe/Sortino feel.
            sharpe = ep.sharpe_ratio(s, period="daily")
            sortino = ep.sortino_ratio(s, period="daily")
        else:
            sharpe = sortino = float("nan")
        print(
            f"{name:16}{len(s):>6}{wr:>8.1f}%{ar:>9.2f}{std:>9.2f}"
            f"{sharpe:>9.2f}{sortino:>10.2f}{s.max():>8.2f}{s.min():>8.2f}"
        )
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--days", type=int, default=1000)
    p.add_argument("--strategy", type=str, default=None)
    args = p.parse_args()
    return run(args.days, args.strategy)


if __name__ == "__main__":
    raise SystemExit(main())
