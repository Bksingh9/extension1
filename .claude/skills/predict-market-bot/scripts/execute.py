"""Stage 4b — Execution. Places (or simulates) a limit order after risk passes.

Enforces: STOP kill switch, slippage abort, and mode gating (dry_run/paper/live).
Live requires TRADING_MODE=live AND ALLOW_LIVE=true.
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    from .common import allow_live, kill_switch_active, load_config, trading_mode
except ImportError:
    from common import allow_live, kill_switch_active, load_config, trading_mode


@dataclass
class ExecutionResult:
    placed: bool
    mode: str
    detail: dict
    reason: str = "ok"


def execute_order(
    connector,
    *,
    market_id: str,
    side: str,
    signal_price: float,
    current_price: float,
    size: float,
) -> ExecutionResult:
    mode = trading_mode()
    cfg = load_config()["risk"]

    if kill_switch_active():
        return ExecutionResult(False, mode, {}, reason="kill_switch_active")

    if signal_price > 0:
        slippage = abs(current_price - signal_price) / signal_price
        if slippage > cfg["slippage_abort_pct"]:
            return ExecutionResult(False, mode, {"slippage": slippage}, reason="slippage_abort")

    if mode == "live" and not allow_live():
        return ExecutionResult(False, mode, {}, reason="live_blocked_allow_live_false")

    dry = mode != "live"
    ack = connector.place_order(
        market_id=market_id, side=side, price=current_price, size=size, dry_run=dry
    )
    if isinstance(ack, dict) and ack.get("error"):
        return ExecutionResult(False, mode, ack, reason=ack["error"])
    return ExecutionResult(True, mode, ack if isinstance(ack, dict) else {}, reason="ok")
