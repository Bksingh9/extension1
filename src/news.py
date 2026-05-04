"""News sentiment scoring.

Cheap, optional, and degrades gracefully:
- If yfinance is available, fetch recent headlines per symbol.
- If ANTHROPIC_API_KEY is set, ask Claude for a -10..+10 score.
- Otherwise, return neutral 0 and skip news-based entries.

We deliberately keep this minimal — sentiment is a *filter* on top of a
technical confirmation, not a signal source.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from .logging_setup import get_logger
from .settings import settings

log = get_logger()


@dataclass
class NewsAssessment:
    symbol: str
    sentiment: float            # -10..+10
    has_earnings_within_2d: bool
    headlines: list[str]


def _fetch_headlines(symbol: str, max_items: int = 10) -> list[str]:
    try:
        import yfinance as yf
        t = yf.Ticker(symbol)
        items = (t.news or [])[:max_items]
        out: list[str] = []
        for it in items:
            title = it.get("title") or it.get("content", {}).get("title")
            if title:
                out.append(str(title))
        return out
    except Exception as e:
        log.debug(f"news fetch failed for {symbol}: {e}")
        return []


def _has_earnings_soon(symbol: str, days: int = 2) -> bool:
    try:
        import yfinance as yf
        t = yf.Ticker(symbol)
        cal = getattr(t, "calendar", None)
        if cal is None:
            return False
        if isinstance(cal, dict):
            dates = cal.get("Earnings Date") or []
        else:
            dates = []
            try:
                dates = list(cal.loc["Earnings Date"].values)
            except Exception:
                dates = []
        now = datetime.now(timezone.utc)
        for d in dates:
            if d is None:
                continue
            try:
                dt = d if isinstance(d, datetime) else datetime.fromisoformat(str(d))
            except Exception:
                continue
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if 0 <= (dt - now).days <= days:
                return True
    except Exception as e:
        log.debug(f"earnings check failed for {symbol}: {e}")
    return False


def _score_with_claude(symbol: str, headlines: list[str]) -> Optional[float]:
    if not settings.anthropic_api_key or not headlines:
        return None
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=settings.anthropic_api_key)
        prompt = (
            f"You are a financial news sentiment scorer for {symbol}. "
            "Read the headlines and respond with a single integer from -10 (very bearish) "
            "to +10 (very bullish). Output ONLY the integer, nothing else.\n\n"
            "Headlines:\n- " + "\n- ".join(headlines)
        )
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=8,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
        return float(int(text))
    except Exception as e:
        log.warning(f"claude sentiment failed for {symbol}: {e}")
        return None


def assess(symbol: str) -> NewsAssessment:
    headlines = _fetch_headlines(symbol)
    earnings_soon = _has_earnings_soon(symbol)
    score = _score_with_claude(symbol, headlines) if headlines else None
    return NewsAssessment(
        symbol=symbol,
        sentiment=float(score) if score is not None else 0.0,
        has_earnings_within_2d=earnings_soon,
        headlines=headlines,
    )
