import os
from flask import Flask
import logging
from pathlib import Path

LOG_FILENAME = os.getenv("API_LOG_FILE", "/logs/api.log")


def configure_logging(app: Flask):
    """
    Configure application logging.
    """
    app.logger.setLevel(logging.INFO)

    if app.config.get("TESTING"):
        if not app.logger.handlers:
            app.logger.addHandler(logging.StreamHandler())
        return

    try:
        log_path = Path(LOG_FILENAME)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(LOG_FILENAME)
    except OSError:
        log_path = Path(LOG_FILENAME)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_path)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)

    app.logger.setLevel(logging.INFO)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
