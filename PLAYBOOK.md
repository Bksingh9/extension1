# Trading Playbook — `my-aios` Mode B

US equities, swing trades, paper-first. Pure mechanical strategy —
no discretion, no overrides except the kill switches in §6.

---

## 1. Universe & filters

- US equities only (no options, crypto, FX, futures, OTC, ADRs).
- Price between **$5 and $500**.
- Average daily volume > 500k shares.
- No leveraged ETFs (TQQQ/SQQQ/SOXL/etc.), no inverse, no penny stocks.
- Watchlist lives in `memory/watchlist.md` — one ticker per line.

## 2. Entry strategies (any one fires → candidate)

| # | Strategy | Entry condition |
|---|---|---|
| 1 | `mean_reversion` | RSI(14) < 35 **AND** close > SMA(50) |
| 2 | `trend_pullback` | close > SMA(200), SMA(50) > SMA(200), close within 1% of SMA(20), RSI 40–55 |
| 3 | `breakout` | New 20-day high, close > SMA(50), RSI 55–80 |
| 4 | `macd_cross` | MACD line crosses above signal line, close > SMA(200), histogram > 0 |

When multiple strategies fire on the same ticker, the highest-scoring signal wins.

## 3. Exit (universal)

Every position enters as a **bracket order** at submission:
- **Stop loss**: `entry × 0.96` (–4%). Hard. Never widened.
- **Take profit**: `entry × 1.08` (+8%). Triggers `2R` win.
- **Time stop**: 30 trading days.
- **No trailing stop** until +4% unrealized. Optional thereafter.

Risk-reward: **1:2** by construction.

## 4. Position sizing & limits

| Limit | Value |
|---|---|
| Position size | 10% of equity |
| Max concurrent positions | 4 |
| Max new entries per day | 4 |
| Daily drawdown kill switch | −5% of equity |
| Weekly drawdown kill switch | −10% of equity |

## 5. Daily flow (cron, US Eastern)

| Time | Routine | What it does |
|---|---|---|
| 07:00 | `routine_01_premarket` | Scan watchlist with all 4 strategies, rank by score |
| 09:35 | `routine_02_open` | Submit brackets on top 4 candidates |
| 12:30 | `routine_03_midday` | Reconcile open positions, log unrealized P&L |
| 16:15 | `routine_04_eod` | Sweep stops/targets, archive closed trades |
| Fri 17 | `routine_05_friday` | Weekly P&L, win rate, R-multiple, tuning |

## 6. Kill switches (operator-only)

- `HALT` — block new entries, hold open positions.
- `FLATTEN` — close all positions at market, then HALT.
- `RESUME` — undo HALT.
- `GO LIVE CONFIRMED` — paper → live (with `memory/go-live.md`).

Self-halts on: `trading_blocked=True`, daily DD > −5%, GUARDRAILS check fail.

## 7. Pre-trade checklist (code-enforced)

1. `TRADING_MODE` ∈ {`dry_run`, `paper`}, or §8 satisfied for `live`.
2. `account.trading_blocked` is False.
3. Open position count < 4.
4. Price in $5–$500.
5. 10% of equity affords ≥ 1 share.
6. Bracket has stop AND target attached.
7. Intent line written **before** the API call.
8. Pre-trade Slack/Discord ping sent.

## 8. Path from paper to live

Four conditions must hold:
1. **20 consecutive paper trading days completed**.
2. **Cumulative paper P&L positive**.
3. **Routine 5** shows positive expectancy in R.
4. **Operator action**: type `GO LIVE CONFIRMED`, create `memory/go-live.md` with that phrase, generate a **separate** live key/secret, update `.env` with `TRADING_MODE=live` and the live base URL.

For the **first 5 live trading days**, set `MAX_POSITION_PCT=0.02`. Then back to 0.10.

## 9. Strategy admission

New strategies admitted only when:
1. Pure function `Signal | None` in `skills/strategies.py`.
2. Backtested with `scripts/backtest.py --strategy <name> --days 1000` on real Alpaca bars.
3. **Trades ≥ 30** AND **expectancy > 0R**.
4. Operator approves by name.
5. Listed in `CLAUDE.md` and `GUARDRAILS.md` §3.

Stop / target / sizing are NEVER strategy-specific.

## 10. Daily commands

```bash
python3 scripts/check_alpaca.py              # validate keys + connectivity
python3 scripts/sync_portfolio.py            # pull broker state
python3 scripts/backtest.py --days 1000      # rank strategies on real bars
python3 routines/routine_01_premarket.py     # manual run
```

Offline smoke test:
```bash
TRADING_MODE=dry_run python3 routines/routine_01_premarket.py \
  && TRADING_MODE=dry_run python3 routines/routine_02_open.py \
  && TRADING_MODE=dry_run python3 routines/routine_03_midday.py \
  && TRADING_MODE=dry_run python3 routines/routine_04_eod.py
```

## 11. Reading the daily reports

| File | What it tells you |
|---|---|
| `memory/premarket-YYYYMMDD.md` | 07:00 ranked candidates |
| `memory/eod-YYYYMMDD.md` | What happened today |
| `memory/weekly-YYYYMMDD.md` | Friday review |
| `memory/backtest-YYYYMMDD.md` | Strategy comparison |
| `memory/trade-history.md` | Permanent ledger |
| `memory/portfolio.md` | Current state |
| `logs/intent-YYYYMMDD.log` | Pre-API order intent |

Broker (Alpaca) = truth in paper/live; `sync_portfolio.py` reconciles.

## 12. Watchlist hygiene

- One ticker per line. Comments after `#` ignored.
- ~25 large-cap, liquid US equities across sectors.
- Routine 5 flags repeat losers/winners. Operator decides.
- Watchlist mutations are operator-only.

## 13. What NOT to do

- Override the −4% / +8% bracket.
- Hold through earnings without operator OK.
- Increase size to recover a drawdown.
- Add a strategy that hasn't passed §9.
- Run live without §8.
- Commit `.env`, intent logs, or live portfolio state.
- Skip the pre-trade intent log.

## 14. One-line summary

**4 strategies, 4 max positions, 10% sizing, 1:2 risk-reward, paper-only until 20 green days, intent-logged before every order, strategy lock enforced by code, kill switches always available.**
