"""
Structured JSON Logging Framework.
Contextual log emission with async ContextVars for trace_id, request_id, org_id, workflow_id, agent_id.
"""

from contextvars import ContextVar
from datetime import datetime, timezone
import json
import logging
import sys
from typing import Any, Dict, Optional

# Context Variables for Request & Distributed Tracing Scope
ctx_request_id: ContextVar[Optional[str]] = ContextVar("ctx_request_id", default=None)
ctx_trace_id: ContextVar[Optional[str]] = ContextVar("ctx_trace_id", default=None)
ctx_org_id: ContextVar[Optional[str]] = ContextVar("ctx_org_id", default=None)
ctx_workflow_id: ContextVar[Optional[str]] = ContextVar("ctx_workflow_id", default=None)
ctx_agent_id: ContextVar[Optional[str]] = ContextVar("ctx_agent_id", default=None)


class StructuredJsonFormatter(logging.Formatter):
    """Formats log records as strict JSON envelopes."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "time": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": ctx_request_id.get(),
            "trace_id": ctx_trace_id.get(),
            "organization_id": ctx_org_id.get(),
            "workflow_id": ctx_workflow_id.get(),
            "agent_id": ctx_agent_id.get(),
        }

        # Include custom extra metadata if present
        if hasattr(record, "metadata") and isinstance(record.metadata, dict):
            log_obj["metadata"] = record.metadata
        elif hasattr(record, "extra") and isinstance(record.extra, dict):
            log_obj["metadata"] = record.extra

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj)


class PlatformLogger:
    """Platform wrapper for emitting structured log entries."""

    def __init__(self, name: str = "docutask.platform"):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(StructuredJsonFormatter())
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
            self.logger.propagate = False

    def info(self, message: str, **kwargs) -> None:
        self.logger.info(message, extra={"metadata": kwargs} if kwargs else None)

    def warning(self, message: str, **kwargs) -> None:
        self.logger.warning(message, extra={"metadata": kwargs} if kwargs else None)

    def error(self, message: str, **kwargs) -> None:
        self.logger.error(message, extra={"metadata": kwargs} if kwargs else None)

    def debug(self, message: str, **kwargs) -> None:
        self.logger.debug(message, extra={"metadata": kwargs} if kwargs else None)
