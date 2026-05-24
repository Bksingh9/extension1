"""Stage 5 — Compound: trade log, failure classification, performance metrics.

Trades persist to a JSONL ledger next to the skill. Metrics are computed with
plain Python (no heavy deps) so the skill stays self-contained.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    from .common import SKILL_DIR
except ImportError:
    from common import SKILL_DIR

LEDGER = SKILL_DIR / "references" / "trade_ledger.jsonl"
FAILURE_LOG = SKILL_DIR / "references" / "failure_log.md"

FAILURE_CLASSES = {"bad_prediction", "bad_timing", "bad_execution", "external_shock"}


@dataclass
class TradeRecord:
    market_id: str
    entry_price: float
    exit_price: float
    predicted_prob: float
    outcome: float           # 1.0 win, 0.0 loss
    pnl_usd: float
    held_minutes: float
    note: str = ""


def log_trade(rec: TradeRecord) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    row = asdict(rec)
    row["ts"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def classify_failure(rec: TradeRecord) -> str:
    """Heuristic post-mortem label for a losing trade."""
    if rec.pnl_usd >= 0:
        return "win"
    # Confident but wrong -> prediction problem.
    if abs(rec.predicted_prob - rec.outcome) >= 0.5:
        return "bad_prediction"
    # Big adverse move while held a long time -> timing.
    if rec.held_minutes > 60 and rec.exit_price < rec.entry_price:
        return "bad_timing"
    # Quick adverse fill -> execution.
    if rec.held_minutes <= 10:
        return "bad_execution"
    return "external_shock"


def append_failure_lesson(rec: TradeRecord, label: str) -> None:
    FAILURE_LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    line = (
        f"- {ts} `{rec.market_id}` **{label}** "
        f"pred={rec.predicted_prob:.2f} outcome={rec.outcome:.0f} "
        f"pnl=${rec.pnl_usd:.2f} — {rec.note}\n"
    )
    with open(FAILURE_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def _load_ledger() -> list[dict]:
    if not LEDGER.exists():
        return []
    rows = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def metrics(rows: list[dict] | None = None) -> dict:
    rows = _load_ledger() if rows is None else rows
    if not rows:
        return {"n": 0, "win_rate": None, "profit_factor": None, "brier": None, "max_drawdown": None}

    pnls = [r["pnl_usd"] for r in rows]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    win_rate = len(wins) / len(pnls)
    gross_win = sum(wins)
    gross_loss = -sum(losses)
    profit_factor = (gross_win / gross_loss) if gross_loss > 0 else None

    preds = [r.get("predicted_prob") for r in rows if r.get("predicted_prob") is not None]
    outs = [r.get("outcome") for r in rows if r.get("predicted_prob") is not None]
    brier = sum((p - o) ** 2 for p, o in zip(preds, outs)) / len(preds) if preds else None

    # Max drawdown on the cumulative equity curve.
    equity, peak, max_dd = 0.0, 0.0, 0.0
    for p in pnls:
        equity += p
        peak = max(peak, equity)
        if peak > 0:
            max_dd = max(max_dd, (peak - equity) / peak)

    return {
        "n": len(pnls),
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "brier": brier,
        "max_drawdown": max_dd,
    }
