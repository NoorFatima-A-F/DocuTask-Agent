"""
Unified Telemetry Developer SDK.

Provides high-level developer primitives for instrumenting metrics, logs,
traces, events, and profiling with minimal overhead.
"""

from __future__ import annotations

import contextlib
import time
from typing import Any, Dict, Generator, Optional

from app.infrastructure.observability.telemetry.collector import TelemetryCollectorPipeline
from app.infrastructure.observability.telemetry.context import (
    TelemetryContext,
    get_current_context,
    set_current_context,
)


class TelemetrySDK:
    """
    Developer-friendly facade for publishing telemetry signals.
    """

    def __init__(self, pipeline: Optional[TelemetryCollectorPipeline] = None) -> None:
        self.pipeline = pipeline or TelemetryCollectorPipeline()

    def counter(self, name: str, value: float = 1.0, tags: Optional[Dict[str, str]] = None) -> None:
        """Record an increment to a monotonic or non-monotonic counter."""
        self.pipeline.record_metric({
            "type": "COUNTER",
            "name": name,
            "value": value,
            "tags": tags or {},
        })

    def gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Record an instantaneous gauge reading."""
        self.pipeline.record_metric({
            "type": "GAUGE",
            "name": name,
            "value": value,
            "tags": tags or {},
        })

    def histogram(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a histogram sample value (e.g. latency in ms, payload size in bytes)."""
        self.pipeline.record_metric({
            "type": "HISTOGRAM",
            "name": name,
            "value": value,
            "tags": tags or {},
        })

    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """Emit a structured log message with ambient correlation context."""
        self.pipeline.record_log({
            "level": level.upper(),
            "message": message,
            "attributes": kwargs,
        })

    def event(self, name: str, payload: Optional[Dict[str, Any]] = None, severity: str = "INFO") -> None:
        """Emit a lifecycle or operational event."""
        self.pipeline.record_event({
            "event_name": name,
            "severity": severity.upper(),
            "payload": payload or {},
        })

    @contextlib.contextmanager
    def span(self, operation_name: str, attributes: Optional[Dict[str, Any]] = None) -> Generator[TelemetryContext, None, None]:
        """Context manager wrapping a code block in an active distributed trace span."""
        parent_ctx = get_current_context()
        child_ctx = parent_ctx.fork_child_span()
        set_current_context(child_ctx)
        start_time = time.time()
        error: Optional[str] = None
        status = "OK"

        try:
            yield child_ctx
        except Exception as e:
            status = "ERROR"
            error = str(e)
            raise
        finally:
            duration_ms = (time.time() - start_time) * 1000
            self.pipeline.record_trace({
                "operation_name": operation_name,
                "duration_ms": duration_ms,
                "status": status,
                "error": error,
                "attributes": {**(attributes or {}), **child_ctx.attributes},
            }, context=child_ctx)
            set_current_context(parent_ctx)
