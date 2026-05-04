"""Routine 5 — Friday weekly review (16:30 ET, Fridays).

- Summarize the past 5 trading days from the audit DB.
- Compute win rate, avg R, expectancy, max DD; per-strategy breakdown.
- Append the analysis to memory/weekly-review.md.
- Suggest weight adjustments by writing a structured block — applying them
  to config.json is operator-approved, not automatic.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.audit import recent_closed_trades  # noqa: E402
from src.journal import append_weekly_review, today_str  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.notify import send as notify_send  # noqa: E402

log = get_logger()


def _summary(trades: list[dict]) -> dict:
    if not trades:
        return {"n": 0, "win_rate": None, "avg_r": None, "expectancy": None}
    rs = [t["pnl_r"] for t in trades if t.get("pnl_r") is not None]
    if not rs:
        return {"n": len(trades), "win_rate": None, "avg_r": None, "expectancy": None}
    wins = [r for r in rs if r > 0]
    win_rate = len(wins) / len(rs)
    avg_r = mean(rs)
    return {"n": len(rs), "win_rate": win_rate, "avg_r": avg_r, "expectancy": avg_r}


def main() -> int:
    trades = recent_closed_trades(200)
    overall = _summary(trades)

    by_strategy: dict[str, list[dict]] = defaultdict(list)
    for t in trades:
        by_strategy[t["strategy"]].append(t)

    lines = [
        f"## {today_str()} — Weekly review",
        "",
        f"- Closed trades analyzed: **{overall['n']}**",
    ]
    if overall["win_rate"] is not None:
        lines.append(f"- Win rate: **{overall['win_rate']*100:.1f}%**")
        lines.append(f"- Avg R / expectancy: **{overall['expectancy']:.2f}R**")
    lines.append("")
    lines.append("### By strategy")
    lines.append("")
    lines.append("| Strategy | N | Win % | Avg R |")
    lines.append("|---|---|---|---|")
    for name, ts in sorted(by_strategy.items()):
        s = _summary(ts)
        wr = f"{s['win_rate']*100:.1f}%" if s["win_rate"] is not None else "—"
        ar = f"{s['avg_r']:.2f}" if s["avg_r"] is not None else "—"
        lines.append(f"| {name} | {s['n']} | {wr} | {ar} |")

    lines.append("")
    lines.append("### Suggested weight changes (operator review required)")
    lines.append("")
    suggestions = []
    for name, ts in by_strategy.items():
        s = _summary(ts)
        if s["expectancy"] is None:
            continue
        if s["expectancy"] > 0.5 and s["n"] >= 10:
            suggestions.append(f"- Increase weight on **{name}** (expectancy {s['expectancy']:.2f}R, n={s['n']})")
        elif s["expectancy"] < -0.25 and s["n"] >= 10:
            suggestions.append(f"- Decrease weight on **{name}** (expectancy {s['expectancy']:.2f}R, n={s['n']})")
    if not suggestions:
        suggestions.append("- No weight changes suggested this week.")
    lines.extend(suggestions)

    append_weekly_review("\n".join(lines))
    notify_send(
        f"Weekly review: n={overall['n']}, "
        + (f"WR={overall['win_rate']*100:.1f}% " if overall["win_rate"] is not None else "")
        + (f"E={overall['expectancy']:.2f}R" if overall["expectancy"] is not None else "")
    )
    log.info(f"[friday] weekly review written, n={overall['n']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
