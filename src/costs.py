"""Transaction-cost model. Converts gross R-multiples to net-of-cost R, and
estimates after-tax aggregate expectancy.

Costs are expressed as a fraction of notional. A round trip charges entry +
exit fees, slippage on both legs, and (where applicable) a per-transfer levy
like India's 1% crypto TDS. Tax on gains (e.g. India crypto 30%, no loss
offset) is applied at the aggregate level, not per trade.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CostModel:
    entry_fee_bps: float = 0.0
    exit_fee_bps: float = 0.0
    slippage_bps: float = 5.0
    tds_pct: float = 0.0          # per round trip, fraction of notional (India crypto = 0.01)
    tax_pct: float = 0.0          # on gains (India crypto = 0.30)
    no_loss_offset: bool = False  # India crypto: losses cannot offset gains

    @classmethod
    def from_dict(cls, d: dict | None) -> "CostModel":
        d = d or {}
        return cls(
            entry_fee_bps=float(d.get("entry_fee_bps", 0.0)),
            exit_fee_bps=float(d.get("exit_fee_bps", 0.0)),
            slippage_bps=float(d.get("slippage_bps", 5.0)),
            tds_pct=float(d.get("tds_pct", 0.0)),
            tax_pct=float(d.get("tax_pct", 0.0)),
            no_loss_offset=bool(d.get("no_loss_offset", False)),
        )

    def roundtrip_fraction(self) -> float:
        """Fraction of notional lost to fees + slippage (both legs) + TDS."""
        bps = self.entry_fee_bps + self.exit_fee_bps + 2.0 * self.slippage_bps
        return bps / 10_000.0 + self.tds_pct


def net_r(gross_r: float, entry: float, stop: float, cm: CostModel) -> float:
    """Convert a gross R-multiple to net-of-cost R. Cost is a fraction of
    notional; expressed in R by dividing by the per-share risk (entry-stop)."""
    risk = entry - stop
    if risk <= 0:
        return gross_r
    cost_in_price = cm.roundtrip_fraction() * entry
    return gross_r - cost_in_price / risk


def after_tax_expectancy(net_rs: list[float], cm: CostModel) -> float:
    """Mean net-of-cost R after applying tax on gains. With no_loss_offset,
    tax hits the gross positive R sum; losses stay as-is and are not
    deductible. Without tax, returns the plain mean."""
    if not net_rs:
        return 0.0
    if cm.tax_pct <= 0:
        return sum(net_rs) / len(net_rs)
    if cm.no_loss_offset:
        taxed = [r * (1.0 - cm.tax_pct) if r > 0 else r for r in net_rs]
    else:
        total = sum(net_rs)
        taxed_total = total * (1.0 - cm.tax_pct) if total > 0 else total
        return taxed_total / len(net_rs)
    return sum(taxed) / len(taxed)
