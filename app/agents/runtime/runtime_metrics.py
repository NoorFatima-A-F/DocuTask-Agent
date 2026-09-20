"""
Runtime Metrics Collector & OpenTelemetry Distributed Spans.
Collects telemetry, startup/shutdown timings, active sessions, CPU/memory, and provides OpenTelemetry span managers.
"""

import time
from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncIterator, Dict, Iterator, List, Optional
from pydantic import BaseModel, Field


class RuntimeMetricsSnapshot(BaseModel):
    """Snapshot of platform runtime telemetry and performance counters."""
    boot_duration_ms: float = 0.0
    shutdown_duration_ms: float = 0.0
    registered_services_count: int = 0
    active_sessions: int = 0
    total_sessions: int = 0
    total_sessions_created: int = 0
    startup_time_ms: float = 0.0
    shutdown_time_ms: float = 0.0
    failed_workflows: int = 0
    restart_count: int = 0
    plugin_count: int = 0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    average_latency_ms: float = 0.0
    token_usage: int = 0
    uptime_seconds: float = 0.0
    availability_ratio: float = 1.0


class RuntimeSpan:
    """Represents an active OpenTelemetry distributed trace span."""

    def __init__(self, name: str, trace_id: str, span_id: str, parent_span_id: Optional[str] = None) -> None:
        self.name = name
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_span_id = parent_span_id
        self.start_time = time.perf_counter()
        self.end_time: Optional[float] = None
        self.attributes: Dict[str, Any] = {}
        self.status: str = "OK"

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def set_status(self, status: str) -> None:
        self.status = status

    def finish(self) -> float:
        self.end_time = time.perf_counter()
        return (self.end_time - self.start_time) * 1000.0


class RuntimeTracer:
    """Manages distributed spans across Boot, Workflow, Agent, Tool, Reflection, and Recovery."""

    def __init__(self) -> None:
        self._completed_spans: List[RuntimeSpan] = []

    @asynccontextmanager
    async def start_span(
        self,
        name: str,
        trace_id: str = "default_trace",
        span_id: str = "default_span",
        parent_span_id: Optional[str] = None,
    ) -> AsyncIterator[RuntimeSpan]:
        """Async context manager creating and recording a distributed span."""
        span = RuntimeSpan(name, trace_id, span_id, parent_span_id)
        try:
            yield span
        except Exception as e:
            span.set_status(f"ERROR: {e}")
            raise
        finally:
            span.finish()
            self._completed_spans.append(span)

    def get_completed_spans(self) -> List[RuntimeSpan]:
        return list(self._completed_spans)


class RuntimeMetricsCollector:
    """In-memory collector for runtime kernel metrics with GCP Cloud Monitoring export."""

    def __init__(self) -> None:
        self._metrics = RuntimeMetricsSnapshot()
        self._start_time: float = time.time()
        self.tracer = RuntimeTracer()

    def record_startup_time(self, duration_ms: float) -> None:
        self._metrics.boot_duration_ms = duration_ms
        self._metrics.startup_time_ms = duration_ms

    def record_shutdown_time(self, duration_ms: float) -> None:
        self._metrics.shutdown_duration_ms = duration_ms
        self._metrics.shutdown_time_ms = duration_ms

    def set_registered_services(self, count: int) -> None:
        self._metrics.registered_services_count = count

    def set_loaded_plugins(self, count: int) -> None:
        self._metrics.plugin_count = count

    def record_session_started(self) -> None:
        self._metrics.total_sessions += 1
        self._metrics.total_sessions_created += 1
        self._metrics.active_sessions += 1

    def record_session_closed(self) -> None:
        self._metrics.active_sessions = max(0, self._metrics.active_sessions - 1)

    def record_restart_triggered(self) -> None:
        self._metrics.restart_count += 1

    def record_failed_workflow(self) -> None:
        self._metrics.failed_workflows += 1

    def record_token_consumption(self, tokens: int) -> None:
        self._metrics.token_usage += tokens

    def update_resource_usage(self, memory_mb: float, cpu_percent: float) -> None:
        self._metrics.memory_usage_mb = memory_mb
        self._metrics.cpu_usage_percent = cpu_percent

    def get_snapshot(self) -> RuntimeMetricsSnapshot:
        snapshot = self._metrics.model_copy()
        snapshot.uptime_seconds = time.time() - self._start_time
        return snapshot

    def export_gcp_metrics(self) -> List[Dict[str, Any]]:
        """Formats metrics for Google Cloud Monitoring custom metric time series."""
        snapshot = self.get_snapshot()
        return [
            {
                "metric": {"type": f"custom.googleapis.com/platform_runtime/{k}"},
                "resource": {"type": "global"},
                "points": [{"value": {"doubleValue": float(v)}}],
            }
            for k, v in snapshot.model_dump().items()
        ]
