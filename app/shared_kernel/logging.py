"""
Structured Logging Library Contracts and Sensitive Data Masker.
Neutral logging interfaces without third-party framework dependencies.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import re

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class SensitiveDataMasker:
    """Regex-based masker for credentials, tokens, PII, and API keys."""
    EMAIL_REGEX = re.compile(r"([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    API_KEY_REGEX = re.compile(r"(api[-_]?key|secret|token|password)[\"']?\s*[:=]\s*[\"']?([a-zA-Z0-9_\-\.]{8,})[\"']?", re.IGNORECASE)
    BEARER_REGEX = re.compile(r"(Bearer\s+)[a-zA-Z0-9_\-\.]{16,}", re.IGNORECASE)

    @classmethod
    def mask_text(cls, text: str) -> str:
        if not text:
            return text
        masked = cls.EMAIL_REGEX.sub(r"***@\2", text)
        masked = cls.API_KEY_REGEX.sub(r"\1: [REDACTED_SECRET]", masked)
        masked = cls.BEARER_REGEX.sub(r"\1[REDACTED_BEARER_TOKEN]", masked)
        return masked

@dataclass(frozen=True)
class LogRecord:
    level: LogLevel
    message: str
    logger_name: str = "platform"
    correlation_id: Optional[str] = None
    trace_id: Optional[str] = None
    execution_id: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class StructuredLoggerContract(ABC):
    @abstractmethod
    def log(self, record: LogRecord) -> None:
        pass

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def critical(self, message: str, **kwargs: Any) -> None:
        pass
