# Platforms — Polymarket & Kalshi

> API notes for the scan + execute steps. These steps need live
> network access and credentials and therefore **do not run from the
> original dev sandbox** (every external host is firewalled there).
> Run them on your own machine / VPS / CI runner.

## Polymarket

- **Type:** crypto-native, Central Limit Order Book (CLOB) with
  off-chain matching, on-chain settlement on Polygon.
- **Discovery:** REST API for markets.
- **Live data:** WebSocket API for orderbook updates.
- **Auth:** EIP-712 signing with your wallet key.
- **Geo:** geo-restricted in some jurisdictions — check before use.
- **Caution:** on-chain settlement means gas + irreversible txns.
  Paper-trade the logic before signing anything.

## Kalshi

- **Type:** US-regulated exchange (CFTC).
- **API:** REST. Requests require header signing.
- **Demo:** has a **demo environment with mock funds** — use this for
  weeks before going live. This is the safest place to start.
- **Legal:** Developer Agreement applies; US-regulated, know the rules
  in your jurisdiction.

## Unified wrapper

- **pmxt** — CCXT-style wrapper across prediction-market venues. Worth
  using so the scan/execute code isn't tied to one platform's quirks.

## Credentials handling

- Never commit keys. Read from env / a gitignored `.env`.
- Polymarket wallet key and Kalshi API secret are bearer credentials —
  treat them like passwords.
- The execution agent must check the `STOP` kill-switch file before
  every order.

## Recommended ramp (from the guide, condensed)

1. **Week 1:** accounts on both. Kalshi demo with mock funds. Manual
   trades to learn mechanics.
2. **Week 2:** build scan, log data, **don't trade**.
3. **Week 3:** build research + predict, backtest, track Brier score.
4. **Week 4:** build risk (this skill), **paper-trade ≥ 2 weeks**.
5. **Week 5+:** go live with $100–500 max total exposure. Scale only
   after 50+ trades with verified positive, out-of-sample results.

## Open-source repos to study (from the guide)

- `github.com/ryanfrigo/kalshi-ai-trading-bot` — multi-model AI
- `github.com/suislanchez/polymarket-kalshi-weather-bot` — weather markets + Kelly
- `github.com/CarlosIbCu/polymarket-kalshi-btc-arbitrage-bot` — arbitrage

Study them; don't trust them with funds unaudited.
