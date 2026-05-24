"""Kelly Criterion position sizing for prediction-market trades.

Deterministic. No network. Importable + CLI.

    f* = (p*b - q) / b      # full Kelly fraction of bankroll
    q  = 1 - p

Use FRACTIONAL Kelly (0.25–0.5) in practice — full Kelly is optimal
in theory but brutally volatile. Default here is quarter-Kelly.

Note on the source PDF's worked example: it states "70% win prob,
2:1 reward/risk → full Kelly 12%". That doesn't tie out — the
standard formula gives 55% for p=0.7, b=2. We implement the correct
formula; see test_risk.py for the verified values. Treat any single
guide's dollar figures as illustrative, not authoritative.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class KellySize:
    full_fraction: float        # full Kelly fraction of bankroll [0,1]
    used_fraction: float        # after applying the fractional multiplier + caps
    stake: float                # dollar amount to bet
    capped_by: str              # which rule bound the size ("kelly", "max_position", "none")


def kelly_fraction(p_win: float, net_odds_b: float) -> float:
    """Full Kelly fraction. Clamped to 0 when there is no edge.

    p_win:      probability of winning  (0..1)
    net_odds_b: net decimal odds = payout/stake - 1.
                Even-money = 1.0. Prediction-market contract bought at
                price `c` that pays $1 has b = (1 - c) / c.
    """
    if not (0.0 < p_win < 1.0):
        raise ValueError("p_win must be in (0,1)")
    if net_odds_b <= 0:
        raise ValueError("net_odds_b must be > 0")
    q = 1.0 - p_win
    f = (p_win * net_odds_b - q) / net_odds_b
    return max(0.0, f)


def b_from_contract_price(price: float) -> float:
    """Net odds for a prediction-market contract bought at `price` (0..1),
    paying $1 on a win."""
    if not (0.0 < price < 1.0):
        raise ValueError("contract price must be in (0,1)")
    return (1.0 - price) / price


def size_position(
    *,
    bankroll: float,
    p_win: float,
    net_odds_b: float,
    fractional: float = 0.25,
    max_position_frac: float = 0.05,
) -> KellySize:
    """Return how much to stake, honoring fractional Kelly + a hard
    per-position cap (default 5% of bankroll, per the spec)."""
    if bankroll <= 0:
        raise ValueError("bankroll must be > 0")
    if not (0.0 < fractional <= 1.0):
        raise ValueError("fractional must be in (0,1]")

    full = kelly_fraction(p_win, net_odds_b)
    used = full * fractional
    capped_by = "kelly" if used > 0 else "none"
    if used > max_position_frac:
        used = max_position_frac
        capped_by = "max_position"
    stake = round(bankroll * used, 2)
    return KellySize(
        full_fraction=round(full, 6),
        used_fraction=round(used, 6),
        stake=stake,
        capped_by=capped_by,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Kelly position sizer")
    ap.add_argument("--bankroll", type=float, required=True)
    ap.add_argument("--p-win", type=float, required=True, help="model win probability 0..1")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--net-odds", type=float, help="net decimal odds (even money = 1.0)")
    g.add_argument("--contract-price", type=float, help="prediction-market price 0..1")
    ap.add_argument("--fractional", type=float, default=0.25, help="Kelly multiplier (default 0.25)")
    ap.add_argument("--max-position-frac", type=float, default=0.05)
    args = ap.parse_args()

    b = args.net_odds if args.net_odds is not None else b_from_contract_price(args.contract_price)
    result = size_position(
        bankroll=args.bankroll, p_win=args.p_win, net_odds_b=b,
        fractional=args.fractional, max_position_frac=args.max_position_frac,
    )
    print(f"full Kelly:    {result.full_fraction:.4%}")
    print(f"used fraction: {result.used_fraction:.4%}  (x{args.fractional} fractional)")
    print(f"stake:         ${result.stake:,.2f}")
    print(f"bounded by:    {result.capped_by}")


if __name__ == "__main__":
    main()
