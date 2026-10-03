"""
Log Ingestion Pipeline.

Processes structured log streams with high-throughput buffering, schema normalization,
and indexing integration.
"""

from __future__ import annotations

import logging
from typing import Callable, Dict, List, Optional
from app.infrastructure.observability.logs.models import LogLevel, LogRecord
from app.infrastructure.observability.telemetry.context import TelemetryContext, get_current_context

logger = logging.getLogger("infrastructure.observability.logs.ingestion")


class LogIngestionPipeline:
    """
    High-throughput ingestion buffer for structured platform logs.
    """

    def __init__(self, sink_callback: Optional[Callable[[List[LogRecord]], None]] = None) -> None:
        self.sink_callback = sink_callback
        self._buffer: List[LogRecord] = []

    def emit(
        self,
        level: LogLevel,
        message: str,
        exception: Optional[Exception] = None,
        stack_trace: Optional[str] = None,
        context: Optional[TelemetryContext] = None,
        attributes: Optional[Dict] = None,
    ) -> LogRecord:
        """Create and buffer a structured log record."""
        ctx = context or get_current_context()

        attrs = attributes or {}
        record = LogRecord(
            level=level,
            message=message,
            service_name=attrs.get("service_name", ctx.service_name),
            service_version=attrs.get("service_version", ctx.service_version),
            environment=attrs.get("environment", ctx.environment),
            region=attrs.get("region", ctx.region),
            cluster=attrs.get("cluster", ctx.cluster),
            tenant_id=attrs.get("tenant_id", ctx.tenant_id),
            trace_id=attrs.get("trace_id", ctx.trace_id),
            span_id=attrs.get("span_id", ctx.span_id),
            correlation_id=attrs.get("correlation_id", ctx.correlation_id),
            request_id=attrs.get("request_id", ctx.request_id),
            workflow_id=attrs.get("workflow_id", ctx.workflow_id),
            agent_id=attrs.get("agent_id", ctx.agent_id),
            user_id=attrs.get("user_id", ctx.user_id),
            exception=str(exception) if exception else None,
            stack_trace=stack_trace,
            attributes=attrs,
        )

        self._buffer.append(record)
        if self.sink_callback and len(self._buffer) >= 50:
            self.flush()

        return record

    def flush(self) -> List[LogRecord]:
        """Flush buffered log records to the configured storage sink."""
        records = list(self._buffer)
        self._buffer.clear()
        if self.sink_callback and records:
            try:
                self.sink_callback(records)
            except Exception as e:
                logger.error(f"Error executing log sink callback: {e}")
        return records
