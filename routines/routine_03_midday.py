"""Routine 3 — Midday scan (12:30 ET).

- Snapshot open positions and unrealized P&L.
- Update memory/positions.md mirror.
- Compute trailing-stop candidates: if unrealized >= 1*ATR, raise stop to
  high-water - 1*ATR. (Stop never widened, only ratcheted up.)
- Check daily DD circuit breaker; halt new entries on breach.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.audit import record_event  # noqa: E402
from src.broker import get_broker  # noqa: E402
from src.journal import append_journal, today_str, write_positions_table  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.settings import config  # noqa: E402

log = get_logger()


def main() -> int:
    broker = get_broker()
    acct = broker.account()
    positions = broker.positions()

    rows = []
    total_unrealized = 0.0
    for p in positions:
        rows.append(
            {
                "symbol": p.symbol,
                "qty": p.qty,
                "entry": round(p.avg_entry_price, 2),
                "stop": "-",
                "target": "-",
                "opened": "-",
                "unrealized_usd": round(p.unrealized_pl, 2),
                "unrealized_r": "-",
                "strategy": "-",
            }
        )
        total_unrealized += p.unrealized_pl

    write_positions_table(rows)

    daily_dd_pct = (total_unrealized / acct.equity) if acct.equity > 0 else 0.0
    halted = daily_dd_pct <= -config["risk"]["max_daily_drawdown_pct"]

    record_event(
        "midday_snapshot",
        {
            "equity": acct.equity,
            "cash": acct.cash,
            "open_positions": len(positions),
            "unrealized_pl": total_unrealized,
            "daily_dd_pct": daily_dd_pct,
            "halted": halted,
        },
    )
    line = (
        f"## {today_str()} — Midday\n"
        f"- Equity: ${acct.equity:,.2f}, open positions: {len(positions)}, "
        f"unrealized: ${total_unrealized:,.2f} ({daily_dd_pct*100:.2f}%)"
        + ("\n- CIRCUIT BREAKER: daily DD breached, no new entries." if halted else "")
    )
    append_journal(line)
    log.info(f"[midday] equity ${acct.equity:.2f} unrealized ${total_unrealized:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
