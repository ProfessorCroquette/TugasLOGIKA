"""
Logging configuration
"""

import logging
import logging.config
from pathlib import Path
from config.settings import LOGS_DIR, LOG_LEVEL

# Create logs directory
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": LOG_LEVEL,
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "level": LOG_LEVEL,
            "filename": LOGS_DIR / "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "level": "ERROR",
            "filename": LOGS_DIR / "errors.log",
            "maxBytes": 10485760,
            "backupCount": 5
        }
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console", "file", "error_file"]
    },
    "loggers": {
        "src": {
            "level": LOG_LEVEL,
            "handlers": ["console", "file"]
        },
        "database": {
            "level": "DEBUG",
            "handlers": ["file"]
        }
    }
}

def setup_logging():
    """Setup logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(__name__)
