import sys
from unittest.mock import MagicMock

from src import alpha_vantage_client


def _fake_resp(status, json_payload=None):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = json_payload or {}
    return r


def _mock_requests(monkeypatch, response):
    monkeypatch.setattr(alpha_vantage_client, "_throttle", lambda: None)
    fake = MagicMock()
    fake.get.return_value = response
    monkeypatch.setitem(sys.modules, "requests", fake)


def test_returns_none_without_key(monkeypatch):
    monkeypatch.setattr(alpha_vantage_client.settings, "alpha_vantage_api_key", "")
    assert alpha_vantage_client.get_daily_bars("AAPL") is None


def test_returns_none_on_throttle_note(monkeypatch):
    monkeypatch.setattr(alpha_vantage_client.settings, "alpha_vantage_api_key", "fake")
    _mock_requests(monkeypatch, _fake_resp(200, {"Note": "Throttled"}))
    assert alpha_vantage_client.get_daily_bars("AAPL") is None


def test_parses_time_series(monkeypatch):
    monkeypatch.setattr(alpha_vantage_client.settings, "alpha_vantage_api_key", "fake")
    payload = {
        "Time Series (Daily)": {
            "2026-05-19": {
                "1. open": "175.0", "2. high": "176.5", "3. low": "174.5",
                "4. close": "176.0", "5. volume": "50000000",
            },
            "2026-05-20": {
                "1. open": "176.0", "2. high": "178.0", "3. low": "175.5",
                "4. close": "177.5", "5. volume": "52000000",
            },
        }
    }
    _mock_requests(monkeypatch, _fake_resp(200, payload))
    df = alpha_vantage_client.get_daily_bars("AAPL", days=10)
    assert df is not None
    assert len(df) == 2
    assert set(df.columns) == {"open", "high", "low", "close", "volume"}
    assert df["close"].iloc[-1] == 177.5


def test_returns_none_on_http_error(monkeypatch):
    monkeypatch.setattr(alpha_vantage_client.settings, "alpha_vantage_api_key", "fake")
    _mock_requests(monkeypatch, _fake_resp(500))
    assert alpha_vantage_client.get_daily_bars("AAPL") is None
