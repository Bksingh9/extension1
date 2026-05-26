"""Orchestrates the full dry-run pipeline: scan -> predict -> risk -> execute.

Research (Step 2) and the LLM ensemble (Step 3) supply p_model/confidence; in
this offline orchestration we accept them as inputs (or default to market price
so nothing trades without a real edge). Run:

    TRADING_MODE=dry_run python3 scripts/pipeline.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import trading_mode  # noqa: E402
from connectors.kalshi import KalshiConnector  # noqa: E402
from connectors.polymarket import PolymarketConnector  # noqa: E402
from execute import execute_order  # noqa: E402
from predict import assess  # noqa: E402
from scan import scan  # noqa: E402
from validate_risk import OrderProposal, PortfolioState, check  # noqa: E402


def run(*, bankroll: float = 10_000.0, model_probs: dict[str, float] | None = None) -> int:
    model_probs = model_probs or {}
    markets: list[dict] = []
    # demo=None -> respects KALSHI_DEMO env (default demo). Set KALSHI_DEMO=false
    # to scan real production markets (read-only, no auth).
    for conn in (KalshiConnector(), PolymarketConnector()):
        try:
            got = conn.list_markets(limit=300)
            markets.extend(got)
            print(f"[pipeline] {conn.name}: {len(got)} markets")
        except Exception as e:
            print(f"[pipeline] connector {conn.name} failed: {e}")

    shortlist = scan(markets)
    print(f"[pipeline] mode={trading_mode()} markets={len(markets)} tradeable={len(shortlist)}")

    state = PortfolioState(
        bankroll=bankroll, open_exposure_usd=0.0, open_position_count=0,
        day_pnl_pct=0.0, drawdown_pct=0.0, var_pct=0.0, ai_cost_today_usd=0.0,
    )

    placed = 0
    for sm in shortlist[:15]:
        # Without a real model probability we default to market price => zero edge => no trade.
        p_model = model_probs.get(sm.id, sm.yes_price)
        pred = assess(p_model=p_model, p_market=sm.yes_price, std=0.05, confidence=0.7)
        if not pred.tradeable:
            continue
        from kelly_size import size_position
        sized = size_position(bankroll=state.bankroll, p_model=p_model, price=sm.yes_price)
        if sized.stake_usd <= 0:
            continue
        proposal = OrderProposal(
            market_id=sm.id, side="yes", price=sm.yes_price, stake_usd=sized.stake_usd,
            p_model=p_model, p_market=sm.yes_price, expected_slippage_pct=0.0,
        )
        decision = check(proposal, state)
        if not decision.approved:
            print(f"[pipeline] {sm.id} blocked: {decision.reason}")
            continue
        # dry_run ack only; connector respects KALSHI_DEMO env.
        from connectors.kalshi import KalshiConnector as _K
        res = execute_order(_K(), market_id=sm.id, side="yes",
                            signal_price=sm.yes_price, current_price=sm.yes_price, size=sized.stake_usd)
        if res.placed:
            placed += 1
            state.open_exposure_usd += sized.stake_usd
            state.open_position_count += 1
            print(f"[pipeline] {res.mode} order {sm.id} ${sized.stake_usd}")
    print(f"[pipeline] placed {placed} order(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
