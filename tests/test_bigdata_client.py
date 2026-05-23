from unittest.mock import MagicMock

from src import bigdata_client


def test_no_credentials_returns_none(monkeypatch):
    monkeypatch.setattr(bigdata_client.settings, "bigdata_username", "")
    monkeypatch.setattr(bigdata_client.settings, "bigdata_password", "")
    assert bigdata_client.latest_earnings_transcript("NVDA") is None


def test_get_client_none_without_creds(monkeypatch):
    monkeypatch.setattr(bigdata_client.settings, "bigdata_username", "")
    monkeypatch.setattr(bigdata_client.settings, "bigdata_password", "")
    assert bigdata_client._get_client() is None


def test_latest_transcript_returns_excerpt(monkeypatch):
    monkeypatch.setattr(bigdata_client.settings, "bigdata_username", "u")
    monkeypatch.setattr(bigdata_client.settings, "bigdata_password", "p")

    # Bypass the real SDK: stub the client + the isolated SDK interaction.
    fake_client = MagicMock()
    monkeypatch.setattr(bigdata_client, "_get_client", lambda: fake_client)

    excerpt = bigdata_client.TranscriptExcerpt(
        symbol="NVDA",
        headline="NVIDIA Q1 2027 Earnings Call",
        timestamp="2026-05-20T21:00:00",
        text="Total revenue of $82 billion, up 85% year-over-year.",
    )
    monkeypatch.setattr(bigdata_client, "_search_latest_transcript", lambda c, s: excerpt)

    out = bigdata_client.latest_earnings_transcript("NVDA")
    assert out is not None
    assert out.symbol == "NVDA"
    assert "82 billion" in out.text


def test_search_failure_degrades_to_none(monkeypatch):
    monkeypatch.setattr(bigdata_client.settings, "bigdata_username", "u")
    monkeypatch.setattr(bigdata_client.settings, "bigdata_password", "p")
    fake_client = MagicMock()
    monkeypatch.setattr(bigdata_client, "_get_client", lambda: fake_client)
    monkeypatch.setattr(bigdata_client, "_search_latest_transcript", lambda c, s: None)
    assert bigdata_client.latest_earnings_transcript("NVDA") is None


def test_news_transcript_lines_empty_without_creds(monkeypatch):
    from src import news
    monkeypatch.setattr(news.settings, "bigdata_username", "")
    monkeypatch.setattr(news.settings, "bigdata_password", "")
    assert news._transcript_lines("NVDA") == []
