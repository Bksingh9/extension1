"""Shared helpers for the predict-market skill scripts."""
from __future__ import annotations

import json
import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
# Repo root is four levels up: scripts/ -> predict-market-bot/ -> skills/ -> .claude/ -> repo
REPO_ROOT = SKILL_DIR.parents[2]
STOP_FILE = REPO_ROOT / "STOP"


def load_config() -> dict:
    with open(SKILL_DIR / "config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def kill_switch_active() -> bool:
    """A file named STOP at repo root halts all new orders."""
    return STOP_FILE.exists()


def trading_mode() -> str:
    return os.getenv("TRADING_MODE", "dry_run").lower()


def allow_live() -> bool:
    return os.getenv("ALLOW_LIVE", "false").lower() == "true"
