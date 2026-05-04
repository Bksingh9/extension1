from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from src.risk_manager import OrderProposal, PortfolioState, check, compute_bracket

ET = ZoneInfo("America/New_York")


def _state(**over) -> PortfolioState:
    base = dict(
        equity=100_000.0,
        cash=50_000.0,
        open_positions={},
        open_position_count=0,
        day_pnl_pct=0.0,
        day_trade_count_5d=0,
        trading_blocked=False,
        now_et=datetime(2026, 5, 4, 10, 30, tzinfo=ET),  # Mon 10:30 ET
    )
    base.update(over)
    return PortfolioState(**base)


def _proposal(**over) -> OrderProposal:
    base = dict(
        symbol="AAPL",
        strategy="momentum",
        side="buy",
        entry=100.0,
        stop=98.0,
        target=104.0,
        qty=10,
        notional=1000.0,
    )
    base.update(over)
    return OrderProposal(**base)


def test_happy_path_approves():
    d = check(_proposal(), _state())
    assert d.approved


def test_blocks_when_trading_blocked():
    d = check(_proposal(), _state(trading_blocked=True))
    assert not d.approved
    assert d.reason == "account_trading_blocked"


def test_blocks_outside_window():
    after_close = datetime(2026, 5, 4, 16, 30, tzinfo=ET)
    d = check(_proposal(), _state(now_et=after_close))
    assert not d.approved


def test_blocks_circuit_breaker():
    d = check(_proposal(), _state(day_pnl_pct=-0.04))
    assert not d.approved
    assert d.reason == "daily_drawdown_circuit_breaker"


def test_blocks_max_open_positions():
    d = check(_proposal(), _state(open_position_count=10))
    assert not d.approved
    assert d.reason == "max_open_positions_reached"


def test_blocks_duplicate():
    d = check(_proposal(), _state(open_positions={"AAPL": 5}, open_position_count=1))
    assert not d.approved
    assert d.reason == "duplicate_symbol_position"


def test_blocks_price_out_of_range():
    d = check(_proposal(entry=2.0, stop=1.5, target=5.0, notional=20.0), _state())
    assert not d.approved
    assert d.reason == "price_out_of_range"


def test_blocks_missing_stop():
    d = check(_proposal(stop=0.0), _state())
    assert not d.approved
    assert d.reason == "missing_stop"


def test_blocks_low_rr():
    d = check(_proposal(entry=100.0, stop=98.0, target=101.0, qty=10, notional=1000.0), _state())
    assert not d.approved
    assert d.reason.startswith("r_r_below")


def test_blocks_oversized_position():
    # 15% of equity > 10% cap
    d = check(_proposal(qty=150, notional=15000.0), _state())
    assert not d.approved
    assert d.reason == "position_size_exceeds_cap"


def test_blocks_oversized_risk():
    # risk_per_share=2, qty=600 -> $1200 risk on $100k equity = 1.2% > 1% cap
    d = check(_proposal(qty=600, notional=60000.0), _state())
    assert not d.approved
    # Either risk cap or position size cap may fire first; both are "block".
    assert d.reason in {"risk_per_trade_exceeds_cap", "position_size_exceeds_cap"}


def test_pdt_blocks_small_account_at_limit():
    d = check(
        _proposal(),
        _state(equity=10_000.0, day_trade_count_5d=3),
    )
    assert not d.approved
    assert d.reason == "pdt_limit_reached"


def test_pdt_does_not_block_large_account():
    d = check(
        _proposal(),
        _state(equity=50_000.0, day_trade_count_5d=10),
    )
    assert d.approved


def test_compute_bracket_uses_atr_when_larger():
    stop, target = compute_bracket(entry=100.0, atr_value=2.0)
    # 1.5 * 2.0 = 3.0 > 0.5%*100 = 0.5
    assert stop == pytest.approx(97.0)
    assert target == pytest.approx(106.0)


def test_compute_bracket_uses_min_pct_when_atr_tiny():
    stop, target = compute_bracket(entry=100.0, atr_value=0.1)
    # min: 0.5%*100 = 0.5
    assert stop == pytest.approx(99.5)
    assert target == pytest.approx(101.0)
