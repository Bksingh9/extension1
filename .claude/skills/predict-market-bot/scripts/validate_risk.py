"""Deterministic pre-trade risk gate for prediction-market orders.

Every order must pass `check()` before execution. Single canonical reason on
denial. This is intentionally code, not prose — the same inputs always produce
the same decision.
"""
from __future__ import annotations

from dataclasses import dataclass, field

try:
    from .common import kill_switch_active, load_config
    from .kelly_size import size_position
except ImportError:
    from common import kill_switch_active, load_config
    from kelly_size import size_position


@dataclass
class PortfolioState:
    bankroll: float
    open_exposure_usd: float
    open_position_count: int
    day_pnl_pct: float        # e.g. -0.05 for -5% today
    drawdown_pct: float       # peak-to-trough, positive number e.g. 0.06
    var_pct: float            # current VaR(95%) as fraction of bankroll
    ai_cost_today_usd: float


@dataclass
class OrderProposal:
    market_id: str
    side: str                 # "yes" | "no"
    price: float              # 0..1
    stake_usd: float
    p_model: float
    p_market: float
    expected_slippage_pct: float = 0.0


@dataclass
class RiskDecision:
    approved: bool
    reason: str = "ok"
    checks: dict = field(default_factory=dict)


def check(proposal: OrderProposal, state: PortfolioState) -> RiskDecision:
    cfg = load_config()
    edge_cfg, sizing, risk = cfg["edge"], cfg["sizing"], cfg["risk"]
    checks: dict[str, bool] = {}

    def deny(reason: str) -> RiskDecision:
        return RiskDecision(approved=False, reason=reason, checks=checks)

    # 0. Kill switch
    checks["kill_switch"] = not kill_switch_active()
    if not checks["kill_switch"]:
        return deny("kill_switch_active")

    # 1. AI cost cap
    checks["ai_cost"] = state.ai_cost_today_usd <= risk["max_ai_cost_per_day_usd"]
    if not checks["ai_cost"]:
        return deny("ai_cost_cap_exceeded")

    # 2. Daily loss limit
    checks["daily_loss"] = state.day_pnl_pct > -risk["max_daily_loss_pct"]
    if not checks["daily_loss"]:
        return deny("daily_loss_limit")

    # 3. Max drawdown
    checks["drawdown"] = state.drawdown_pct < risk["max_drawdown_pct"]
    if not checks["drawdown"]:
        return deny("max_drawdown_block")

    # 4. Concurrent positions
    checks["positions"] = state.open_position_count < risk["max_concurrent_positions"]
    if not checks["positions"]:
        return deny("max_concurrent_positions")

    # 5. Edge
    checks["edge"] = (proposal.p_model - proposal.p_market) > edge_cfg["min_edge"]
    if not checks["edge"]:
        return deny("edge_below_threshold")

    # 6. Price sanity
    checks["price"] = 0.0 < proposal.price < 1.0
    if not checks["price"]:
        return deny("invalid_price")

    # 7. Position size within fractional Kelly
    sized = size_position(bankroll=state.bankroll, p_model=proposal.p_model, price=proposal.price)
    checks["kelly"] = sized.reason == "ok" and proposal.stake_usd <= sized.stake_usd + 1e-6
    if not checks["kelly"]:
        return deny("exceeds_kelly_size")

    # 8. Max position pct
    checks["max_position"] = proposal.stake_usd <= sizing["max_position_pct"] * state.bankroll + 1e-6
    if not checks["max_position"]:
        return deny("exceeds_max_position")

    # 9. Total exposure
    new_exposure = state.open_exposure_usd + proposal.stake_usd
    checks["exposure"] = new_exposure <= sizing["max_total_exposure_pct"] * state.bankroll + 1e-6
    if not checks["exposure"]:
        return deny("exceeds_total_exposure")

    # 10. VaR
    checks["var"] = state.var_pct <= risk["max_var_pct"]
    if not checks["var"]:
        return deny("var_exceeds_limit")

    # 11. Slippage
    checks["slippage"] = proposal.expected_slippage_pct <= risk["slippage_abort_pct"]
    if not checks["slippage"]:
        return deny("slippage_too_high")

    return RiskDecision(approved=True, reason="ok", checks=checks)
