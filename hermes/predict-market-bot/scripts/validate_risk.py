"""Deterministic risk gate for prediction-market trades.

EVERY rule must pass before the bot may execute. Code, not prose,
so the checks are identical every run. No network.

Rules (from the reference architecture):
  1. edge       : p_model - p_market > min_edge (default 0.04)
  2. position   : stake <= fractional-Kelly size AND <= max 5% bankroll
  3. exposure   : stake + open_exposure <= max_total_exposure
  4. var95      : 95% Value-at-Risk of the new book <= daily VaR limit
  5. drawdown   : current drawdown < max_drawdown (default 8%)
  6. daily_loss : today's realized loss < daily_loss_limit
  7. concurrency: open_positions < max_concurrent (default 15)
  8. ai_budget  : ai_spend_today < max_ai_cost_per_day (default $50)
  9. kill_switch: a STOP file must NOT exist
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

from kelly_size import size_position


@dataclass
class Account:
    bankroll: float
    open_exposure: float = 0.0          # $ currently at risk across open positions
    open_positions: int = 0
    realized_pnl_today: float = 0.0     # negative = loss
    peak_bankroll: float | None = None  # for drawdown; defaults to bankroll
    ai_spend_today: float = 0.0


@dataclass
class TradeProposal:
    market_id: str
    p_model: float          # your estimated win probability
    p_market: float         # current market price (= implied probability)
    stake: float            # $ you intend to bet
    net_odds_b: float       # net decimal odds for the contract


@dataclass
class Limits:
    min_edge: float = 0.04
    fractional_kelly: float = 0.25
    max_position_frac: float = 0.05
    max_total_exposure_frac: float = 0.30   # of bankroll
    daily_var_limit_frac: float = 0.10       # 95% VaR cap as frac of bankroll
    max_drawdown_frac: float = 0.08
    daily_loss_limit_frac: float = 0.15
    max_concurrent: int = 15
    max_ai_cost_per_day: float = 50.0
    kill_switch_path: str = "STOP"


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


@dataclass
class RiskDecision:
    approved: bool
    checks: list[CheckResult] = field(default_factory=list)

    def failed(self) -> list[str]:
        return [c.name for c in self.checks if not c.passed]


def _var95_loss(stake: float, p_win: float) -> float:
    """Crude 95% VaR for a binary contract: the loss incurred if the
    bet loses (you lose the full stake). For a single binary position
    the 95% VaR is `stake` when P(loss) > 5%, else 0."""
    p_loss = 1.0 - p_win
    return stake if p_loss > 0.05 else 0.0


def validate(proposal: TradeProposal, account: Account, limits: Limits | None = None) -> RiskDecision:
    limits = limits or Limits()
    checks: list[CheckResult] = []
    peak = account.peak_bankroll if account.peak_bankroll is not None else account.bankroll

    # 9. kill switch (checked first — a STOP file halts everything)
    kill = Path(limits.kill_switch_path)
    checks.append(CheckResult(
        "kill_switch", not kill.exists(),
        "STOP file present — trading halted" if kill.exists() else "no STOP file",
    ))

    # 1. edge
    edge = proposal.p_model - proposal.p_market
    checks.append(CheckResult(
        "edge", edge > limits.min_edge,
        f"edge={edge:.4f} (need > {limits.min_edge})",
    ))

    # 2. position size vs fractional Kelly + hard cap
    kelly = size_position(
        bankroll=account.bankroll, p_win=proposal.p_model,
        net_odds_b=proposal.net_odds_b, fractional=limits.fractional_kelly,
        max_position_frac=limits.max_position_frac,
    )
    checks.append(CheckResult(
        "position", proposal.stake <= kelly.stake + 1e-9,
        f"stake=${proposal.stake:,.2f} vs allowed ${kelly.stake:,.2f} ({kelly.capped_by})",
    ))

    # 3. exposure
    max_exp = account.bankroll * limits.max_total_exposure_frac
    new_exp = account.open_exposure + proposal.stake
    checks.append(CheckResult(
        "exposure", new_exp <= max_exp,
        f"new_exposure=${new_exp:,.2f} vs cap ${max_exp:,.2f}",
    ))

    # 4. VaR 95%
    var_cap = account.bankroll * limits.daily_var_limit_frac
    var = _var95_loss(proposal.stake, proposal.p_model)
    checks.append(CheckResult(
        "var95", var <= var_cap,
        f"VaR95=${var:,.2f} vs cap ${var_cap:,.2f}",
    ))

    # 5. drawdown
    dd = 0.0 if peak <= 0 else max(0.0, (peak - account.bankroll) / peak)
    checks.append(CheckResult(
        "drawdown", dd < limits.max_drawdown_frac,
        f"drawdown={dd:.4f} (block at {limits.max_drawdown_frac})",
    ))

    # 6. daily loss
    loss_today = max(0.0, -account.realized_pnl_today)
    loss_cap = account.bankroll * limits.daily_loss_limit_frac
    checks.append(CheckResult(
        "daily_loss", loss_today < loss_cap,
        f"loss_today=${loss_today:,.2f} vs cap ${loss_cap:,.2f}",
    ))

    # 7. concurrency
    checks.append(CheckResult(
        "concurrency", account.open_positions < limits.max_concurrent,
        f"open={account.open_positions} (max {limits.max_concurrent})",
    ))

    # 8. AI budget
    checks.append(CheckResult(
        "ai_budget", account.ai_spend_today < limits.max_ai_cost_per_day,
        f"ai_spend=${account.ai_spend_today:,.2f} (cap ${limits.max_ai_cost_per_day})",
    ))

    return RiskDecision(approved=all(c.passed for c in checks), checks=checks)


def _load(path: str | None, default: dict) -> dict:
    if not path:
        return default
    return json.loads(Path(path).read_text())


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate a trade against all risk rules")
    ap.add_argument("--proposal", help="JSON file: TradeProposal fields", required=False)
    ap.add_argument("--account", help="JSON file: Account fields", required=False)
    ap.add_argument("--limits", help="JSON file: Limits overrides", required=False)
    # inline fallbacks for quick checks
    ap.add_argument("--market-id", default="demo")
    ap.add_argument("--p-model", type=float)
    ap.add_argument("--p-market", type=float)
    ap.add_argument("--stake", type=float)
    ap.add_argument("--net-odds", type=float)
    ap.add_argument("--bankroll", type=float)
    args = ap.parse_args()

    if args.proposal:
        prop = TradeProposal(**_load(args.proposal, {}))
    else:
        if None in (args.p_model, args.p_market, args.stake, args.net_odds):
            ap.error("provide --proposal JSON or all of --p-model --p-market --stake --net-odds")
        prop = TradeProposal(args.market_id, args.p_model, args.p_market, args.stake, args.net_odds)

    if args.account:
        acct = Account(**_load(args.account, {}))
    else:
        if args.bankroll is None:
            ap.error("provide --account JSON or --bankroll")
        acct = Account(bankroll=args.bankroll)

    limits = Limits(**_load(args.limits, {})) if args.limits else Limits()

    decision = validate(prop, acct, limits)
    for c in decision.checks:
        print(f"  [{'PASS' if c.passed else 'FAIL'}] {c.name:12s} {c.detail}")
    print()
    print("APPROVED ✅" if decision.approved else f"REJECTED ❌  (failed: {', '.join(decision.failed())})")
    sys.exit(0 if decision.approved else 1)


if __name__ == "__main__":
    main()
