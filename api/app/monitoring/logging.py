from flask import Flask
import logging
from pathlib import Path

LOG_FILENAME = "../logs/api.log"


def configure_logging(app: Flask):
    """
    Configure application logging.
    """

    Path("logs").mkdir(exist_ok=True)

    handler = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)

    app.logger.setLevel(logging.INFO)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
