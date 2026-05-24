"""Prediction math: edge, expected value, mispricing z-score, Brier, ensemble.

Pure functions. No network, no LLM calls here — the LLM/ensemble votes are
passed in as numbers so this stays deterministic and testable.
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    from .common import load_config
except ImportError:
    from common import load_config


@dataclass
class Prediction:
    p_model: float
    p_market: float
    edge: float
    expected_value: float
    mispricing_z: float
    confidence: float
    tradeable: bool
    reason: str = "ok"


def edge(p_model: float, p_market: float) -> float:
    return p_model - p_market


def expected_value(p: float, price: float) -> float:
    """EV per $1 staked on a YES contract bought at `price`.
    Win pays (1/price - 1) net; loss costs 1. b = (1-price)/price."""
    if not (0.0 < price < 1.0):
        return 0.0
    b = (1.0 - price) / price
    return p * b - (1.0 - p)


def mispricing_z(p_model: float, p_market: float, std: float) -> float:
    if std <= 0:
        return 0.0
    return (p_model - p_market) / std


def brier_score(predictions: list[float], outcomes: list[float]) -> float:
    if not predictions or len(predictions) != len(outcomes):
        return float("nan")
    return sum((p - o) ** 2 for p, o in zip(predictions, outcomes)) / len(predictions)


def ensemble_aggregate(votes: list[tuple[float, float]]) -> float:
    """votes: list of (probability, weight). Returns weighted-mean probability."""
    total_w = sum(w for _, w in votes)
    if total_w <= 0:
        return 0.0
    return sum(p * w for p, w in votes) / total_w


def assess(
    *,
    p_model: float,
    p_market: float,
    std: float,
    confidence: float,
) -> Prediction:
    cfg = load_config()["edge"]
    e = edge(p_model, p_market)
    ev = expected_value(p_model, p_market)
    z = mispricing_z(p_model, p_market, max(std, cfg["max_mispricing_std_floor"]))

    tradeable = True
    reason = "ok"
    if e <= cfg["min_edge"]:
        tradeable, reason = False, "edge_below_threshold"
    elif confidence < cfg["min_confidence"]:
        tradeable, reason = False, "confidence_below_threshold"
    elif ev <= 0:
        tradeable, reason = False, "non_positive_ev"

    return Prediction(
        p_model=p_model,
        p_market=p_market,
        edge=e,
        expected_value=ev,
        mispricing_z=z,
        confidence=confidence,
        tradeable=tradeable,
        reason=reason,
    )
