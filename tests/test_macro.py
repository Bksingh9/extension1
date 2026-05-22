from unittest.mock import MagicMock

from src import macro


def _fake_response(text="", status=200, json_payload=None):
    r = MagicMock()
    r.status_code = status
    r.text = text
    r.json.return_value = json_payload or {}
    return r


def test_latest_csv_parses_last_numeric_value(monkeypatch):
    csv = "DATE,VIXCLS\n2026-05-19,15.20\n2026-05-20,16.10\n2026-05-21,.\n"
    fake_requests = MagicMock()
    fake_requests.get.return_value = _fake_response(text=csv)
    import sys
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    v = macro._latest_csv("VIXCLS")
    assert v == 16.10


def test_latest_csv_returns_none_when_only_missing(monkeypatch):
    csv = "DATE,VIXCLS\n2026-05-21,.\n"
    fake_requests = MagicMock()
    fake_requests.get.return_value = _fake_response(text=csv)
    import sys
    monkeypatch.setitem(sys.modules, "requests", fake_requests)

    assert macro._latest_csv("VIXCLS") is None


def test_latest_json_requires_key(monkeypatch):
    monkeypatch.setattr(macro.settings, "fred_api_key", "")
    assert macro._latest_json("VIXCLS") is None


def test_snapshot_markdown_handles_all_none():
    snap = macro.MacroSnapshot(vix=None, ten_year_yield=None, fed_funds=None, unemployment=None)
    md = macro.snapshot_markdown(snap)
    assert "unavailable" in md


def test_snapshot_markdown_formats_present_values():
    snap = macro.MacroSnapshot(vix=15.2, ten_year_yield=4.31, fed_funds=5.33, unemployment=3.8)
    md = macro.snapshot_markdown(snap)
    assert "15.20" in md
    assert "4.31" in md
    assert "5.33" in md
    assert "3.8" in md
