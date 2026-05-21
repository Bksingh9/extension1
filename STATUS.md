# Status

_Last updated: 2026-05-21_

## Current mode

**`dry_run`** — no broker calls, no orders, no scheduler. Default in `.env.example`.

## Build status

| Component | State | Notes |
|---|---|---|
| Project scaffold | done | branch `claude/trading-playbook-setup-cEwnm` |
| Indicators (RSI/EMA/MACD/BB/ATR/VWAP) | done | Pure-pandas, tested |
| 5 strategies | done | momentum, mean_reversion, breakout, vwap_intraday, news_sentiment |
| Risk manager | done | 13 block reasons, all unit-tested |
| Position sizer (1/4 Kelly) | done | Capped at 10% equity AND 1% per-trade risk |
| ATR bracket helper | done | stop = max(1.5×ATR, 0.5%×entry), target = 2× stop |
| Broker wrapper (Alpaca) | done | dry_run / paper / live modes |
| Audit (SQLite + loguru) | done | `logs/audit.sqlite`, `logs/audit.log` |
| 5 routines | done | premarket, open, midday, eod, friday |
| Backtester | done | yfinance bars, walk-forward |
| HMM regime engine | done | 5 states (CRASH/BEAR/NEUTRAL/BULL/EUPHORIA), aggregate-exposure gate |
| Regime training script | done | `scripts/train_regime.py` — fits on yfinance bars |
| **Performance metrics (empyrical)** | **done** | Sharpe / Sortino / Calmar / max-DD / CAGR in Friday review and backtester |
| **HTML tear-sheet (quantstats)** | **done** | Written to `memory/tearsheet-YYYY-MM-DD.html` each Friday |
| Tests | 55 / 55 passing | + features, allocation, regime, performance |
| GitHub Actions scheduler | scaffolded, disabled | `.yml.disabled` — opt-in by renaming |
| Notifications | stub ready | Slack/ClickUp/Discord webhook compatible |
| News sentiment (Claude) | optional | Falls back to neutral 0 without `ANTHROPIC_API_KEY` |

## What works right now (no keys needed)

```bash
pytest -q                                           # 49 passing
python3 scripts/train_regime.py --symbol SPY --days 504   # fits HMM, saves model
python3 scripts/backtest.py --days 1000             # needs yfinance
TRADING_MODE=dry_run python3 routines/routine_03_midday.py
TRADING_MODE=dry_run python3 routines/routine_04_eod.py
```

## Gates to start paper trading (operator action)

- [ ] `pip install -r requirements.txt` in a venv.
- [ ] Create paper account at <https://alpaca.markets> (free).
- [ ] `cp .env.example .env`, fill in `ALPACA_API_KEY` + `ALPACA_SECRET_KEY` (paper keys).
- [ ] Set `TRADING_MODE=paper` in `.env`.
- [ ] `python3 scripts/check_alpaca.py` — should print equity and confirm connectivity.
- [ ] Run all five routines manually once each.
- [ ] (Optional) rename `.github/workflows/trading-routines.yml.disabled` → `.yml`
      and add `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` as repo secrets.

## Gates to go live (all three required)

- [ ] **Paper soak**: ≥ 20 green paper-trading days in `memory/journal.md`.
- [ ] **Expectancy**: routine_05_friday shows positive R-expectancy.
- [ ] **`.env`**: `TRADING_MODE=live` AND `ALLOW_LIVE=true`.
- [ ] **Separate live keys**: distinct from paper keys.
- [ ] **`memory/go-live.md`** exists and contains `GO LIVE CONFIRMED`.
- [ ] **First-week throttle**: set `max_position_pct` to `0.02` in `config/config.json` for 5 trading days, then back to `0.10`.

## What I will NOT do for you

- Place live orders or auto-flip the live gate.
- Commit `.env` or any keys.
- Enable the scheduler — you rename the workflow file.
- Run during market hours unless you explicitly invoke a routine.
- Add Indian-market support to this repo (separate effort, different broker).

## Open questions for you

1. Paper-trading account ready? Do you want me to walk you through the Alpaca signup + `.env` step-by-step in your local terminal?
2. Notification target — Slack / ClickUp / Discord / none? I can wire the exact payload format if you share the webhook style.
3. Watchlist — keep the default 20-symbol list, or you want to swap any?
