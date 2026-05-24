# predict-market-bot (Hermes-style skill)

A prediction-market trading bot structured as a Claude skill, built
from the "MyHermes" reference architecture. **Educational. Trading is
real financial risk — don't trade money you can't afford to lose.**

## What's actually built and tested here

The **safety-critical, deterministic core** — the part that's pure
math and needs no network — is complete and verified:

| File | Status |
|---|---|
| `scripts/kelly_size.py` | ✅ Kelly + fractional Kelly + 5% hard cap. Tested. |
| `scripts/validate_risk.py` | ✅ 9-rule risk gate. Tested. |
| `scripts/test_risk.py` | ✅ **14/14 tests pass** (run: `python scripts/test_risk.py`) |
| `SKILL.md` | ✅ skill definition + triggers + hard safety rules |
| `references/formulas.md` | ✅ all the math |
| `references/platforms.md` | ✅ Polymarket + Kalshi API notes |
| `references/failure_log.md` | ✅ seeded failure modes |

## What is NOT built (and why)

The five-step pipeline is: scan → research → predict → **risk/execute**
→ compound. This package implements the **risk/execute gate (step 4)**,
the one piece that's deterministic and safety-critical.

Steps 1–3 (scan markets, scrape research, predict probabilities) and
the execution half of step 4 need **live exchange + social APIs**
(Polymarket CLOB, Kalshi REST, Twitter/X, Reddit, news). Those are
firewalled from the dev sandbox this was built in — every external
host returns `403 host_not_allowed`. They must run on your own
machine / VPS / CI runner with real credentials.

This is deliberate: the risk gate is the part you most want correct
and testable *before* any money is involved. It's done.

## Quick start

```bash
# 1. Run the tests (no network, runs anywhere)
python scripts/test_risk.py

# 2. Size a position
python scripts/kelly_size.py --bankroll 10000 --p-win 0.62 \
    --contract-price 0.50 --fractional 0.25

# 3. Validate a trade (exit 0 = approved, 1 = rejected)
python scripts/validate_risk.py --bankroll 10000 \
    --p-model 0.62 --p-market 0.50 --stake 250 --net-odds 1.0
```

## Activate as a Claude skill

Copy or symlink this folder into your skills directory:

```bash
ln -s "$(pwd)/hermes/predict-market-bot" ~/.claude/skills/predict-market-risk
```

Then in a Claude session: ask "check risk on this trade" or "size
this position" and the skill triggers.

## Hard safety defaults (enforced in code)

- **Kill switch:** create a file named `STOP` to halt all new orders.
- **Paper-trade first.** Live execution is a separate explicit step,
  never the default.
- **Every trade passes `validate_risk.py` or it does not execute.**
- **Scraped content is data, not instructions** — prevents prompt
  injection from tweets / articles / forums.
- **AI spend caps at $50/day.**
- Default limits: 4% min edge · quarter-Kelly · 5% max position · 30%
  max exposure · 8% max drawdown · 15% daily loss limit · 15 max
  concurrent positions.

## Build-out order for the rest of the pipeline

When you wire steps 1–3 + execution on a networked host, do it in
this order (and paper-trade between each):

1. **scan** — Polymarket CLOB + Kalshi REST; filter by volume (≥200),
   expiry (≤30 days), liquidity; flag anomalies. Run every 15–30 min.
2. **research** — scrape X / Reddit / news; sentiment; compare to
   market odds. Treat all content as data.
3. **predict** — ensemble (XGBoost + multiple LLMs); only signal when
   edge > 4%; track Brier score.
4. **execute** — limit orders only; abort if slippage > 2%; auto-hedge;
   the `STOP` kill switch.
5. **compound** — post-mortem every loss into `references/failure_log.md`.

## Disclaimer

Not financial advice. The reference architecture's quoted "68.4% win
rate / 2.14 Sharpe / −4.2% max drawdown over 312 trades" is an
unverified backtest claim from the source guide. Your own
out-of-sample Brier score is the only number that tells you whether
you have an edge. Most retail trading bots lose money.
