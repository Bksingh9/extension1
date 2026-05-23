"""Bigdata.com (RavenPack) earnings-transcript retrieval.

Used to enrich the `news_sentiment` strategy around earnings: when a
watchlist name has a recent earnings call, we pull the transcript text and
feed it (alongside news headlines) to the Claude sentiment scorer.

IMPORTANT — SDK surface:
The official client is `bigdata-client` (pip install bigdata-client). Its
exact method names/enums have changed across major versions, so the single
SDK interaction below is isolated in `_search_latest_transcript()` and the
whole module degrades to None on ANY error or missing credentials. Verify
the call against your installed bigdata-client version's docs:
    https://docs.bigdata.com
If your version differs, only `_search_latest_transcript()` needs editing.

All public functions return None / [] on failure; nothing here ever raises
into the trading routines.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .logging_setup import get_logger
from .settings import settings

log = get_logger()

_MAX_CHUNKS = 20


@dataclass
class TranscriptExcerpt:
    symbol: str
    headline: str
    timestamp: str
    text: str  # concatenated top chunks


def _credentials_present() -> bool:
    return bool(settings.bigdata_username and settings.bigdata_password)


def _get_client():
    """Construct the Bigdata client. Returns None if SDK or creds missing."""
    if not _credentials_present():
        return None
    try:
        from bigdata_client import Bigdata
    except ImportError:
        log.debug("bigdata-client not installed; skipping transcript fetch")
        return None
    try:
        return Bigdata(settings.bigdata_username, settings.bigdata_password)
    except Exception as e:
        log.warning(f"bigdata auth failed: {e}")
        return None


def _search_latest_transcript(client, symbol: str) -> Optional[TranscriptExcerpt]:
    """ISOLATED SDK interaction — the only version-sensitive code.

    Strategy: resolve the company, then search transcripts mentioning it,
    newest first, and concatenate the top text chunks.
    """
    try:
        from bigdata_client.query import Entity, Similarity
        from bigdata_client.models.search import DocumentType, SortBy

        companies = client.knowledge_graph.find_companies(symbol)
        if not companies:
            return None
        entity_id = companies[0].id

        results = client.search.new(
            query=Entity(entity_id) & Similarity(f"{symbol} quarterly earnings call results and guidance"),
            scope=DocumentType.TRANSCRIPTS,
            sortby=SortBy.DATE,
        ).run(limit=1)

        if not results:
            return None
        doc = results[0]
        chunks = getattr(doc, "chunks", []) or []
        text = "\n".join(getattr(c, "text", "") for c in chunks[:_MAX_CHUNKS]).strip()
        return TranscriptExcerpt(
            symbol=symbol,
            headline=getattr(doc, "headline", "") or "",
            timestamp=str(getattr(doc, "timestamp", "") or ""),
            text=text,
        )
    except Exception as e:
        log.warning(f"bigdata transcript search failed for {symbol}: {e}")
        return None


def latest_earnings_transcript(symbol: str) -> Optional[TranscriptExcerpt]:
    """Return the most recent earnings-call transcript excerpt, or None."""
    client = _get_client()
    if client is None:
        return None
    return _search_latest_transcript(client, symbol)
