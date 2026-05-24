"""Tests for the predict-market-bot Claude skill scripts.

The skill scripts live under .claude/skills/predict-market-bot/scripts/, which
isn't a normal import path, so we add it to sys.path here.
"""
import sys
from pathlib import Path

import pytest

SKILL_SCRIPTS = (
    Path(__file__).resolve().parent.parent
    / ".claude" / "skills" / "predict-market-bot" / "scripts"
)
sys.path.insert(0, str(SKILL_SCRIPTS))

import kelly_size  # noqa: E402
import predict  # noqa: E402
import scan  # noqa: E402
import validate_risk as vr  # noqa: E402
from connectors.kalshi import normalize_kalshi_market  # noqa: E402
from validate_risk import OrderProposal, PortfolioState  # noqa: E402


# ---------- kelly_size ----------

def test_net_odds_from_price():
    assert kelly_size.net_odds_from_price(1 / 3) == pytest.approx(2.0)
    assert kelly_size.net_odds_from_price(0.5) == pytest.approx(1.0)


def test_kelly_fraction_matches_formula():
    # p=0.7, b=2 -> (0.7*2 - 0.3)/2 = 0.55
    assert kelly_size.kelly_fraction(0.7, 2.0) == pytest.approx(0.55)


def test_kelly_negative_when_no_edge():
    # p=0.4, b=1 -> (0.4 - 0.6)/1 = -0.2
    assert kelly_size.kelly_fraction(0.4, 1.0) < 0


def test_size_position_caps_at_max_position_pct():
    r = kelly_size.size_position(bankroll=10_000, p_model=0.95, price=0.5)
    assert r.reason == "ok"
    assert r.stake_usd <= 0.05 * 10_000 + 1e-6  # 5% cap


def test_size_position_zero_on_negative_kelly():
    r = kelly_size.size_position(bankroll=10_000, p_model=0.40, price=0.5)
    assert r.stake_usd == 0.0
    assert r.reason == "non_positive_kelly"


def test_size_position_invalid_price():
    r = kelly_size.size_position(bankroll=10_000, p_model=0.7, price=1.5)
    assert r.reason == "invalid_price"


# ---------- predict ----------

def test_edge_and_ev():
    assert predict.edge(0.65, 0.49) == pytest.approx(0.16)
    assert predict.expected_value(0.65, 0.49) > 0


def test_brier_score_perfect_is_zero():
    assert predict.brier_score([1.0, 0.0], [1.0, 0.0]) == 0.0


def test_brier_score_worst_is_one():
    assert predict.brier_score([1.0, 0.0], [0.0, 1.0]) == 1.0


def test_ensemble_weighted_mean():
    # 0.65@0.5 + 0.55@0.5 = 0.60
    assert predict.ensemble_aggregate([(0.65, 0.5), (0.55, 0.5)]) == pytest.approx(0.60)


def test_assess_tradeable_when_edge_and_confidence_ok():
    p = predict.assess(p_model=0.65, p_market=0.49, std=0.05, confidence=0.8)
    assert p.tradeable
    assert p.reason == "ok"


def test_assess_blocks_small_edge():
    p = predict.assess(p_model=0.51, p_market=0.49, std=0.05, confidence=0.9)
    assert not p.tradeable
    assert p.reason == "edge_below_threshold"


def test_assess_blocks_low_confidence():
    p = predict.assess(p_model=0.70, p_market=0.49, std=0.05, confidence=0.4)
    assert not p.tradeable
    assert p.reason == "confidence_below_threshold"


# ---------- scan ----------

def _market(**over):
    base = dict(
        id="MKT", question="Will X happen?", volume=1000, liquidity_usd=2000,
        days_to_resolution=10, yes_price=0.5, spread_cents=0.02,
        price_move_pct=0.0, volume_7d_avg=500,
    )
    base.update(over)
    return base


def test_scan_filters_low_volume():
    out = scan.scan([_market(volume=50)])
    assert out == []


def test_scan_filters_far_resolution():
    out = scan.scan([_market(days_to_resolution=90)])
    assert out == []


def test_scan_flags_anomalies():
    out = scan.scan([_market(price_move_pct=0.15, spread_cents=0.08, volume=2000, volume_7d_avg=500)])
    assert len(out) == 1
    assert "price_move" in out[0].flags
    assert "wide_spread" in out[0].flags
    assert "volume_spike" in out[0].flags


def test_scan_ranks_by_score():
    a = _market(id="A", volume=5000, spread_cents=0.01)
    b = _market(id="B", volume=300, spread_cents=0.05)
    out = scan.scan([b, a])
    assert out[0].id == "A"


# ---------- validate_risk ----------

def _state(**over):
    base = dict(
        bankroll=10_000.0, open_exposure_usd=0.0, open_position_count=0,
        day_pnl_pct=0.0, drawdown_pct=0.0, var_pct=0.0, ai_cost_today_usd=0.0,
    )
    base.update(over)
    return PortfolioState(**base)


def _proposal(**over):
    base = dict(
        market_id="MKT", side="yes", price=0.5, stake_usd=300.0,
        p_model=0.65, p_market=0.49, expected_slippage_pct=0.0,
    )
    base.update(over)
    return OrderProposal(**base)


def test_risk_happy_path():
    d = vr.check(_proposal(), _state())
    assert d.approved, d.reason


def test_risk_blocks_small_edge():
    d = vr.check(_proposal(p_model=0.50, p_market=0.49), _state())
    assert not d.approved
    assert d.reason == "edge_below_threshold"


def test_risk_blocks_drawdown():
    d = vr.check(_proposal(), _state(drawdown_pct=0.09))
    assert not d.approved
    assert d.reason == "max_drawdown_block"


def test_risk_blocks_daily_loss():
    d = vr.check(_proposal(), _state(day_pnl_pct=-0.16))
    assert not d.approved
    assert d.reason == "daily_loss_limit"


def test_risk_blocks_too_many_positions():
    d = vr.check(_proposal(), _state(open_position_count=15))
    assert not d.approved
    assert d.reason == "max_concurrent_positions"


def test_risk_blocks_oversize_vs_kelly():
    d = vr.check(_proposal(stake_usd=5000.0), _state())
    assert not d.approved
    assert d.reason in {"exceeds_kelly_size", "exceeds_max_position"}


def test_risk_blocks_exposure():
    d = vr.check(_proposal(stake_usd=400.0), _state(open_exposure_usd=5900.0))
    assert not d.approved
    assert d.reason == "exceeds_total_exposure"


def test_risk_blocks_slippage():
    d = vr.check(_proposal(expected_slippage_pct=0.05), _state())
    assert not d.approved
    assert d.reason == "slippage_too_high"


def test_risk_blocks_var():
    d = vr.check(_proposal(), _state(var_pct=0.20))
    assert not d.approved
    assert d.reason == "var_exceeds_limit"


# ---------- kalshi connector normalization (current API schema) ----------

def _raw_kalshi(**over):
    base = {
        "ticker": "KXTEMPNYCH-26MAY2412-T64.99",
        "title": "Will the temp in NYC be above 64.99 on May 24?",
        "volume_fp": "350",
        "volume_24h_fp": "120",
        "liquidity_dollars": "750.0000",
        "yes_bid_dollars": "0.4500",
        "yes_ask_dollars": "0.5000",
        "close_time": "2099-01-01T00:00:00Z",
    }
    base.update(over)
    return base


def test_normalize_parses_string_fields():
    n = normalize_kalshi_market(_raw_kalshi())
    assert n["id"].startswith("KXTEMP")
    assert n["volume"] == 350.0
    assert n["liquidity_usd"] == 750.0
    assert n["yes_price"] == pytest.approx(0.475)          # mid of 0.45/0.50
    assert n["spread_cents"] == pytest.approx(0.05)
    assert n["volume_7d_avg"] == 120.0
    assert n["days_to_resolution"] > 30                    # 2099 far out


def test_normalize_handles_empty_demo_market():
    n = normalize_kalshi_market(_raw_kalshi(
        volume_fp=None, liquidity_dollars="0.0000",
        yes_bid_dollars="0.0000", yes_ask_dollars="0.0000",
    ))
    assert n["volume"] == 0.0
    assert n["liquidity_usd"] == 0.0
    assert n["yes_price"] == 0.0


def test_normalized_market_passes_scan_when_liquid():
    # Close within 30 days so it isn't filtered on time-to-resolution.
    from datetime import datetime, timedelta, timezone
    soon = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat().replace("+00:00", "Z")
    n = normalize_kalshi_market(_raw_kalshi(close_time=soon))
    out = scan.scan([n])
    assert len(out) == 1
    assert out[0].id.startswith("KXTEMP")


def test_normalized_empty_market_filtered_by_scan():
    n = normalize_kalshi_market(_raw_kalshi(volume_fp="0", liquidity_dollars="0.0000"))
    assert scan.scan([n]) == []
