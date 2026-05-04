"""Pull broker state and reconcile memory/positions.md."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.broker import get_broker  # noqa: E402
from src.journal import write_positions_table  # noqa: E402


def main() -> int:
    broker = get_broker()
    acct = broker.account()
    positions = broker.positions()
    print(f"equity ${acct.equity:,.2f} cash ${acct.cash:,.2f} positions={len(positions)}")
    rows = [
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
        for p in positions
    ]
    write_positions_table(rows)
    print("memory/positions.md updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
