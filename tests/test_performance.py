import json
import sqlite3
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import pytest

from src import performance


def _build_audit_db(tmp_path, equity_points):
    """Create a minimal audit DB with the given eod_snapshot equity points."""
    db = tmp_path / "audit.sqlite"
    with sqlite3.connect(db) as c:
        c.execute(
            "CREATE TABLE events (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, kind TEXT, symbol TEXT, strategy TEXT, payload TEXT)"
        )
        base = datetime(2026, 1, 5, 16, 15, tzinfo=timezone.utc)
        for i, eq in enumerate(equity_points):
            ts = (base + timedelta(days=i)).isoformat(timespec="seconds")
            c.execute(
                "INSERT INTO events (ts, kind, payload) VALUES (?, ?, ?)",
                (ts, "eod_snapshot", json.dumps({"equity": eq})),
            )
    return db


def test_equity_curve_empty_when_no_db(tmp_path, monkeypatch):
    monkeypatch.setattr(performance, "DB_PATH", tmp_path / "missing.sqlite")
    s = performance.equity_curve_from_audit()
    assert s.empty


def test_equity_curve_reads_eod_snapshots(tmp_path, monkeypatch):
    db = _build_audit_db(tmp_path, [100_000, 100_500, 101_000, 100_750, 101_500])
    monkeypatch.setattr(performance, "DB_PATH", db)
    s = performance.equity_curve_from_audit()
    assert len(s) == 5
    assert s.iloc[0] == 100_000
    assert s.iloc[-1] == 101_500


def test_returns_from_equity_matches_pct_change():
    eq = pd.Series([100, 101, 102.01, 101.0], index=pd.date_range("2026-01-01", periods=4))
    ret = performance.returns_from_equity(eq)
    assert len(ret) == 3
    assert ret.iloc[0] == pytest.approx(0.01)


def test_compute_metrics_returns_nones_when_too_few_points():
    ret = pd.Series([0.001, 0.002])
    m = performance.compute_metrics(ret)
    assert m["cagr"] is None
    assert m["sharpe"] is None


def test_compute_metrics_produces_finite_numbers():
    rng = np.random.default_rng(0)
    rets = pd.Series(
        rng.normal(0.001, 0.01, 252),
        index=pd.date_range("2026-01-01", periods=252, freq="B"),
    )
    m = performance.compute_metrics(rets)
    assert m["n_days"] == 252
    assert m["cagr"] is not None
    assert m["sharpe"] is not None
    assert m["max_drawdown"] is not None
    assert m["max_drawdown"] <= 0
    assert 0.0 <= m["hit_rate"] <= 1.0


def test_write_tearsheet_skips_on_insufficient_data(tmp_path):
    ret = pd.Series([0.001, 0.002])
    out = performance.write_tearsheet(ret, tmp_path / "t.html")
    assert out is None
