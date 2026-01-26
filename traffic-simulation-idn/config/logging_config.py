"""
Logging configuration
"""

import logging
import logging.config
from pathlib import Path
from config.settings import LOGS_DIR, LOG_LEVEL

# Create logs directory
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def cleanup_old_logs(log_dir=LOGS_DIR, max_logs=10):
    """
    Delete old log files if count exceeds maximum.
    Keeps the newest log files and removes oldest ones.
    
    Args:
        log_dir: Directory containing log files
        max_logs: Maximum number of log files to keep
    """
    try:
        # Get all log files (including rotated ones)
        log_files = sorted(log_dir.glob("*.log*"))
        
        if len(log_files) > max_logs:
            num_to_delete = len(log_files) - max_logs
            for log_file in log_files[:num_to_delete]:
                try:
                    log_file.unlink()
                    logging.getLogger(__name__).debug(f"Deleted old log: {log_file.name}")
                except Exception as e:
                    logging.getLogger(__name__).warning(f"Failed to delete {log_file.name}: {e}")
    
    except Exception as e:
        logging.getLogger(__name__).error(f"Error during log cleanup: {e}")

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
    """Setup logging configuration with automatic cleanup"""
    # Cleanup old logs before setting up logging
    cleanup_old_logs(log_dir=LOGS_DIR, max_logs=10)
    
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(__name__)
