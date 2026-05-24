# Platforms & APIs

> Verify all endpoints/auth against current official docs before live use.
> Signatures here are a starting reference, not a guarantee.

## Kalshi (US-regulated)
- Base (demo): `https://demo-api.kalshi.co/trade-api/v2`
- Base (prod): `https://api.elections.kalshi.com/trade-api/v2`
- Toggle: `KALSHI_DEMO=true|false` (default true). Read-only market discovery
  needs no auth on either base.
- Market discovery: `GET /markets?status=open&limit=...`
- Orderbook: `GET /markets/{ticker}/orderbook`
- Place order: `POST /portfolio/orders` (auth required)
- Auth (orders only): API key id + RSA-PSS request signing. Env:
  `KALSHI_API_KEY_ID`, `KALSHI_PRIVATE_KEY`.
- Demo environment has mock funds but markets are typically empty
  (vol/liquidity ≈ 0) — fine for plumbing, useless for real signals.
- **Current field schema (string-typed):** `volume_fp`, `volume_24h_fp`,
  `liquidity_dollars`, `yes_bid_dollars`, `yes_ask_dollars`, `close_time`.
  Prices are already 0–1 USD (NOT cents). `normalize_kalshi_market()` maps
  these to the scan dict; yes_price is the bid/ask mid.

## Polymarket (crypto-native, Polygon)
- CLOB base: `https://clob.polymarket.com`
- Markets: `GET /markets`
- Orderbook: `GET /book?token_id=...`
- Orders: EIP-712 signed via official `py-clob-client`.
- Auth/env: `POLYMARKET_PK` (Polygon wallet key),
  `POLYMARKET_API_KEY` / `_SECRET` / `_PASSPHRASE`.
- Geo-restrictions apply — check eligibility in your jurisdiction.

## Unified wrapper
- `pmxt` (CCXT-style wrapper across prediction markets) is an option to avoid
  maintaining two connectors.

## Connector behavior in this skill
- `list_markets()` reads public data without a key and returns [] on failure.
- `place_order(dry_run=True)` never touches the network — returns a simulated ack.
- Live order placement is a marked TODO in each connector; wire it with the
  official client + your credentials.
