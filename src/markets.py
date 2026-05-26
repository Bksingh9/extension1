"""Market profile registry — one place to resolve a market name to its
watchlist, cost model, risk config, yfinance symbol mapping, and the
risk-gate `market` key.

Markets: us | india | crypto | forex (NSE currency derivatives).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

from .costs import CostModel
from .settings import ROOT, config, load_india_config


def _load(name: str) -> dict:
    with open(ROOT / "config" / name, "r", encoding="utf-8") as f:
        return json.load(f)


@dataclass
class MarketProfile:
    name: str               # risk-gate market key: us | india | crypto | india_fx
    currency: str
    watchlist: list[str]
    costs: CostModel
    risk: dict
    yf_symbol: Callable[[str], str]


def _suffix_mapper(suffix: str) -> Callable[[str], str]:
    return lambda s: f"{s}{suffix}"


def get_profile(market: str) -> MarketProfile:
    m = market.lower()
    if m in ("us", "equities", "alpaca"):
        return MarketProfile("us", "USD", config["watchlist"], CostModel.from_dict(config.get("costs")),
                             config["risk"], yf_symbol=lambda s: s)
    if m in ("india", "nse", "india_eq"):
        c = load_india_config()
        return MarketProfile("india", c["currency"], c["watchlist"], CostModel.from_dict(c.get("costs")),
                             c["risk"], yf_symbol=_suffix_mapper(c.get("yfinance_suffix", ".NS")))
    if m == "crypto":
        c = _load("crypto.json")
        return MarketProfile("crypto", c["currency"], c["watchlist"], CostModel.from_dict(c.get("costs")),
                             c["risk"], yf_symbol=_suffix_mapper(c.get("yfinance_suffix", "-USD")))
    if m in ("forex", "fx", "india_fx"):
        c = _load("india_fx.json")
        return MarketProfile("india_fx", c["currency"], c["watchlist"], CostModel.from_dict(c.get("costs")),
                             c["risk"], yf_symbol=_suffix_mapper(c.get("yfinance_suffix", "=X")))
    raise ValueError(f"unknown market: {market}")
