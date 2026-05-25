import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import kite_broker  # noqa: E402
from src.broker import Account, MissingCredentialsError, Position  # noqa: E402
from src.settings import load_india_config  # noqa: E402


def test_india_config_shape():
    cfg = load_india_config()
    assert cfg["exchange"] == "NSE"
    assert cfg["currency"] == "INR"
    assert len(cfg["watchlist"]) >= 15
    assert cfg["risk"]["max_open_positions"] == 4
    assert cfg["yfinance_suffix"] == ".NS"


def test_kite_broker_requires_credentials(monkeypatch):
    monkeypatch.setattr(kite_broker.settings, "kite_api_key", "")
    monkeypatch.setattr(kite_broker.settings, "kite_access_token", "")
    with pytest.raises(MissingCredentialsError):
        kite_broker.KiteBroker()


def test_get_india_broker_dry_run_returns_dryrun(monkeypatch):
    monkeypatch.setattr(kite_broker.settings, "trading_mode", "dry_run")
    # is_dry is a property off trading_mode; patch the property's source.
    monkeypatch.setattr(type(kite_broker.settings), "is_dry", property(lambda self: True))
    b = kite_broker.get_india_broker()
    assert b.__class__.__name__ == "DryRunBroker"


def test_kite_account_parsing(monkeypatch):
    monkeypatch.setattr(kite_broker.settings, "kite_api_key", "k")
    monkeypatch.setattr(kite_broker.settings, "kite_access_token", "t")

    fake_kite = MagicMock()
    fake_kite.margins.return_value = {"equity": {"net": 1000000.0, "available": {"cash": 950000.0}}}
    fake_module = MagicMock()
    fake_module.KiteConnect.return_value = fake_kite
    monkeypatch.setitem(sys.modules, "kiteconnect", fake_module)

    broker = kite_broker.KiteBroker()
    acct = broker.account()
    assert isinstance(acct, Account)
    assert acct.equity == 1_000_000.0
    assert acct.cash == 950_000.0
    assert acct.trading_blocked is False


def test_kite_positions_parsing(monkeypatch):
    monkeypatch.setattr(kite_broker.settings, "kite_api_key", "k")
    monkeypatch.setattr(kite_broker.settings, "kite_access_token", "t")

    fake_kite = MagicMock()
    fake_kite.positions.return_value = {
        "net": [
            {"tradingsymbol": "RELIANCE", "quantity": 10, "average_price": 2900.0, "value": 29000.0, "unrealised": 150.0},
            {"tradingsymbol": "TCS", "quantity": 0, "average_price": 0.0},  # flat, skipped
        ]
    }
    fake_module = MagicMock()
    fake_module.KiteConnect.return_value = fake_kite
    monkeypatch.setitem(sys.modules, "kiteconnect", fake_module)

    broker = kite_broker.KiteBroker()
    pos = broker.positions()
    assert len(pos) == 1
    assert isinstance(pos[0], Position)
    assert pos[0].symbol == "RELIANCE"
    assert pos[0].qty == 10


def test_kite_submit_bracket_dry_run(monkeypatch):
    monkeypatch.setattr(kite_broker.settings, "kite_api_key", "k")
    monkeypatch.setattr(kite_broker.settings, "kite_access_token", "t")
    monkeypatch.setattr(kite_broker.settings, "trading_mode", "paper")

    fake_kite = MagicMock()
    fake_module = MagicMock()
    fake_module.KiteConnect.return_value = fake_kite
    monkeypatch.setitem(sys.modules, "kiteconnect", fake_module)

    broker = kite_broker.KiteBroker()
    ack = broker.submit_bracket(symbol="RELIANCE", qty=10, entry=2900.0, stop=2784.0, target=3132.0)
    assert ack["status"] == "dry_run"
    # paper mode must NOT call the real place_order
    fake_kite.place_order.assert_not_called()
