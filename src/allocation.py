"""Regime-based allocation engine.

Maps a (regime_label, confidence) tuple to a target portfolio exposure
percentage. If confidence is below the threshold, falls back to NEUTRAL.

This sits on top of the existing per-trade risk manager:
- Per-trade caps (1% risk, 10% size) still apply unconditionally.
- Allocation here gates *aggregate* exposure across all open positions.
"""
from __future__ import annotations

from dataclasses import dataclass

from .settings import config

REGIME_CFG = config["regime"]
ALLOC = REGIME_CFG["allocation_pct"]
DEFAULT_LABEL = REGIME_CFG["default_label_on_low_confidence"]
MIN_CONF = float(REGIME_CFG["min_confidence"])


@dataclass
class AllocationDecision:
    label: str
    effective_label: str
    confidence: float
    target_exposure_pct: float
    reason: str


def decide(label: str, confidence: float) -> AllocationDecision:
    if label not in ALLOC:
        # Unknown regime label, be conservative.
        return AllocationDecision(
            label=label,
            effective_label=DEFAULT_LABEL,
            confidence=confidence,
            target_exposure_pct=ALLOC[DEFAULT_LABEL],
            reason="unknown_label_default_neutral",
        )
    if confidence < MIN_CONF:
        return AllocationDecision(
            label=label,
            effective_label=DEFAULT_LABEL,
            confidence=confidence,
            target_exposure_pct=ALLOC[DEFAULT_LABEL],
            reason=f"low_confidence_below_{MIN_CONF}",
        )
    return AllocationDecision(
        label=label,
        effective_label=label,
        confidence=confidence,
        target_exposure_pct=ALLOC[label],
        reason="ok",
    )


def remaining_exposure_budget(equity: float, current_notional: float, label: str, confidence: float) -> float:
    """How much *more* dollar notional we may add right now under this regime.
    Negative result means we are over-exposed; caller should add nothing."""
    d = decide(label, confidence)
    cap_dollars = d.target_exposure_pct * equity
    return max(0.0, cap_dollars - current_notional)
