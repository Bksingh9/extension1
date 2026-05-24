"""Tests for the deterministic risk + sizing core. No network.

Run:  python -m pytest scripts/test_risk.py -q
 or:  python scripts/test_risk.py   (falls back to a plain runner)
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kelly_size import kelly_fraction, b_from_contract_price, size_position
from validate_risk import Account, TradeProposal, Limits, validate


# ── Kelly math ──────────────────────────────────────────────────────
def test_kelly_even_money_positive_edge():
    # p=0.6 at even money → f = (0.6 - 0.4)/1 = 0.20
    assert math.isclose(kelly_fraction(0.6, 1.0), 0.20, abs_tol=1e-9)


def test_kelly_2to1():
    # p=0.7, b=2 → (1.4 - 0.3)/2 = 0.55  (the correct value; the PDF's
    # "12%" figure does not match the standard formula)
    assert math.isclose(kelly_fraction(0.7, 2.0), 0.55, abs_tol=1e-9)


def test_kelly_no_edge_clamped_zero():
    assert kelly_fraction(0.5, 1.0) == 0.0          # break-even
    assert kelly_fraction(0.4, 1.0) == 0.0          # negative → clamp


def test_contract_price_to_odds():
    # buy at $0.50 → even money
    assert math.isclose(b_from_contract_price(0.5), 1.0, abs_tol=1e-9)
    # buy at $0.25 → 3:1
    assert math.isclose(b_from_contract_price(0.25), 3.0, abs_tol=1e-9)


def test_quarter_kelly_and_position_cap():
    # full Kelly 0.55, quarter = 0.1375, but hard cap 5% binds
    s = size_position(bankroll=10_000, p_win=0.7, net_odds_b=2.0,
                      fractional=0.25, max_position_frac=0.05)
    assert math.isclose(s.full_fraction, 0.55, abs_tol=1e-6)
    assert s.used_fraction == 0.05          # capped
    assert s.stake == 500.0
    assert s.capped_by == "max_position"


def test_quarter_kelly_uncapped():
    # small edge so quarter-Kelly is below the 5% cap
    s = size_position(bankroll=10_000, p_win=0.55, net_odds_b=1.0,
                      fractional=0.25, max_position_frac=0.05)
    # full = (0.55-0.45)/1 = 0.10 ; quarter = 0.025 → $250
    assert math.isclose(s.full_fraction, 0.10, abs_tol=1e-6)
    assert math.isclose(s.used_fraction, 0.025, abs_tol=1e-6)
    assert s.stake == 250.0
    assert s.capped_by == "kelly"


# ── Risk gate ───────────────────────────────────────────────────────
def _base_account():
    return Account(bankroll=10_000, open_exposure=0, open_positions=0,
                   realized_pnl_today=0, peak_bankroll=10_000, ai_spend_today=0)


def test_clean_trade_approved(tmp_path=None):
    # ensure no STOP file in cwd
    if Path("STOP").exists():
        Path("STOP").unlink()
    prop = TradeProposal("mkt1", p_model=0.62, p_market=0.50, stake=250, net_odds_b=1.0)
    d = validate(prop, _base_account())
    assert d.approved, d.failed()


def test_insufficient_edge_rejected():
    prop = TradeProposal("mkt1", p_model=0.52, p_market=0.50, stake=100, net_odds_b=1.0)
    d = validate(prop, _base_account())
    assert not d.approved
    assert "edge" in d.failed()


def test_oversized_position_rejected():
    # stake way above 5% cap ($500) on $10k bankroll
    prop = TradeProposal("mkt1", p_model=0.62, p_market=0.50, stake=2_000, net_odds_b=1.0)
    d = validate(prop, _base_account())
    assert not d.approved
    assert "position" in d.failed()


def test_drawdown_blocks():
    acct = _base_account()
    acct.peak_bankroll = 12_000          # 10k now vs 12k peak = 16.7% dd
    prop = TradeProposal("mkt1", p_model=0.62, p_market=0.50, stake=250, net_odds_b=1.0)
    d = validate(prop, acct)
    assert not d.approved
    assert "drawdown" in d.failed()


def test_daily_loss_limit_blocks():
    acct = _base_account()
    acct.realized_pnl_today = -1_600     # 16% loss vs 15% cap
    prop = TradeProposal("mkt1", p_model=0.62, p_market=0.50, stake=250, net_odds_b=1.0)
    d = validate(prop, acct)
    assert not d.approved
    assert "daily_loss" in d.failed()


def test_concurrency_blocks():
    acct = _base_account()
    acct.open_positions = 15
    prop = TradeProposal("mkt1", p_model=0.62, p_market=0.50, stake=250, net_odds_b=1.0)
    d = validate(prop, acct)
    assert not d.approved
    assert "concurrency" in d.failed()


def test_kill_switch_blocks():
    stop = Path("STOP")
    stop.write_text("halt")
    try:
        prop = TradeProposal("mkt1", p_model=0.62, p_market=0.50, stake=250, net_odds_b=1.0)
        d = validate(prop, _base_account())
        assert not d.approved
        assert "kill_switch" in d.failed()
    finally:
        stop.unlink()


def test_ai_budget_blocks():
    acct = _base_account()
    acct.ai_spend_today = 50.0
    prop = TradeProposal("mkt1", p_model=0.62, p_market=0.50, stake=250, net_odds_b=1.0)
    d = validate(prop, acct)
    assert not d.approved
    assert "ai_budget" in d.failed()


# ── plain runner fallback ───────────────────────────────────────────
if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS {fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL {fn.__name__}: {e}")
        except Exception as e:
            print(f"  ERR  {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{passed}/{len(fns)} passed")
    sys.exit(0 if passed == len(fns) else 1)
