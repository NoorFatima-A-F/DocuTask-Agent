"""
Structured Logging Module.
Configures python logging for production readiness.
"""

import logging
import sys
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Configures structured application logging."""
    logger = logging.getLogger("ai_doc_platform")
    
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(log_level)

    # Avoid duplicate handlers if setup is called multiple times
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logging()
