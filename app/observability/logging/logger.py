"""Enterprise Structured Logger with Context Enrichment."""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from ..core.context import ObservabilityContext, get_current_context
from .formatter import JSONLogFormatter
from .storage import LogEntry, LogStorageBackend


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


LEVEL_ORDER = {
    LogLevel.DEBUG: 10,
    LogLevel.INFO: 20,
    LogLevel.WARNING: 30,
    LogLevel.ERROR: 40,
    LogLevel.CRITICAL: 50,
}


class StructuredLogger:
    """Enterprise SRE logger attaching trace IDs, tenant IDs, and emitting structured logs."""

    def __init__(
        self,
        service_name: str = "docutask-platform",
        min_level: LogLevel = LogLevel.INFO,
        storage: Optional[LogStorageBackend] = None,
        formatter: Optional[JSONLogFormatter] = None,
    ):
        self.service_name = service_name
        self.min_level = min_level
        self.storage = storage or LogStorageBackend()
        self.formatter = formatter or JSONLogFormatter()
        self._handlers: List[Callable[[Dict[str, Any]], None]] = []

    def add_handler(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        self._handlers.append(handler)

    def log(
        self,
        level: LogLevel,
        message: str,
        context: Optional[ObservabilityContext] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Core log entrypoint formatting and writing to storage and handlers."""
        if LEVEL_ORDER[level] < LEVEL_ORDER[self.min_level]:
            return {}

        ctx = context or get_current_context()
        record_dict = self.formatter.format(
            level.value,
            message,
            ctx,
            metadata,
            service_name=self.service_name,
        )

        entry = LogEntry(
            timestamp=record_dict["timestamp"],
            service=record_dict["service"],
            level=record_dict["level"],
            message=record_dict["message"],
            trace_id=record_dict["trace_id"],
            tenant_id=record_dict["tenant_id"],
            record_dict=record_dict,
        )
        self.storage.write(entry)

        for h in self._handlers:
            try:
                h(record_dict)
            except Exception:
                pass

        return record_dict

    def debug(self, message: str, context: Optional[ObservabilityContext] = None, **metadata: Any) -> Dict[str, Any]:
        return self.log(LogLevel.DEBUG, message, context, metadata)

    def info(self, message: str, context: Optional[ObservabilityContext] = None, **metadata: Any) -> Dict[str, Any]:
        return self.log(LogLevel.INFO, message, context, metadata)

    def warning(self, message: str, context: Optional[ObservabilityContext] = None, **metadata: Any) -> Dict[str, Any]:
        return self.log(LogLevel.WARNING, message, context, metadata)

    def error(self, message: str, context: Optional[ObservabilityContext] = None, **metadata: Any) -> Dict[str, Any]:
        return self.log(LogLevel.ERROR, message, context, metadata)

    def critical(self, message: str, context: Optional[ObservabilityContext] = None, **metadata: Any) -> Dict[str, Any]:
        return self.log(LogLevel.CRITICAL, message, context, metadata)
