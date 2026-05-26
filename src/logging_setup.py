from __future__ import annotations

import sys

from loguru import logger

from .settings import ROOT, settings

_configured = False


def get_logger():
    global _configured
    if not _configured:
        logs_dir = ROOT / "logs"
        logs_dir.mkdir(exist_ok=True)
        logger.remove()
        logger.add(sys.stderr, level=settings.log_level)
        logger.add(
            str(logs_dir / "audit.log"),
            level="DEBUG",
            rotation="10 MB",
            retention=30,
            enqueue=True,
            backtrace=False,
            diagnose=False,
        )
        _configured = True
    return logger
