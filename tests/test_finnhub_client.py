from unittest.mock import MagicMock


from src import finnhub_client


def test_company_news_returns_empty_without_key(monkeypatch):
    monkeypatch.setattr(finnhub_client.settings, "finnhub_api_key", "")
    assert finnhub_client.company_news("AAPL") == []


def test_has_earnings_within_returns_false_without_key(monkeypatch):
    monkeypatch.setattr(finnhub_client.settings, "finnhub_api_key", "")
    assert finnhub_client.has_earnings_within("AAPL") is False


def test_company_news_parses_headlines(monkeypatch):
    monkeypatch.setattr(finnhub_client.settings, "finnhub_api_key", "fakekey")
    monkeypatch.setattr(finnhub_client, "_throttle", lambda: None)

    fake_resp = MagicMock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = [
        {"headline": "Apple beats earnings"},
        {"headline": "Analyst upgrades Apple"},
        {"other": "noise"},
    ]
    fake_requests = MagicMock()
    fake_requests.get.return_value = fake_resp
    import sys
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    hs = finnhub_client.company_news("AAPL", days_back=3, max_items=5)
    assert hs == ["Apple beats earnings", "Analyst upgrades Apple"]


def test_has_earnings_within_true_when_calendar_nonempty(monkeypatch):
    monkeypatch.setattr(finnhub_client.settings, "finnhub_api_key", "fakekey")
    monkeypatch.setattr(finnhub_client, "_throttle", lambda: None)

    fake_resp = MagicMock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = {
        "earningsCalendar": [{"symbol": "AAPL", "date": "2026-05-23"}]
    }
    fake_requests = MagicMock()
    fake_requests.get.return_value = fake_resp
    import sys
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    assert finnhub_client.has_earnings_within("AAPL", days=7) is True


def test_has_earnings_within_false_when_calendar_empty(monkeypatch):
    monkeypatch.setattr(finnhub_client.settings, "finnhub_api_key", "fakekey")
    monkeypatch.setattr(finnhub_client, "_throttle", lambda: None)

    fake_resp = MagicMock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = {"earningsCalendar": []}
    fake_requests = MagicMock()
    fake_requests.get.return_value = fake_resp
    import sys
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    assert finnhub_client.has_earnings_within("AAPL", days=7) is False


def test_429_returns_none(monkeypatch):
    monkeypatch.setattr(finnhub_client.settings, "finnhub_api_key", "fakekey")
    monkeypatch.setattr(finnhub_client, "_throttle", lambda: None)

    fake_resp = MagicMock()
    fake_resp.status_code = 429
    fake_resp.text = "rate limited"
    fake_requests = MagicMock()
    fake_requests.get.return_value = fake_resp
    import sys
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    assert finnhub_client.company_news("AAPL") == []
