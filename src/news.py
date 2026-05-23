"""News sentiment scoring.

Cheap, optional, and degrades gracefully. Headline + earnings provider
chain (first hit wins):
  1. Finnhub (if FINNHUB_API_KEY set) — free 60 req/min, public-apis registry
  2. yfinance — flaky but no key
  3. None → neutral 0, skip news-based entry

Sentiment scoring (-10..+10) uses Claude if `ANTHROPIC_API_KEY` is set;
otherwise returns neutral 0.

We deliberately keep this minimal — sentiment is a *filter* on top of a
technical confirmation, not a signal source.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

from . import finnhub_client
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
    # Prefer Finnhub if a key is configured.
    if settings.finnhub_api_key:
        hs = finnhub_client.company_news(symbol, days_back=3, max_items=max_items)
        if hs:
            return hs
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
    if settings.finnhub_api_key:
        try:
            return finnhub_client.has_earnings_within(symbol, days=days)
        except Exception as e:
            log.debug(f"finnhub earnings check failed for {symbol}: {e}")
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


def _transcript_lines(symbol: str) -> list[str]:
    """Pull the latest earnings-call transcript excerpt (Bigdata.com) as
    extra context for the Claude scorer. Empty list if unavailable."""
    if not (settings.bigdata_username and settings.bigdata_password):
        return []
    from . import bigdata_client
    excerpt = bigdata_client.latest_earnings_transcript(symbol)
    if excerpt is None or not excerpt.text:
        return []
    # Cap length so we don't blow up the prompt; first ~2000 chars is enough signal.
    snippet = excerpt.text[:2000]
    return [f"[Earnings transcript {excerpt.timestamp}] {snippet}"]


def assess(symbol: str) -> NewsAssessment:
    headlines = _fetch_headlines(symbol)
    earnings_soon = _has_earnings_soon(symbol)

    scoring_inputs = list(headlines) + _transcript_lines(symbol)
    claude_score = _score_with_claude(symbol, scoring_inputs) if scoring_inputs else None

    # Blend with Stocktwits retail sentiment when available — free, no key.
    from . import stocktwits_client
    twits_score = stocktwits_client.sentiment_score(symbol)

    if claude_score is not None and twits_score is not None:
        # Weighted 60% Claude (news quality) / 40% retail (Stocktwits).
        blended = 0.6 * claude_score + 0.4 * twits_score
    elif claude_score is not None:
        blended = claude_score
    elif twits_score is not None:
        blended = twits_score
    else:
        blended = 0.0

    return NewsAssessment(
        symbol=symbol,
        sentiment=float(blended),
        has_earnings_within_2d=earnings_soon,
        headlines=headlines,
    )
