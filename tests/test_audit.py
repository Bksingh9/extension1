import os
import tempfile
from pathlib import Path
from unittest.mock import patch


def test_audit_records_event_and_trade(tmp_path, monkeypatch):
    from src import audit
    test_db = tmp_path / "audit.sqlite"
    monkeypatch.setattr(audit, "DB_PATH", test_db)

    audit.record_event("test_event", {"foo": "bar"}, symbol="AAPL", strategy="momentum")
    tid = audit.record_trade_open(
        symbol="AAPL", strategy="momentum", side="buy",
        qty=10, entry=100.0, stop=98.0, target=104.0,
    )
    audit.record_trade_close(
        trade_id=tid, exit_price=104.0, exit_reason="target",
        pnl_usd=40.0, pnl_r=2.0,
    )
    closed = audit.recent_closed_trades(10)
    assert len(closed) == 1
    assert closed[0]["pnl_r"] == 2.0
    assert closed[0]["exit_reason"] == "target"
