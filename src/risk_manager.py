"""Pre-trade risk gate. Deterministic and auditable.

Every order MUST pass `RiskManager.check()` before submission. Each blocked
trade returns a `RiskDecision(approved=False, reason=...)` with a single
canonical reason string suitable for journaling and audit.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timezone
from typing import Iterable

from .audit import record_event
from .settings import config

RISK = config["risk"]


@dataclass
class PortfolioState:
    equity: float
    cash: float
    open_positions: dict[str, float]  # symbol -> qty
    open_position_count: int
    day_pnl_pct: float  # e.g. -0.012 for -1.2%
    day_trade_count_5d: int  # rolling 5 business days
    trading_blocked: bool
    now_et: datetime


@dataclass
class OrderProposal:
    symbol: str
    strategy: str
    side: str
    entry: float
    stop: float
    target: float
    qty: float
    notional: float


@dataclass
class RiskDecision:
    approved: bool
    reason: str = "ok"


def _cutoff(close_h: int, close_m: int, no_trade_min: int) -> time:
    total = close_h * 60 + close_m - no_trade_min
    return time(total // 60, total % 60)


def _trading_window(market: str, rc: dict) -> tuple[time, time]:
    nt = rc.get("no_trade_minutes_before_close", RISK.get("no_trade_minutes_before_close", 5))
    if market == "india":
        return time(9, 15), _cutoff(15, 30, nt)  # NSE 09:15–15:30 IST
    return time(9, 35), _cutoff(16, 0, nt)        # US 09:30–16:00 ET (enter from 09:35)


def check(
    proposal: OrderProposal,
    state: PortfolioState,
    *,
    risk_cfg: dict | None = None,
    market: str = "us",
) -> RiskDecision:
    p = proposal
    s = state
    rc = risk_cfg if risk_cfg is not None else RISK

    if s.trading_blocked:
        return _deny(p, "account_trading_blocked")

    open_t, cutoff = _trading_window(market, rc)
    if not (open_t <= s.now_et.time() <= cutoff):
        return _deny(p, "outside_trading_window")

    if s.day_pnl_pct <= -rc.get("max_daily_drawdown_pct", RISK["max_daily_drawdown_pct"]):
        return _deny(p, "daily_drawdown_circuit_breaker")

    if s.open_position_count >= rc["max_open_positions"]:
        return _deny(p, "max_open_positions_reached")

    if p.symbol in s.open_positions:
        return _deny(p, "duplicate_symbol_position")

    if p.entry < rc["min_price"] or p.entry > rc["max_price"]:
        return _deny(p, "price_out_of_range")

    if p.stop is None or p.stop <= 0:
        return _deny(p, "missing_stop")
    if p.target is None or p.target <= 0:
        return _deny(p, "missing_target")

    risk_per_share = p.entry - p.stop
    reward_per_share = p.target - p.entry
    if risk_per_share <= 0 or reward_per_share <= 0:
        return _deny(p, "invalid_bracket")

    min_stop_distance = rc.get("min_atr_stop_pct", RISK["min_atr_stop_pct"]) * p.entry
    if risk_per_share < min_stop_distance:
        return _deny(p, "stop_too_tight")

    min_rr = rc.get("min_r_r_ratio", RISK["min_r_r_ratio"])
    rr = reward_per_share / risk_per_share
    if rr < min_rr:
        return _deny(p, f"r_r_below_{min_rr}")

    trade_risk = risk_per_share * p.qty
    if trade_risk > rc["max_risk_per_trade_pct"] * s.equity:
        return _deny(p, "risk_per_trade_exceeds_cap")

    if p.notional > rc["max_position_pct"] * s.equity:
        return _deny(p, "position_size_exceeds_cap")

    # PDT applies to US margin accounts only.
    if market == "us" and s.equity < rc.get("pdt_account_threshold_usd", 25000.0):
        if s.day_trade_count_5d >= rc.get("pdt_max_day_trades", 3):
            return _deny(p, "pdt_limit_reached")

    record_event(
        "risk_approved",
        {
            "symbol": p.symbol,
            "strategy": p.strategy,
            "market": market,
            "entry": p.entry,
            "stop": p.stop,
            "target": p.target,
            "qty": p.qty,
            "notional": p.notional,
            "rr": rr,
        },
        symbol=p.symbol,
        strategy=p.strategy,
    )
    return RiskDecision(approved=True, reason="ok")


def _deny(p: OrderProposal, reason: str) -> RiskDecision:
    record_event(
        "risk_denied",
        {
            "symbol": p.symbol,
            "strategy": p.strategy,
            "reason": reason,
            "entry": p.entry,
            "stop": p.stop,
            "target": p.target,
            "qty": p.qty,
        },
        symbol=p.symbol,
        strategy=p.strategy,
    )
    return RiskDecision(approved=False, reason=reason)


def compute_bracket(entry: float, atr_value: float, min_stop_pct: float | None = None) -> tuple[float, float]:
    """Universal stop/target. Stop = max(1.5*ATR, min_stop_pct*entry); target = 2*stop_distance."""
    msp = min_stop_pct if min_stop_pct is not None else RISK["min_atr_stop_pct"]
    stop_distance = max(1.5 * atr_value, msp * entry)
    stop = round(entry - stop_distance, 2)
    target = round(entry + 2.0 * stop_distance, 2)
    return stop, target
