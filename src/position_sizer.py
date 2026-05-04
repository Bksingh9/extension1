"""Fractional Kelly position sizing.

  Kelly fraction = W - (1 - W) / R
  where W = win rate, R = avg_win / avg_loss.

We use 1/4 Kelly. We also enforce a hard max of `max_position_pct` of equity
and require the trade-risk dollar amount to stay within `max_risk_per_trade_pct`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .settings import config

SIZING = config["sizing"]
RISK = config["risk"]


@dataclass
class SizingResult:
    qty: float
    notional: float
    kelly_fraction_used: float
    win_rate: float
    win_loss_ratio: float
    reason: str = "ok"


def _stats_from_trades(trades: Iterable[dict]) -> tuple[float, float]:
    wins = [t["pnl_r"] for t in trades if t.get("pnl_r") is not None and t["pnl_r"] > 0]
    losses = [-t["pnl_r"] for t in trades if t.get("pnl_r") is not None and t["pnl_r"] < 0]
    n = len(wins) + len(losses)
    if n < 5:
        return SIZING["default_win_rate"], SIZING["default_win_loss_ratio"]
    win_rate = len(wins) / n
    avg_win = sum(wins) / len(wins) if wins else 0.0
    avg_loss = sum(losses) / len(losses) if losses else 1.0
    ratio = (avg_win / avg_loss) if avg_loss > 0 else SIZING["default_win_loss_ratio"]
    return win_rate, max(0.1, ratio)


def kelly_fraction(win_rate: float, win_loss_ratio: float) -> float:
    if win_loss_ratio <= 0:
        return 0.0
    return win_rate - (1.0 - win_rate) / win_loss_ratio


def size_position(*, equity: float, entry: float, stop: float, recent_trades: list[dict]) -> SizingResult:
    if entry <= 0 or stop <= 0 or stop >= entry:
        return SizingResult(0.0, 0.0, 0.0, 0.0, 0.0, reason="invalid_bracket")

    win_rate, ratio = _stats_from_trades(recent_trades[: SIZING["lookback_trades"]])
    raw_kelly = kelly_fraction(win_rate, ratio)
    if raw_kelly <= 0:
        return SizingResult(0.0, 0.0, raw_kelly, win_rate, ratio, reason="non_positive_kelly")

    fractional = raw_kelly * SIZING["kelly_fraction"]
    fractional = min(fractional, RISK["max_position_pct"])

    risk_per_share = entry - stop
    risk_budget = RISK["max_risk_per_trade_pct"] * equity
    qty_by_risk = risk_budget / risk_per_share

    target_notional = fractional * equity
    qty_by_kelly = target_notional / entry

    qty = max(0.0, min(qty_by_risk, qty_by_kelly))
    qty_int = float(int(qty))  # whole shares for equities
    notional = qty_int * entry

    if qty_int < 1:
        return SizingResult(0.0, 0.0, fractional, win_rate, ratio, reason="size_below_one_share")

    return SizingResult(
        qty=qty_int,
        notional=notional,
        kelly_fraction_used=fractional,
        win_rate=win_rate,
        win_loss_ratio=ratio,
        reason="ok",
    )
