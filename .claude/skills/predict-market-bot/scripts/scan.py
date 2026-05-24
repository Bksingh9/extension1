"""Stage 1 — Scan: filter raw markets to a ranked, tradeable shortlist.

Pure functions over a list of market dicts so this is testable without any
network. Connectors (scripts/connectors/) supply the raw market dicts.

Expected market dict keys:
  id, question, volume, liquidity_usd, days_to_resolution,
  yes_price, spread_cents, price_move_pct, volume_7d_avg
"""
from __future__ import annotations

from dataclasses import dataclass, field

try:
    from .common import load_config
except ImportError:
    from common import load_config


@dataclass
class ScannedMarket:
    id: str
    question: str
    yes_price: float
    score: float
    flags: list[str] = field(default_factory=list)


def _is_tradeable(m: dict, scan_cfg: dict) -> bool:
    return (
        m.get("volume", 0) >= scan_cfg["min_volume_contracts"]
        and 0 < m.get("days_to_resolution", 9999) <= scan_cfg["max_days_to_resolution"]
        and m.get("liquidity_usd", 0) >= scan_cfg["min_liquidity_usd"]
    )


def _anomaly_flags(m: dict, scan_cfg: dict) -> list[str]:
    flags: list[str] = []
    if abs(m.get("price_move_pct", 0.0)) >= scan_cfg["anomaly_price_move_pct"]:
        flags.append("price_move")
    if m.get("spread_cents", 0.0) >= scan_cfg["anomaly_spread_cents"]:
        flags.append("wide_spread")
    avg = m.get("volume_7d_avg", 0) or 0
    if avg > 0 and m.get("volume", 0) >= scan_cfg["anomaly_volume_spike_mult"] * avg:
        flags.append("volume_spike")
    return flags


def _opportunity_score(m: dict, flags: list[str]) -> float:
    # More volume + tighter spread + anomaly presence => higher score.
    vol_term = min(1.0, m.get("volume", 0) / 5000.0)
    spread_term = max(0.0, 1.0 - m.get("spread_cents", 0.05) / 0.10)
    anomaly_term = min(1.0, 0.25 * len(flags))
    return round(0.4 * vol_term + 0.3 * spread_term + 0.3 * anomaly_term, 4)


def scan(markets: list[dict]) -> list[ScannedMarket]:
    scan_cfg = load_config()["scan"]
    out: list[ScannedMarket] = []
    for m in markets:
        if not _is_tradeable(m, scan_cfg):
            continue
        flags = _anomaly_flags(m, scan_cfg)
        out.append(
            ScannedMarket(
                id=str(m.get("id", "")),
                question=str(m.get("question", "")),
                yes_price=float(m.get("yes_price", 0.0)),
                score=_opportunity_score(m, flags),
                flags=flags,
            )
        )
    out.sort(key=lambda s: s.score, reverse=True)
    return out
