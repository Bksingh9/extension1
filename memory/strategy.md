# Active Strategy Rules — Mode B (canonical)

This file is the **source of truth** for strategy rules. The Friday review
routine may rebalance `strategy_weights` in `config/config.json`, but the rule
definitions below are operator-only edits.

## Hard, non-negotiable risk constraints

1. Risk ≤ 1% of equity per trade (sized off ATR stop distance).
2. Max 10 concurrent positions.
3. Every position has an ATR-based stop, minimum 0.5% below entry.
4. Never average down a loser.
5. Halt all new entries if intraday DD ≤ −3%.
6. PDT compliance for accounts < $25k: ≤ 3 day-trades / rolling 5 business days.
7. No new entries in the last 5 minutes before close.
8. Trades only during regular market hours (09:35–15:55 ET).
9. Minimum R/R 2:1 to enter.
10. Profit target: 2× ATR (swing) or 1.5% (intraday).

## Five strategies

| # | Name | Entry conditions |
|---|---|---|
| 1 | `momentum` | RSI(14) > 55, MACD hist turns positive, EMA(9) > EMA(21) > EMA(50), close > prior-day high, vol > 1.5× 20d avg |
| 2 | `mean_reversion` | Touches lower BB(20,2), RSI(14) < 35, EMA(50) slope flat or up, first green candle |
| 3 | `breakout` | Close > 20-day high with vol > 2× 20d avg |
| 4 | `vwap_intraday` | Reclaims VWAP after pullback, RSI recovering from < 45, candle closes above VWAP |
| 5 | `news_sentiment` | Claude-scored sentiment ≥ +6, no earnings within 2 trading days, plus a technical confirmation from 1–4 |

## Stop / target rules (universal, NOT strategy-specific)

- Stop distance = max(1.5 × ATR(14), 0.5% × entry).
- Target distance = max(2 × ATR(14), 2 × stop distance) — i.e. R/R ≥ 2.
- Time stop: 30 trading days for swings; intraday strategies (vwap, breakout-day) close by EOD.
- Trailing stop: only after +1× ATR unrealized; trail at 1× ATR behind high-water mark.

## Position sizing

- Kelly fraction = W − (1−W)/R, where W = win rate, R = avg-win / avg-loss.
- Use 1/4 Kelly. Cap at 10% of equity. Floor at 0 (no negative-Kelly trades).
- Compute W and R from the most recent 30 closed trades in `memory/journal.md`.
- Cold-start defaults: W = 0.5, R = 1.5.

### The Kelly-fraction knob (operator, "max growth" within caps)

`config/config.json → sizing.kelly_fraction` (default `0.25`) is the single
lever for the growth/variance tradeoff. It multiplies the raw Kelly estimate
before the hard caps apply.

| Setting | Behaviour | Tradeoff |
|---|---|---|
| 0.10–0.25 | Conservative (default 0.25 = quarter-Kelly) | Smoother equity curve, slow compounding, low ruin risk |
| 0.50 | Half-Kelly | ~Higher growth, materially larger drawdowns |
| 1.00 | Full Kelly | Theoretical max growth rate, but ~50% drawdowns are normal and a bad win-rate estimate can ruin the account |
| > 1.0 | Over-betting | Negative long-run growth despite a positive edge — do NOT |

Raising this is the ONLY sanctioned way to chase higher growth. The hard caps
(1% risk/trade, max positions, daily-DD circuit breaker, kill switch) are NOT
adjustable for that purpose and always bind after the Kelly multiplier. Edit
the value in config; no code change needed (`src/position_sizer.py` reads it).

## Regime layer (HMM, optional gate on aggregate exposure)

A 5-state Gaussian HMM is fit on the primary symbol (default `SPY`) to label
the current market regime as one of: `CRASH`, `BEAR`, `NEUTRAL`, `BULL`,
`EUPHORIA`. Each regime maps to a target *aggregate* exposure cap:

| Regime | Aggregate exposure cap |
|---|---|
| CRASH | 10% |
| BEAR | 40% |
| NEUTRAL | 60% |
| BULL | 95% |
| EUPHORIA | 95% |

If posterior confidence for the labeled state is below `0.60`, the layer
defaults to `NEUTRAL` (60%). Per-trade caps (1% risk, 10% size) and every
risk-manager block reason still apply on top of this.

To train: `python3 scripts/train_regime.py` (writes `models/regime.joblib`).
The premarket and open routines load the model if present; if absent they
default to NEUTRAL.

## Strategy admission

A new strategy is admitted only when:
1. Implemented as a pure `Signal | None` function in `src/strategies.py`.
2. Backtested ≥ 1000 trading days on real Alpaca bars via `scripts/backtest.py`.
3. ≥ 30 trades AND expectancy > 0R AND Sharpe > 0.5.
4. Operator approves by name in this file.
5. Listed in this file and reflected in `config/config.json` `strategy_weights`.
