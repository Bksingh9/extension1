import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import ccxt_broker
from src.broker import Account, MissingCredentialsError
from src.markets import get_profile
from src.risk_manager import OrderProposal, PortfolioState, _trading_window, check, compute_bracket

UTC = ZoneInfo("UTC")
IST = ZoneInfo("Asia/Kolkata")


# ---------- risk windows ----------

def test_crypto_window_is_always_open():
    rc = get_profile("crypto").risk
    open_t, cutoff = _trading_window("crypto", rc)
    assert open_t.hour == 0 and cutoff.hour == 23


def test_forex_window_is_ist_currency_hours():
    rc = get_profile("forex").risk
    open_t, cutoff = _trading_window("india_fx", rc)
    assert (open_t.hour, open_t.minute) == (9, 0)
    assert (cutoff.hour, cutoff.minute) == (16, 55)  # 17:00 - 5 min


def test_crypto_trade_approved_at_3am():
    rc = get_profile("crypto").risk
    entry = 60000.0
    stop, target = compute_bracket(entry, entry * 0.03, min_stop_pct=rc["min_atr_stop_pct"])
    state = PortfolioState(equity=100_000, cash=100_000, open_positions={}, open_position_count=0,
                           day_pnl_pct=0.0, day_trade_count_5d=0, trading_blocked=False,
                           now_et=datetime(2026, 5, 25, 3, 0, tzinfo=UTC))  # 3am — crypto is open
    qty = 0.01
    prop = OrderProposal("BTC", "breakout", "buy", entry, stop, target, qty, qty * entry)
    d = check(prop, state, risk_cfg=rc, market="crypto")
    assert d.approved, d.reason


# ---------- ccxt broker ----------

def test_ccxt_requires_credentials(monkeypatch):
    monkeypatch.setattr(ccxt_broker.settings, "ccxt_api_key", "")
    monkeypatch.setattr(ccxt_broker.settings, "ccxt_secret", "")
    with pytest.raises(MissingCredentialsError):
        ccxt_broker.CcxtBroker()


def test_ccxt_account_parsing(monkeypatch):
    monkeypatch.setattr(ccxt_broker.settings, "ccxt_api_key", "k")
    monkeypatch.setattr(ccxt_broker.settings, "ccxt_secret", "s")
    monkeypatch.setattr(ccxt_broker.settings, "ccxt_exchange", "binance")

    fake_ex = MagicMock()
    fake_ex.fetch_balance.return_value = {"total": {"USDT": 5000.0, "BTC": 0.1}}
    fake_ccxt = MagicMock()
    fake_ccxt.binance.return_value = fake_ex
    monkeypatch.setitem(sys.modules, "ccxt", fake_ccxt)

    b = ccxt_broker.CcxtBroker()
    acct = b.account()
    assert isinstance(acct, Account)
    assert acct.equity == 5000.0
    pos = b.positions()
    assert any(p.symbol == "BTC" for p in pos)


def test_ccxt_dry_run_bracket_no_live_call(monkeypatch):
    monkeypatch.setattr(ccxt_broker.settings, "ccxt_api_key", "k")
    monkeypatch.setattr(ccxt_broker.settings, "ccxt_secret", "s")
    monkeypatch.setattr(ccxt_broker.settings, "trading_mode", "paper")
    fake_ex = MagicMock()
    fake_ccxt = MagicMock()
    fake_ccxt.binance.return_value = fake_ex
    monkeypatch.setitem(sys.modules, "ccxt", fake_ccxt)

    b = ccxt_broker.CcxtBroker()
    ack = b.submit_bracket(symbol="BTC/USDT", qty=0.1, entry=60000, stop=58000, target=64000)
    assert ack["status"] == "dry_run"
    fake_ex.create_order.assert_not_called()


def test_forex_profile_symbols():
    p = get_profile("forex")
    assert p.name == "india_fx"
    assert p.yf_symbol("USDINR") == "USDINR=X"
    assert p.currency == "INR"
