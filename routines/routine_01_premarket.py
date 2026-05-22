"""Routine 1 — Pre-market research (08:00 ET).

- Read positions and active strategy.
- Pull recent daily bars for each watchlist symbol.
- Run all four technical strategies on each.
- (Optional) score sentiment and flag earnings within 2 days.
- Rank candidates and write top-5 thesis to memory/market-context.md.

Runs safely in dry_run mode using yfinance for bars.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd  # noqa: E402

from src.allocation import decide as decide_allocation  # noqa: E402
from src.audit import record_event  # noqa: E402
from src.broker import get_broker  # noqa: E402
from src.journal import today_str, write_market_context  # noqa: E402
from src.logging_setup import get_logger  # noqa: E402
from src.macro import snapshot as macro_snapshot, snapshot_markdown  # noqa: E402
from src.regime import assess_with_default  # noqa: E402
from src.settings import config, settings  # noqa: E402
from src.strategies import Signal, best_signal, news_sentiment_signal  # noqa: E402

log = get_logger()


def _bars_yf(symbol: str, days: int = 200) -> Optional[pd.DataFrame]:
    try:
        import yfinance as yf
        df = yf.download(symbol, period=f"{max(days, 200)}d", interval="1d", progress=False, auto_adjust=False)
        if df is None or df.empty:
            return None
        df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
        return df.tail(days)
    except Exception as e:
        log.debug(f"yfinance fetch failed for {symbol}: {e}")
        return None


def _bars(symbol: str, days: int = 200) -> Optional[pd.DataFrame]:
    if settings.is_dry:
        return _bars_yf(symbol, days)
    try:
        broker = get_broker()
        df = broker.get_bars(symbol, days=days, timeframe="1Day")
        if df is None or df.empty:
            return _bars_yf(symbol, days)
        return df
    except Exception as e:
        log.warning(f"broker bars failed for {symbol}, falling back to yfinance: {e}")
        return _bars_yf(symbol, days)


def main() -> int:
    weights = config["strategy_weights"]
    use_news = bool(settings.anthropic_api_key)

    # Regime assessment on the primary symbol (default SPY).
    primary = config["regime"]["primary_symbol"]
    primary_bars = _bars(primary, days=config["regime"]["lookback_days"])
    regime = assess_with_default(primary_bars) if primary_bars is not None and not primary_bars.empty else None
    if regime is not None:
        alloc = decide_allocation(regime.label, regime.confidence)
        record_event(
            "regime_assessment",
            {
                "label": regime.label,
                "confidence": regime.confidence,
                "effective_label": alloc.effective_label,
                "target_exposure_pct": alloc.target_exposure_pct,
                "reason": alloc.reason,
            },
        )
        log.info(
            f"[premarket] regime={regime.label} conf={regime.confidence:.2f} "
            f"-> effective={alloc.effective_label} cap={alloc.target_exposure_pct*100:.0f}%"
        )
    else:
        alloc = decide_allocation("NEUTRAL", 0.0)
        log.info("[premarket] no regime data, defaulting to NEUTRAL")

    candidates: list[Signal] = []
    skipped = 0
    for symbol in config["watchlist"]:
        bars = _bars(symbol, days=200)
        if bars is None or bars.empty:
            skipped += 1
            continue
        sig = best_signal(symbol, bars, weights)

        if use_news:
            from src.news import assess  # lazy import
            news = assess(symbol)
            if news.has_earnings_within_2d:
                record_event("earnings_within_2d_skip", {"symbol": symbol}, symbol=symbol)
                continue
            news_sig = news_sentiment_signal(
                symbol=symbol,
                bars=bars,
                sentiment_score=news.sentiment,
                has_earnings_within_2d=news.has_earnings_within_2d,
                min_score=config["news_sentiment"]["min_score_to_trade"],
            )
            if news_sig is not None and (sig is None or news_sig.score > sig.score):
                sig = news_sig

        if sig is not None:
            candidates.append(sig)
            record_event(
                "premarket_signal",
                {
                    "symbol": symbol,
                    "strategy": sig.strategy,
                    "score": sig.score,
                    "entry": sig.entry,
                    "atr": sig.atr,
                    "notes": sig.notes,
                },
                symbol=symbol,
                strategy=sig.strategy,
            )

    candidates.sort(key=lambda s: s.score, reverse=True)
    top5 = candidates[:5]

    regime_line = (
        f"_Regime: **{alloc.effective_label}** (raw={regime.label if regime else 'NEUTRAL'}, "
        f"conf={(regime.confidence if regime else 0.0):.2f}, "
        f"cap={alloc.target_exposure_pct*100:.0f}%)_"
    )

    # Macro snapshot from FRED (free, public-apis).
    macro = macro_snapshot()
    if macro.vix is not None:
        record_event("macro_snapshot", {
            "vix": macro.vix, "ten_year_yield": macro.ten_year_yield,
            "fed_funds": macro.fed_funds, "unemployment": macro.unemployment,
        })

    lines = [
        f"_Generated: {datetime.now().isoformat(timespec='seconds')}_",
        regime_line,
        f"_Universe: {len(config['watchlist'])} symbols, {skipped} no-data, {len(candidates)} candidates_",
        "",
        "## Macro (FRED)",
        "",
        snapshot_markdown(macro),
        "",
        "## Top 5 candidates",
        "",
        "| Rank | Symbol | Strategy | Entry | ATR | Score | Notes |",
        "|------|--------|----------|-------|-----|-------|-------|",
    ]
    if not top5:
        lines.append("| — | _(no candidates today)_ | | | | | |")
    else:
        for i, s in enumerate(top5, 1):
            lines.append(
                f"| {i} | {s.symbol} | {s.strategy} | {s.entry:.2f} | {s.atr:.2f} | {s.score:.2f} | {s.notes} |"
            )
    write_market_context(today_str(), "\n".join(lines))
    log.info(f"[premarket] wrote market-context.md with {len(top5)} candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
