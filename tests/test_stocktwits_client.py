import sys
from unittest.mock import MagicMock

import pytest

from src import stocktwits_client


def _fake_resp(status, json_payload=None):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = json_payload or {}
    return r


def _mock_requests(monkeypatch, response):
    monkeypatch.setattr(stocktwits_client, "_throttle", lambda: None)
    fake = MagicMock()
    fake.get.return_value = response
    monkeypatch.setitem(sys.modules, "requests", fake)


def test_returns_none_on_http_error(monkeypatch):
    _mock_requests(monkeypatch, _fake_resp(500))
    assert stocktwits_client.sentiment_score("AAPL") is None


def test_returns_none_when_too_few_messages(monkeypatch):
    payload = {
        "messages": [
            {"entities": {"sentiment": {"basic": "Bullish"}}},
            {"entities": {"sentiment": {"basic": "Bearish"}}},
        ]
    }
    _mock_requests(monkeypatch, _fake_resp(200, payload))
    assert stocktwits_client.sentiment_score("AAPL", min_messages=5) is None


def test_positive_score_when_mostly_bullish(monkeypatch):
    payload = {
        "messages": (
            [{"entities": {"sentiment": {"basic": "Bullish"}}}] * 8
            + [{"entities": {"sentiment": {"basic": "Bearish"}}}] * 2
        )
    }
    _mock_requests(monkeypatch, _fake_resp(200, payload))
    score = stocktwits_client.sentiment_score("AAPL", min_messages=5)
    assert score is not None
    assert score == pytest.approx(6.0)  # (8-2)/10 * 10


def test_negative_score_when_mostly_bearish(monkeypatch):
    payload = {
        "messages": (
            [{"entities": {"sentiment": {"basic": "Bullish"}}}] * 1
            + [{"entities": {"sentiment": {"basic": "Bearish"}}}] * 9
        )
    }
    _mock_requests(monkeypatch, _fake_resp(200, payload))
    score = stocktwits_client.sentiment_score("AAPL", min_messages=5)
    assert score is not None
    assert score == pytest.approx(-8.0)


def test_ignores_messages_without_sentiment(monkeypatch):
    payload = {
        "messages": (
            [{"entities": {"sentiment": {"basic": "Bullish"}}}] * 3
            + [{"entities": {}}] * 20  # no sentiment, should be ignored
        )
    }
    _mock_requests(monkeypatch, _fake_resp(200, payload))
    # only 3 graded msgs, below threshold of 5
    assert stocktwits_client.sentiment_score("AAPL", min_messages=5) is None
