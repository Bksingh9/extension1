"""Routine 4 — End-of-day summary (16:15 ET).

- Snapshot equity and P&L vs SPY benchmark.
- Append a daily recap to memory/journal.md.
- Send EOD notification with day's summary.
"""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.audit import record_event  # noqa: E402
from src.broker import get_broker  # noqa: E402
from src.journal import append_journal, today_str  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.notify import send as notify_send  # noqa: E402

log = get_logger()


def _spy_day_change_pct() -> Optional[float]:
    try:
        import yfinance as yf
        df = yf.download("SPY", period="5d", interval="1d", progress=False, auto_adjust=False)
        if df is None or len(df) < 2:
            return None
        close = df["Close"]
        return float((close.iloc[-1] / close.iloc[-2] - 1.0) * 100.0)
    except Exception as e:
        log.debug(f"SPY benchmark fetch failed: {e}")
        return None


def main() -> int:
    broker = get_broker()
    acct = broker.account()
    positions = broker.positions()

    unrealized = sum(p.unrealized_pl for p in positions)
    day_pct = (unrealized / acct.equity * 100.0) if acct.equity > 0 else 0.0
    spy_pct = _spy_day_change_pct()

    summary = (
        f"## {today_str()} — EOD\n"
        f"- Equity: ${acct.equity:,.2f}\n"
        f"- Open positions: {len(positions)}\n"
        f"- Unrealized P&L: ${unrealized:,.2f} ({day_pct:.2f}%)\n"
        + (f"- SPY day: {spy_pct:.2f}% — alpha: {day_pct - spy_pct:.2f}%\n" if spy_pct is not None else "")
        + "\nPositions:\n"
        + (
            "\n".join(
                f"  - {p.symbol} qty={p.qty} avg={p.avg_entry_price:.2f} unrealized=${p.unrealized_pl:,.2f}"
                for p in positions
            )
            or "  - (none)"
        )
    )
    append_journal(summary)
    record_event(
        "eod_snapshot",
        {
            "equity": acct.equity,
            "open_positions": len(positions),
            "unrealized_pl": unrealized,
            "day_pct": day_pct,
            "spy_pct": spy_pct,
        },
    )
    notify_send(
        f"EOD: equity ${acct.equity:,.0f}, day {day_pct:+.2f}%"
        + (f" vs SPY {spy_pct:+.2f}%" if spy_pct is not None else "")
        + f", {len(positions)} open"
    )
    log.info(f"[eod] equity ${acct.equity:.2f} day {day_pct:.2f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
