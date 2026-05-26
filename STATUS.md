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
| Risk manager | done | market-aware (US / India / crypto-24x7 / forex-IST); 13 block reasons, all unit-tested |
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
| Tests | 137 / 137 passing | US + India + crypto + forex + prediction-market, mocked offline; ruff + CI gate |
| GitHub Actions scheduler | scaffolded, disabled | `.yml.disabled` — opt-in by renaming |
| Notifications | stub ready | Slack/ClickUp/Discord webhook compatible |
| News sentiment (Claude) | optional | Falls back to neutral 0 without `ANTHROPIC_API_KEY` |
| Finnhub news + earnings | done | 60 req/min free. Set `FINNHUB_API_KEY`. Falls back to yfinance. |
| FRED macro snapshot | done | VIX / 10Y / Fed funds / unemployment in premarket. No key needed. |
| Stocktwits retail sentiment | done | Bullish/bearish ratio per symbol. No key. Blended 60/40 with Claude news score. |
| Alpha Vantage bars fallback | done | 3rd-tier bars source (Alpaca → yfinance → AV). Set `ALPHA_VANTAGE_API_KEY`. |
| **Bigdata.com earnings transcripts** | **done** | Latest earnings-call transcript feeds the Claude sentiment scorer. SDK `bigdata-client`; set `BIGDATA_USERNAME`/`BIGDATA_PASSWORD`. Degrades to no-op without creds. |
| **Prediction-market skill** | **done** | Claude Code skill `.claude/skills/predict-market-bot/` (Polymarket/Kalshi). Deterministic Kelly + 11-check risk gate + edge/EV/Brier + scan + STOP kill switch + compound ledger. dry_run default. |
| **Indian market (NSE) adapter** | **done** | `src/kite_broker.py` (Zerodha Kite) + `config/india.json` (20 NSE large-caps) + `scripts/india_scan.py`. Reuses strategies/bracket/Kelly. Bars via yfinance `.NS`. Live order = LIMIT+GTT-OCO TODO. Set `MARKET=india`, `KITE_API_KEY`, `KITE_ACCESS_TOKEN`. |
| **Crypto adapter (ccxt)** | **done** | `src/ccxt_broker.py` + `config/crypto.json` (24/7, 30% tax + 1% TDS no-offset modeled). Bars via yfinance `-USD`. Live order = limit+reduce-only TODO. Set `MARKET=crypto`, `CCXT_*`. |
| **Forex adapter (NSE F&O)** | **done** | `config/india_fx.json` (USDINR etc.) via `KiteBroker` currency F&O — legal path only, NOT offshore FX. |
| **Cost model + OOS backtest** | **done** | `src/costs.py` + `src/markets.py`; `backtest.py --market` reports gross/net/after-tax, in-sample vs out-of-sample. |
| **CI / lint / security** | **done** | `.github/workflows/ci.yml` (ruff + pytest), `ruff.toml`, `.pre-commit-config.yaml`, `SECURITY.md` (11 findings; prompt-injection hardening). |
| **Generic scanner** | **done** | `scripts/market_scan.py --market {us,india,crypto,forex}` — dry-run, full risk gate, no keys. |

## What works right now (no keys needed)

```bash
pytest -q                                           # 137 passing
TRADING_MODE=dry_run python3 .claude/skills/predict-market-bot/scripts/pipeline.py  # prediction-market dry run
MARKET=india TRADING_MODE=dry_run python3 scripts/india_scan.py    # NSE scan (yfinance .NS bars)
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

## Open questions for you

1. Paper-trading account ready? Do you want me to walk you through the Alpaca signup + `.env` step-by-step in your local terminal?
2. Notification target — Slack / ClickUp / Discord / none? I can wire the exact payload format if you share the webhook style.
3. Watchlist — keep the default 20-symbol list, or you want to swap any?
