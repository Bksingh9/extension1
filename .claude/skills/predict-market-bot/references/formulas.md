# Formulas

All implemented in `scripts/`. This file is the human reference.

## Edge
```
edge = p_model - p_market
```
Only trade when `edge > 0.04`.

## Expected value (per $1 on a YES contract at price `price`)
```
b  = (1 - price) / price          # net decimal odds
EV = p * b - (1 - p)
```
Trade only when `EV > 0`.

## Mispricing z-score
```
delta = (p_model - p_market) / std
```
Higher = stronger divergence from market.

## Kelly position sizing
```
f* = (p * b - q) / b              # q = 1 - p, b = net odds
stake = min(f* * kelly_fraction, max_position_pct) * bankroll
```
Default `kelly_fraction = 0.25` (quarter-Kelly), `max_position_pct = 0.05`.

Example: bankroll $10,000, p=0.70, 2:1 odds (price=1/3, b=2).
Full Kelly f* = (0.70*2 - 0.30)/2 = 0.55 → but capped; quarter-Kelly of the
raw edge lands near the 3% the guide cites.

## Brier score (calibration)
```
BS = (1/n) * sum((predicted - outcome)^2)
```
Lower is better; target < 0.25.

## Performance targets
- Win rate ≥ 60%
- Sharpe ≥ 2.0
- Profit factor ≥ 1.5 (gross_profit / gross_loss)
- Max drawdown < 8% (else block new trades)
