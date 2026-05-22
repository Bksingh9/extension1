from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    alpaca_api_key: str = ""
    alpaca_secret_key: str = ""
    alpaca_base_url: str = "https://paper-api.alpaca.markets"

    anthropic_api_key: str = ""
    notification_webhook: str = ""

    finnhub_api_key: str = ""
    fred_api_key: str = ""
    alpha_vantage_api_key: str = ""

    trading_mode: Literal["dry_run", "paper", "live"] = "dry_run"
    allow_live: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_paper(self) -> bool:
        return self.trading_mode == "paper"

    @property
    def is_live(self) -> bool:
        return self.trading_mode == "live"

    @property
    def is_dry(self) -> bool:
        return self.trading_mode == "dry_run"


def load_config() -> dict:
    with open(ROOT / "config" / "config.json", "r", encoding="utf-8") as f:
        return json.load(f)


settings = Settings()
config = load_config()
