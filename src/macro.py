"""Macro context via FRED (Federal Reserve Economic Data).

FRED is a free public API from the St. Louis Fed. Most series are
accessible without a key via the public CSV download, but the JSON API
requires `FRED_API_KEY`. We try CSV (no key) first, fall back to JSON
(with key) if needed.

Series we care about for trading context:
  - VIXCLS  : CBOE Volatility Index (daily close)
  - DGS10   : 10-Year Treasury Constant Maturity Rate
  - DFF     : Effective Federal Funds Rate
  - UNRATE  : Unemployment Rate (monthly)

All functions degrade gracefully and return None on failure.
"""
from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import Optional

from .logging_setup import get_logger
from .settings import settings

log = get_logger()

CSV_BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv"
JSON_BASE = "https://api.stlouisfed.org/fred/series/observations"
TIMEOUT = 6

CARE_SERIES = ["VIXCLS", "DGS10", "DFF", "UNRATE"]


@dataclass
class MacroSnapshot:
    vix: Optional[float]
    ten_year_yield: Optional[float]
    fed_funds: Optional[float]
    unemployment: Optional[float]


def _latest_csv(series_id: str) -> Optional[float]:
    try:
        import pandas as pd
        import requests
    except ImportError:
        return None
    try:
        r = requests.get(CSV_BASE, params={"id": series_id}, timeout=TIMEOUT)
        if r.status_code >= 400:
            return None
        df = pd.read_csv(StringIO(r.text))
        if df.empty:
            return None
        # FRED CSVs use "." for missing values; drop them and take the most recent number.
        val_col = df.columns[-1]
        df = df[df[val_col].astype(str).str.strip() != "."]
        if df.empty:
            return None
        return float(df[val_col].iloc[-1])
    except Exception as e:
        log.debug(f"fred csv {series_id} failed: {e}")
        return None


def _latest_json(series_id: str) -> Optional[float]:
    if not settings.fred_api_key:
        return None
    try:
        import requests
    except ImportError:
        return None
    try:
        r = requests.get(
            JSON_BASE,
            params={
                "series_id": series_id,
                "api_key": settings.fred_api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 5,
            },
            timeout=TIMEOUT,
        )
        if r.status_code >= 400:
            return None
        obs = (r.json() or {}).get("observations", [])
        for o in obs:
            v = o.get("value")
            if v and v != ".":
                return float(v)
    except Exception as e:
        log.debug(f"fred json {series_id} failed: {e}")
    return None


def latest(series_id: str) -> Optional[float]:
    v = _latest_csv(series_id)
    if v is not None:
        return v
    return _latest_json(series_id)


def snapshot() -> MacroSnapshot:
    return MacroSnapshot(
        vix=latest("VIXCLS"),
        ten_year_yield=latest("DGS10"),
        fed_funds=latest("DFF"),
        unemployment=latest("UNRATE"),
    )


def snapshot_markdown(snap: Optional[MacroSnapshot] = None) -> str:
    snap = snap or snapshot()
    rows = [
        ("VIX (CBOE volatility)", snap.vix, "{:.2f}"),
        ("10Y Treasury yield (%)", snap.ten_year_yield, "{:.2f}"),
        ("Fed funds rate (%)", snap.fed_funds, "{:.2f}"),
        ("Unemployment (%)", snap.unemployment, "{:.1f}"),
    ]
    lines = ["| Indicator | Latest |", "|---|---|"]
    any_data = False
    for label, value, fmt in rows:
        if value is None:
            lines.append(f"| {label} | _n/a_ |")
        else:
            any_data = True
            lines.append(f"| {label} | {fmt.format(value)} |")
    if not any_data:
        return "_FRED not reachable; macro snapshot unavailable._"
    return "\n".join(lines)
