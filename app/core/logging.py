"""Application logging with secret scrubbing.

Every formatted log line (message, arguments and tracebacks) passes through
:func:`scrub`, which masks the configured secrets (JWT secret, Gemini keys, database and
Redis passwords) and generic credential shapes (bearer tokens, JWTs, Google API keys,
``password``/``key``/``token`` parameters, ``user:password@`` in URLs).
"""

from __future__ import annotations

import contextlib
import logging
import os
import re
import sys
from urllib.parse import urlsplit

from app.core.config import settings

MASK = "***"

_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/=-]+"), rf"\1 {MASK}"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]+"), MASK),  # JWT
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), MASK),  # Google API key
    (re.compile(r"(?i)\b(x-goog-api-key|authorization)(['\"]?\s*[:=]\s*['\"]?)[^\s'\",}]+"), rf"\1\2{MASK}"),
    (
        re.compile(
            r"(?i)([\"']?(?:password|passwd|secret|api[_-]?key|access_token|refresh_token|token|key)[\"']?\s*[:=]\s*[\"']?)[^\s\"'&,}]+"
        ),
        rf"\1{MASK}",
    ),
    (re.compile(r"(?i)\b([a-z][a-z0-9+.-]*://[^:/\s@]*:)[^@\s/]+@"), rf"\1{MASK}@"),  # user:pass@ in URLs
]


def _configured_secrets() -> list[str]:
    values = [settings.JWT_SECRET, settings.GEMINI_API_KEY, settings.GOOGLE_API_KEY]
    values += [os.environ.get("AWS_SECRET_ACCESS_KEY"), os.environ.get("AWS_SESSION_TOKEN")]
    for url in (settings.DATABASE_URL, settings.REDIS_URL):
        if url:
            with contextlib.suppress(ValueError):
                values.append(urlsplit(url).password)
    # Very short values would mask ordinary words; real secrets are long.
    return sorted({v for v in values if v and len(v) >= 8}, key=len, reverse=True)


def scrub(text: str) -> str:
    """Mask secrets in a log line."""
    for secret in _configured_secrets():
        text = text.replace(secret, MASK)
    for pattern, repl in _PATTERNS:
        text = pattern.sub(repl, text)
    return text


class ScrubbingFormatter(logging.Formatter):
    """Formatter that scrubs the fully formatted record, including exception text."""

    def __init__(self, inner: logging.Formatter | None = None, **kwargs: object):
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self.inner = inner

    def format(self, record: logging.LogRecord) -> str:
        text = self.inner.format(record) if self.inner else super().format(record)
        return scrub(text)


def install_secret_scrubbing(*logger_names: str) -> None:
    """Wrap the formatters of existing handlers (root, uvicorn, httpx, celery ...) with scrubbing."""
    for name in ("", "uvicorn", "uvicorn.error", "uvicorn.access", "celery", *logger_names):
        for handler in logging.getLogger(name).handlers:
            if not isinstance(handler.formatter, ScrubbingFormatter):
                handler.setFormatter(ScrubbingFormatter(handler.formatter or logging.Formatter()))


def setup_logging() -> logging.Logger:
    """Configure the application logger (stdout, scrubbed)."""
    app_logger = logging.getLogger("ai_doc_platform")
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    app_logger.setLevel(log_level)

    if not app_logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(
            ScrubbingFormatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        app_logger.addHandler(console_handler)
    install_secret_scrubbing()
    return app_logger


logger = setup_logging()
