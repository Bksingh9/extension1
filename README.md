# extension1 — autonomous trading bot

Paper-first US-equities swing-trading bot. Five strategies, ATR brackets,
fractional Kelly sizing, deterministic risk gate, audit trail.

> **Live trading is disabled by default and requires three independent gates
> to enable.** See [§Going live](#going-live).

## What this does

- Runs five entry strategies (`momentum`, `mean_reversion`, `breakout`,
  `vwap_intraday`, `news_sentiment`) on a watchlist of large-cap US equities.
- Sizes every entry with fractional Kelly (1/4 Kelly, capped at 10% equity,
  capped again by 1% per-trade risk).
- Submits bracket orders only — every position has a stop AND a target,
  computed from ATR.
- Five routines mirror a standard trading day:

  | Routine | When (ET) | Purpose |
  |---|---|---|
  | `routine_01_premarket` | 08:00 | Score watchlist, write `memory/market-context.md` |
  | `routine_02_open`      | 09:35 | Re-confirm and submit brackets |
  | `routine_03_midday`    | 12:30 | Reconcile, ratchet trails, check circuit breaker |
  | `routine_04_eod`       | 16:15 | Equity snapshot, daily P&L vs SPY |
  | `routine_05_friday`    | 16:30 | Weekly review and weight suggestions |

- Audit trail lives in `logs/audit.sqlite` and `logs/audit.log`.
- Markdown "brain" lives in `memory/` (strategy, positions, journal, weekly).

## Project layout

```
config/config.json         risk params, watchlist, strategy weights
memory/                    strategy.md, positions.md, journal.md, etc.
src/                       settings, indicators, strategies, risk_manager,
                           position_sizer, broker, audit, news, notify, journal
routines/                  routine_01..05
scripts/                   check_alpaca, sync_portfolio, backtest
tests/                     pytest suite
.github/workflows/         trading-routines.yml.disabled (opt-in scheduler)
```

## Trading modes

Set `TRADING_MODE` in `.env`:

- `dry_run` — no broker calls. Routines run end-to-end on yfinance bars and
  write to `memory/` and `logs/`. **Default.**
- `paper`   — real Alpaca paper-trading endpoint. Requires keys.
- `live`    — real money. Requires three gates (see below).

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in keys in .env. NEVER commit .env.
```

Connectivity check:

```bash
python3 scripts/check_alpaca.py
```

Offline smoke test (no keys needed):

```bash
TRADING_MODE=dry_run python3 routines/routine_01_premarket.py \
  && TRADING_MODE=dry_run python3 routines/routine_02_open.py \
  && TRADING_MODE=dry_run python3 routines/routine_03_midday.py \
  && TRADING_MODE=dry_run python3 routines/routine_04_eod.py
```

Backtest:

```bash
python3 scripts/backtest.py --days 1000
python3 scripts/backtest.py --days 500 --strategy momentum
```

## Tests

```bash
pytest -q
```

Tests cover: indicators, strategies (firing logic), risk manager (every
block reason), position sizer (Kelly + caps), audit DB.

## Risk model — what's enforced in code

Every order passes through `src/risk_manager.check()`. Any failure aborts the
order with a single canonical reason logged to the audit DB:

- `account_trading_blocked`
- `outside_trading_window` (09:35–15:55 ET, weekdays)
- `daily_drawdown_circuit_breaker` (≤ -3% intraday)
- `max_open_positions_reached` (≥ 10 open)
- `duplicate_symbol_position`
- `price_out_of_range` ($5–$1000)
- `missing_stop` / `missing_target` / `invalid_bracket`
- `stop_too_tight` (< 0.5% of entry)
- `r_r_below_2.0`
- `risk_per_trade_exceeds_cap` (> 1% equity)
- `position_size_exceeds_cap` (> 10% equity)
- `pdt_limit_reached` (accounts < $25k, > 3 day-trades / 5d)

## Going live

Three independent gates, ALL required:

1. `TRADING_MODE=live` in `.env`.
2. `ALLOW_LIVE=true` in `.env`.
3. A file `memory/go-live.md` exists and contains `GO LIVE CONFIRMED` on a line.

Live keys must be a **separate** Alpaca live key/secret pair, not the paper
keys. Operators should keep `MAX_POSITION_PCT=0.02` for the first 5 live
trading days, then return to 0.10. (Do this by editing
`config/config.json`.)

## Cloud scheduling

`.github/workflows/trading-routines.yml.disabled` contains the full cron-
driven workflow. Rename to `.yml` to enable. Note: GitHub Actions cron is
UTC; the included offsets are EDT (Mar–Nov). For EST add 1h to each.

## Notes / not-yet

- **Indian market**: out of scope for this codebase. NSE/BSE has different
  brokers (Zerodha Kite, Upstox), tax rules, and regulatory regime — should
  live in a separate project, not tacked on here.
- **24/7 trading**: not applicable. US equities trade 09:30–16:00 ET only.
- **News sentiment**: optional. Requires `ANTHROPIC_API_KEY`; falls back to
  neutral 0 otherwise. Always combined with a technical confirmation —
  never used alone.
- The earlier `PLAYBOOK.md` (4-strategy, fixed -4%/+8%) is superseded by
  `memory/strategy.md`. Kept in repo for historical context.
