"""Connectivity test. Prints account info if keys work, errors otherwise.

Usage:
    python3 scripts/check_alpaca.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.settings import settings  # noqa: E402


def main() -> int:
    print(f"trading_mode = {settings.trading_mode}")
    print(f"base_url     = {settings.alpaca_base_url}")
    print(f"allow_live   = {settings.allow_live}")
    if settings.is_dry:
        print("dry_run mode: no broker call made.")
        return 0
    if not settings.alpaca_api_key or not settings.alpaca_secret_key:
        print("ERROR: missing ALPACA_API_KEY / ALPACA_SECRET_KEY")
        return 1
    try:
        from src.broker import AlpacaBroker
        broker = AlpacaBroker()
        acct = broker.account()
        print(
            f"OK: equity ${acct.equity:,.2f} cash ${acct.cash:,.2f} "
            f"trading_blocked={acct.trading_blocked}"
        )
        positions = broker.positions()
        print(f"open_positions = {len(positions)}")
        return 0
    except Exception as e:
        print(f"ERROR: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
