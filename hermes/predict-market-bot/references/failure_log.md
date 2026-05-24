# Failure log

The compound step appends here after every loss. The scan + research
agents read this BEFORE processing new markets, so the system stops
repeating mistakes. Seeded with the canonical failure modes.

Format per entry:

```
## YYYY-MM-DD · market_id · $loss
type: prediction | timing | execution | external_shock
what happened: ...
lesson: ...
guardrail added: ...
```

---

## SEED — known failure modes (no real trades yet)

### bad_calibration
Model says 80%, reality is 55%. You oversize and bleed out.
**Guardrail:** track Brier score; pause live trading if it exceeds 0.25.

### overfitting
Backtest looks amazing, live fails.
**Guardrail:** always evaluate on out-of-sample data; require 50+ live
paper trades before scaling.

### liquidity_trap
Looks tradeable, but orderbook depth can't fill at your price.
**Guardrail:** check orderbook depth + spread before sizing; the scan
step already filters spread > 5¢ and volume < 200 contracts.

### api_failure
Platform downtime leaves an orphaned position.
**Guardrail:** execution agent must reconcile open orders on reconnect;
never assume a fill without confirmation.

### runaway_cost
Heartbeat checks with full context cost $50/day.
**Guardrail:** ai_budget check in validate_risk.py blocks at $50/day;
keep heartbeats cheap (no full-context calls on a timer).

### regulatory
Geo-restriction or jurisdiction rule violated.
**Guardrail:** confirm platform availability in your jurisdiction
before enabling live mode.
