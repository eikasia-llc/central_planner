"""
Centralized logging configuration.

Emits structured JSON logs to stdout. Cloud Run forwards stdout to Cloud Logging
where JSON fields are automatically parsed (severity, message, timestamp, etc.).

Usage — call once from each bootstrap file (api_server.py, app.py):

    from log_config import setup_logging
    setup_logging()
"""

import logging
import os
import sys

try:
    from pythonjsonlogger.json import JsonFormatter          # v3+
except ImportError:
    from pythonjsonlogger.jsonlogger import JsonFormatter    # v2.x

_initialized = False


def setup_logging():
    """Configure root logger with JSON output and install uncaught exception hook."""
    global _initialized
    if _initialized:
        return
    _initialized = True

    level = os.environ.get("LOG_LEVEL", "INFO").upper()

    handler = logging.StreamHandler(sys.stderr)
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d %(funcName)s",
        rename_fields={"asctime": "timestamp", "levelname": "severity"},
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    # Capture uncaught exceptions as CRITICAL logs with full traceback
    _default_excepthook = sys.excepthook

    def _log_uncaught(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            _default_excepthook(exc_type, exc_value, exc_tb)
            return
        logging.critical(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_tb)
        )

    sys.excepthook = _log_uncaught
