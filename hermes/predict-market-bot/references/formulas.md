# Formulas

All implemented in `scripts/`. This is the human reference.

## Market edge

```
edge = p_model - p_market
```

Only consider trading when `edge > 0.04`. `p_market` is the contract
price (a $0.49 contract implies a 49% probability).

## Expected value

```
EV = p * b - (1 - p)
```

- `p` = your model's win probability
- `b` = net decimal odds = payout/stake − 1 (even money = 1.0)

For a prediction-market contract bought at price `c` that pays $1:

```
b = (1 - c) / c
```

## Mispricing score (z-score)

```
delta = (p_model - p_market) / sigma
```

Standardised divergence of your model from the market. `sigma` is the
standard deviation of your model's estimate (from ensemble spread or
historical calibration). Higher |delta| = stronger signal.

## Kelly Criterion (position sizing)

```
f* = (p * b - q) / b        q = 1 - p
```

- Clamp `f*` to 0 when negative (no bet).
- Use **fractional Kelly**: `f_used = f* × k`, `k ∈ [0.25, 0.5]`.
- Then hard-cap at 5% of bankroll per position.

Worked values (verified in `test_risk.py`):

| p | b | full f* | quarter | note |
|---|---|---------|---------|------|
| 0.60 | 1.0 | 0.20 | 0.05 | even money |
| 0.70 | 2.0 | 0.55 | 0.1375 | capped to 5% in practice |
| 0.50 | 1.0 | 0.00 | 0.00 | break-even, no bet |
| 0.40 | 1.0 | 0.00 | 0.00 | negative edge, clamped |

> The source PDF states p=0.7, b=2 → "full Kelly 12%". That is
> inconsistent with the standard formula, which gives 55%. We
> implement the standard formula. Treat third-party dollar examples
> as illustrative only.

## Brier score (calibration tracking)

```
BS = (1/n) * sum((predicted - outcome)^2)
```

`outcome` is 1 if the event happened, else 0. Lower is better; a
well-calibrated model tracks **below 0.25**. This is the only honest
measure of whether you actually have an edge.

## Value at Risk (95%)

For a single binary contract, the loss on a losing bet is the full
stake. The 95% VaR of the position is `stake` when P(loss) > 5%, else
0. For a book, sum independent position VaRs (a conservative proxy;
correlated markets need a covariance-aware model).

## Performance metrics (the compound step tracks these)

| Metric | Target | Meaning |
|---|---|---|
| Win rate | ≥ 60% | fraction of profitable trades |
| Sharpe ratio | > 2.0 | risk-adjusted return |
| Max drawdown | < 8% | largest peak-to-trough; blocks new trades |
| Profit factor | > 1.5 | gross profit ÷ gross loss |
| Brier score | < 0.25 | prediction calibration |
