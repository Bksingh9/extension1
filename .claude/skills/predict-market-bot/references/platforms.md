# Platforms & APIs

> Verify all endpoints/auth against current official docs before live use.
> Signatures here are a starting reference, not a guarantee.

## Kalshi (US-regulated)
- Base (demo): `https://demo-api.kalshi.co/trade-api/v2`
- Base (prod): `https://api.elections.kalshi.com/trade-api/v2`
- Market discovery: `GET /markets?status=open&limit=...`
- Orderbook: `GET /markets/{ticker}/orderbook`
- Place order: `POST /portfolio/orders` (auth required)
- Auth: API key id + RSA-PSS request signing. Env:
  `KALSHI_API_KEY_ID`, `KALSHI_PRIVATE_KEY`.
- Demo environment has mock funds — use it for paper trading.
- Prices are in cents (0–100); connector normalizes to 0–1.

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
