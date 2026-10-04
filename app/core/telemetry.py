"""
app/core/telemetry.py
Enterprise OpenTelemetry & Structured Logging Pipeline for AI Pipelines.
"""

from __future__ import annotations
import json
import logging
import time
import uuid
from contextvars import ContextVar
from typing import Any, Dict, Optional

# Thread-safe / Coroutine-safe Context Variable for Request & Agent Tracing
request_trace_id: ContextVar[str] = ContextVar("request_trace_id", default="system")


class StructuredJsonFormatter(logging.Formatter):
    """Formats log records as newline-delimited enterprise JSON logs."""

    def format(self, record: logging.LogRecord) -> str:
        log_payload: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": request_trace_id.get(),
            "module": record.module,
            "line": record.lineno,
        }
        if hasattr(record, "metrics"):
            log_payload["metrics"] = record.metrics
        return json.dumps(log_payload)


def setup_telemetry(log_level: int = logging.INFO) -> logging.Logger:
    """Configures structured telemetry logger for the platform."""
    logger_instance = logging.getLogger("docutask")
    logger_instance.setLevel(log_level)

    # Avoid duplicate handlers if re-initialized
    if not logger_instance.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredJsonFormatter())
        logger_instance.addHandler(handler)

    return logger_instance


logger = setup_telemetry()


class AgentSpan:
    """Context manager for measuring agent execution latency, tokens, and errors."""

    def __init__(self, operation_name: str, span_metadata: Optional[Dict[str, Any]] = None):
        self.operation_name = operation_name
        self.metadata = span_metadata or {}
        self.start_time: float = 0.0

    def __enter__(self) -> AgentSpan:
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        duration_ms = (time.perf_counter() - self.start_time) * 1000.0
        status = "ERROR" if exc_type else "SUCCESS"
        metrics = {
            "operation": self.operation_name,
            "duration_ms": round(duration_ms, 2),
            "status": status,
            **self.metadata,
        }
        if exc_type:
            logger.error(
                f"Agent operation {self.operation_name} failed: {exc_val}",
                extra={"metrics": metrics},
            )
        else:
            logger.info(
                f"Agent operation {self.operation_name} completed",
                extra={"metrics": metrics},
            )


def get_current_trace_id() -> str:
    """Get the active request trace ID or generate a new one if unset."""
    current = request_trace_id.get()
    if current == "system":
        new_id = f"trace-{uuid.uuid4().hex[:12]}"
        request_trace_id.set(new_id)
        return new_id
    return current


def set_trace_id(trace_id: str) -> None:
    """Explicitly assign a trace ID to the active async context."""
    request_trace_id.set(trace_id)
