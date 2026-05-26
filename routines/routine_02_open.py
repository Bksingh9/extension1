"""Routine 2 — Market open execution (09:35 ET).

- Re-confirm signals on top-5 candidates from market-context.md.
- For each, compute bracket via universal stop/target rule.
- Size with fractional Kelly off recent journal trades.
- Run risk manager. Submit bracket on approve, log block reason on deny.
- Cap entries at remaining open-position budget and per-day max.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.allocation import decide as decide_allocation, remaining_exposure_budget  # noqa: E402
from src.audit import record_event, recent_closed_trades  # noqa: E402
from src.broker import MissingCredentialsError, get_broker  # noqa: E402
from src.journal import append_journal, today_str  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.notify import send as notify_send  # noqa: E402
from src.position_sizer import size_position  # noqa: E402
from src.regime import assess_with_default  # noqa: E402
from src.risk_manager import OrderProposal, PortfolioState, check, compute_bracket  # noqa: E402
from src.settings import config  # noqa: E402
from src.strategies import best_signal  # noqa: E402

from routines.routine_01_premarket import _bars  # noqa: E402

log = get_logger()
ET = ZoneInfo("America/New_York")
MAX_NEW_PER_DAY = 4


def _portfolio_state(broker) -> PortfolioState:
    acct = broker.account()
    positions = {p.symbol: p.qty for p in broker.positions()}
    day_pnl_pct = 0.0  # broker computes live; dry_run keeps 0
    return PortfolioState(
        equity=acct.equity,
        cash=acct.cash,
        open_positions=positions,
        open_position_count=len(positions),
        day_pnl_pct=day_pnl_pct,
        day_trade_count_5d=0,
        trading_blocked=acct.trading_blocked,
        now_et=datetime.now(ET),
    )


def main() -> int:
    try:
        broker = get_broker()
    except MissingCredentialsError as e:
        log.error(f"[open] {e}")
        return 2
    state = _portfolio_state(broker)
    if state.trading_blocked:
        log.warning("[open] account.trading_blocked → no entries submitted")
        return 0

    recent = recent_closed_trades(30)
    weights = config["strategy_weights"]

    # Regime gating on aggregate exposure.
    primary = config["regime"]["primary_symbol"]
    primary_bars = _bars(primary, days=config["regime"]["lookback_days"])
    regime = assess_with_default(primary_bars) if primary_bars is not None and not primary_bars.empty else None
    label = regime.label if regime else "NEUTRAL"
    confidence = regime.confidence if regime else 0.0
    alloc = decide_allocation(label, confidence)

    positions = broker.positions()
    current_notional = sum(p.market_value for p in positions)
    remaining_budget = remaining_exposure_budget(state.equity, current_notional, label, confidence)
    log.info(
        f"[open] regime={label} conf={confidence:.2f} cap={alloc.target_exposure_pct*100:.0f}% "
        f"current=${current_notional:,.0f} remaining=${remaining_budget:,.0f}"
    )

    placed = 0
    journal_lines = [
        f"## {today_str()} — Open execution",
        f"- Regime: **{alloc.effective_label}** (conf {confidence:.2f}, cap {alloc.target_exposure_pct*100:.0f}%, remaining ${remaining_budget:,.0f})",
    ]
    for symbol in config["watchlist"]:
        if placed >= MAX_NEW_PER_DAY:
            break
        if symbol in state.open_positions:
            continue

        bars = _bars(symbol, days=200)
        if bars is None or bars.empty:
            continue
        sig = best_signal(symbol, bars, weights)
        if sig is None:
            continue

        stop, target = compute_bracket(sig.entry, sig.atr)
        sizing = size_position(equity=state.equity, entry=sig.entry, stop=stop, recent_trades=recent)
        if sizing.qty < 1:
            record_event("size_zero", {"symbol": symbol, "reason": sizing.reason}, symbol=symbol)
            continue

        # Regime exposure gate — never exceed the aggregate cap for this regime.
        if sizing.notional > remaining_budget:
            scaled_qty = float(int(remaining_budget / sig.entry)) if sig.entry > 0 else 0.0
            if scaled_qty < 1:
                record_event(
                    "regime_exposure_cap",
                    {"symbol": symbol, "remaining_budget": remaining_budget, "wanted": sizing.notional},
                    symbol=symbol,
                )
                journal_lines.append(f"- BLOCKED {symbol}: regime_exposure_cap (remaining ${remaining_budget:,.0f})")
                continue
            sizing.qty = scaled_qty
            sizing.notional = scaled_qty * sig.entry

        proposal = OrderProposal(
            symbol=symbol,
            strategy=sig.strategy,
            side="buy",
            entry=sig.entry,
            stop=stop,
            target=target,
            qty=sizing.qty,
            notional=sizing.notional,
        )
        decision = check(proposal, state)
        if not decision.approved:
            log.info(f"[open] {symbol} blocked: {decision.reason}")
            journal_lines.append(f"- BLOCKED {symbol} ({sig.strategy}): {decision.reason}")
            continue

        broker.submit_bracket(
            symbol=symbol, qty=sizing.qty, entry=sig.entry, stop=stop, target=target, side="buy"
        )
        placed += 1
        state.open_positions[symbol] = sizing.qty
        state.open_position_count += 1
        remaining_budget -= sizing.notional
        line = (
            f"- BUY {sizing.qty:.0f} {symbol} @ {sig.entry:.2f} "
            f"stop {stop:.2f} target {target:.2f} "
            f"({sig.strategy}, score {sig.score:.2f}, {sig.notes})"
        )
        journal_lines.append(line)
        notify_send(f":chart_with_upwards_trend: {line}")

    if placed == 0:
        journal_lines.append("- No entries placed.")
    append_journal("\n".join(journal_lines))
    log.info(f"[open] placed {placed} bracket(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
