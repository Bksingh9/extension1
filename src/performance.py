"""Portfolio performance helpers built on empyrical-reloaded + quantstats.

- `equity_curve_from_audit()` reconstructs a daily equity series from the
  `eod_snapshot` events in `logs/audit.sqlite`.
- `compute_metrics(returns)` returns a dict of institutional metrics
  (CAGR, Sharpe, Sortino, max-DD, Calmar, hit rate, best/worst day).
- `write_tearsheet(returns, out_path, benchmark)` renders an HTML
  quantstats tear-sheet next to the markdown weekly review.

Cold-start safe: if there is no equity history (or fewer than ~5 daily
points), all helpers return empty / `None` instead of raising.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional

import pandas as pd

from .audit import DB_PATH
from .logging_setup import get_logger

log = get_logger()

MIN_POINTS = 5


def equity_curve_from_audit() -> pd.Series:
    """Reconstruct a daily equity series from eod_snapshot events."""
    if not DB_PATH.exists():
        return pd.Series(dtype=float)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT ts, payload FROM events WHERE kind = 'eod_snapshot' ORDER BY ts ASC"
        )
        rows = cur.fetchall()
    if not rows:
        return pd.Series(dtype=float)
    points: list[tuple[pd.Timestamp, float]] = []
    for ts, payload in rows:
        try:
            data = json.loads(payload)
            equity = float(data["equity"])
            t = pd.Timestamp(ts)
            points.append((t.normalize(), equity))
        except Exception:
            continue
    if not points:
        return pd.Series(dtype=float)
    # Keep last equity per day.
    df = pd.DataFrame(points, columns=["date", "equity"]).drop_duplicates("date", keep="last")
    return pd.Series(df["equity"].values, index=pd.DatetimeIndex(df["date"]), name="equity").sort_index()


def returns_from_equity(equity: pd.Series) -> pd.Series:
    if equity.empty or len(equity) < 2:
        return pd.Series(dtype=float)
    return equity.pct_change().dropna()


def compute_metrics(returns: pd.Series) -> dict[str, Optional[float]]:
    if returns is None or returns.empty or len(returns) < MIN_POINTS:
        return {k: None for k in [
            "n_days", "cagr", "sharpe", "sortino", "max_drawdown",
            "calmar", "hit_rate", "best_day", "worst_day", "vol_ann",
        ]}
    import empyrical as ep
    return {
        "n_days": int(len(returns)),
        "cagr": float(ep.annual_return(returns)),
        "sharpe": float(ep.sharpe_ratio(returns)),
        "sortino": float(ep.sortino_ratio(returns)),
        "max_drawdown": float(ep.max_drawdown(returns)),
        "calmar": float(ep.calmar_ratio(returns)),
        "hit_rate": float((returns > 0).mean()),
        "best_day": float(returns.max()),
        "worst_day": float(returns.min()),
        "vol_ann": float(ep.annual_volatility(returns)),
    }


def write_tearsheet(
    returns: pd.Series, out_path: Path, benchmark: Optional[pd.Series] = None, title: str = "Strategy"
) -> Optional[Path]:
    """Render an HTML tear-sheet. Returns the path written, or None on failure."""
    if returns is None or returns.empty or len(returns) < MIN_POINTS:
        return None
    try:
        import quantstats as qs
        qs.extend_pandas()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        qs.reports.html(
            returns=returns,
            benchmark=benchmark,
            output=str(out_path),
            title=title,
        )
        return out_path
    except Exception as e:
        log.warning(f"quantstats tearsheet failed: {e}")
        return None


def fetch_spy_returns_aligned(returns: pd.Series) -> Optional[pd.Series]:
    """Fetch SPY daily returns over the same date range, for benchmarking."""
    if returns is None or returns.empty:
        return None
    try:
        import yfinance as yf
        start = returns.index.min() - pd.Timedelta(days=5)
        end = returns.index.max() + pd.Timedelta(days=1)
        df = yf.download("SPY", start=start, end=end, interval="1d", progress=False, auto_adjust=False)
        if df is None or df.empty:
            return None
        close = df["Close"] if "Close" in df.columns else df.iloc[:, 0]
        spy_ret = close.pct_change().dropna()
        spy_ret.index = pd.DatetimeIndex(spy_ret.index).normalize()
        return spy_ret.reindex(returns.index).dropna()
    except Exception as e:
        log.debug(f"SPY benchmark fetch failed: {e}")
        return None
