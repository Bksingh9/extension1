"""Markdown journal helpers. Append-only writes to /memory/*.md."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

from .settings import ROOT

MEM = ROOT / "memory"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def append_journal(section: str) -> None:
    p = MEM / "journal.md"
    body = _read(p)
    p.write_text(body.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")


def write_market_context(date_str: str, body: str) -> None:
    p = MEM / "market-context.md"
    header = f"# Market Context — {date_str}\n\n"
    p.write_text(header + body.strip() + "\n", encoding="utf-8")


def write_positions_table(rows: Iterable[dict]) -> None:
    p = MEM / "positions.md"
    lines = [
        "# Open Positions",
        "",
        "Updated by routines/routine_03_midday.py and routine_04_eod.py.",
        "Broker (Alpaca) is the source of truth; this file is a human-readable mirror.",
        "",
        "| Symbol | Strategy | Entry | Qty | Stop | Target | Opened | Unrealized $ | Unrealized R |",
        "|--------|----------|-------|-----|------|--------|--------|--------------|--------------|",
    ]
    rows = list(rows)
    if not rows:
        lines.append("| _(none)_ | | | | | | | | |")
    else:
        for r in rows:
            lines.append(
                f"| {r['symbol']} | {r.get('strategy','')} | {r.get('entry','')} | {r.get('qty','')} | "
                f"{r.get('stop','')} | {r.get('target','')} | {r.get('opened','')} | "
                f"{r.get('unrealized_usd','')} | {r.get('unrealized_r','')} |"
            )
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_weekly_review(section: str) -> None:
    p = MEM / "weekly-review.md"
    body = _read(p)
    p.write_text(body.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")
