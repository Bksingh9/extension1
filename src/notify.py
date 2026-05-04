"""Notification stub. Posts plaintext to NOTIFICATION_WEBHOOK if set,
otherwise just logs locally. Compatible with Slack incoming webhooks and
ClickUp/Discord/etc. since we POST {"text": "..."}."""
from __future__ import annotations

from .logging_setup import get_logger
from .settings import settings

log = get_logger()


def send(message: str) -> bool:
    if not settings.notification_webhook:
        log.info(f"[notify] {message}")
        return False
    try:
        import requests
        r = requests.post(settings.notification_webhook, json={"text": message}, timeout=8)
        ok = 200 <= r.status_code < 300
        if not ok:
            log.warning(f"notify webhook responded {r.status_code}: {r.text[:200]}")
        return ok
    except Exception as e:
        log.warning(f"notify webhook failed: {e}")
        return False
