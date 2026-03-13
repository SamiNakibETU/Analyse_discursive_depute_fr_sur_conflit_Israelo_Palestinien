import logging
import logging.config
from pathlib import Path
from typing import Optional


DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(log_file: Optional[Path] = None, level: int = logging.INFO) -> None:
    """Configure structured logging for the pipeline."""

    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": level,
            "formatter": "default",
        }
    }
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers["file"] = {
            "class": "logging.FileHandler",
            "level": level,
            "formatter": "verbose",
            "filename": str(log_file),
            "encoding": "utf-8",
        }

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": DEFAULT_FORMAT},
            "verbose": {"format": DEFAULT_FORMAT},
        },
        "handlers": handlers,
        "root": {
            "level": level,
            "handlers": list(handlers.keys()),
        },
    }
    logging.config.dictConfig(logging_config)

