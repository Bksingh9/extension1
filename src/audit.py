from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any

from .settings import ROOT

DB_PATH = ROOT / "logs" / "audit.sqlite"


def _ensure_db() -> None:
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ts          TEXT NOT NULL,
                kind        TEXT NOT NULL,
                symbol      TEXT,
                strategy    TEXT,
                payload     TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                opened_at       TEXT NOT NULL,
                closed_at       TEXT,
                symbol          TEXT NOT NULL,
                strategy        TEXT NOT NULL,
                side            TEXT NOT NULL,
                qty             REAL NOT NULL,
                entry           REAL NOT NULL,
                stop            REAL NOT NULL,
                target          REAL NOT NULL,
                exit_price      REAL,
                exit_reason     TEXT,
                pnl_usd         REAL,
                pnl_r           REAL
            )
            """
        )


@contextmanager
def _conn():
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def record_event(kind: str, payload: dict[str, Any], symbol: str | None = None, strategy: str | None = None) -> None:
    with _conn() as c:
        c.execute(
            "INSERT INTO events (ts, kind, symbol, strategy, payload) VALUES (?, ?, ?, ?, ?)",
            (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                kind,
                symbol,
                strategy,
                json.dumps(payload, default=str),
            ),
        )


def record_trade_open(*, symbol: str, strategy: str, side: str, qty: float, entry: float, stop: float, target: float) -> int:
    with _conn() as c:
        cur = c.execute(
            """
            INSERT INTO trades (opened_at, symbol, strategy, side, qty, entry, stop, target)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                symbol,
                strategy,
                side,
                qty,
                entry,
                stop,
                target,
            ),
        )
        return int(cur.lastrowid)


def record_trade_close(*, trade_id: int, exit_price: float, exit_reason: str, pnl_usd: float, pnl_r: float) -> None:
    with _conn() as c:
        c.execute(
            """
            UPDATE trades
               SET closed_at = ?, exit_price = ?, exit_reason = ?, pnl_usd = ?, pnl_r = ?
             WHERE id = ?
            """,
            (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                exit_price,
                exit_reason,
                pnl_usd,
                pnl_r,
                trade_id,
            ),
        )


def recent_closed_trades(limit: int = 30) -> list[dict[str, Any]]:
    with _conn() as c:
        cur = c.execute(
            """
            SELECT symbol, strategy, side, qty, entry, stop, target, exit_price, exit_reason, pnl_usd, pnl_r
              FROM trades
             WHERE closed_at IS NOT NULL
             ORDER BY closed_at DESC
             LIMIT ?
            """,
            (limit,),
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
