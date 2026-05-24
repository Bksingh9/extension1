"""Fractional Kelly position sizing for binary prediction-market contracts.

Kelly fraction for a bet:
    f* = (p * b - q) / b
where p = win probability, q = 1 - p, b = net decimal odds (payout/stake).

For a YES contract bought at price `price` (in dollars, 0..1) that pays $1 on
a win, net odds b = (1 - price) / price.

We use fractional Kelly (default 0.25) and cap at `max_position_pct` of bankroll.
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    from .common import load_config
except ImportError:  # when run as a loose script with scripts/ on sys.path
    from common import load_config


@dataclass
class SizingResult:
    stake_usd: float
    fraction_used: float
    kelly_raw: float
    reason: str = "ok"


def net_odds_from_price(price: float) -> float:
    """Decimal net odds b for a YES contract at `price` (0<price<1)."""
    if price <= 0 or price >= 1:
        raise ValueError("price must be strictly between 0 and 1")
    return (1.0 - price) / price


def kelly_fraction(p: float, b: float) -> float:
    if b <= 0:
        return 0.0
    q = 1.0 - p
    return (p * b - q) / b


def size_position(
    *,
    bankroll: float,
    p_model: float,
    price: float,
    kelly_fraction_mult: float | None = None,
    max_position_pct: float | None = None,
) -> SizingResult:
    cfg = load_config()
    frac_mult = cfg["sizing"]["kelly_fraction"] if kelly_fraction_mult is None else kelly_fraction_mult
    max_pos = cfg["sizing"]["max_position_pct"] if max_position_pct is None else max_position_pct

    if not (0.0 < price < 1.0):
        return SizingResult(0.0, 0.0, 0.0, reason="invalid_price")
    if not (0.0 <= p_model <= 1.0):
        return SizingResult(0.0, 0.0, 0.0, reason="invalid_probability")
    if bankroll <= 0:
        return SizingResult(0.0, 0.0, 0.0, reason="invalid_bankroll")

    b = net_odds_from_price(price)
    raw = kelly_fraction(p_model, b)
    if raw <= 0:
        return SizingResult(0.0, 0.0, raw, reason="non_positive_kelly")

    fraction = min(raw * frac_mult, max_pos)
    stake = round(fraction * bankroll, 2)
    return SizingResult(stake_usd=stake, fraction_used=fraction, kelly_raw=raw, reason="ok")


if __name__ == "__main__":
    # Doc example: $10k bankroll, 70% win prob, 2:1 reward/risk -> quarter-Kelly ~ 3%.
    r = size_position(bankroll=10_000, p_model=0.70, price=1 / 3)
    print(f"stake=${r.stake_usd} fraction={r.fraction_used:.3f} kelly_raw={r.kelly_raw:.3f}")
