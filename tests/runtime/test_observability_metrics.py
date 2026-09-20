"""
Enterprise Observability & Distributed Metrics Test Suite.
Validates:
- OpenTelemetry distributed span creation, attributes, and duration tracking
- RuntimeTracer context manager behavior on success and exception
- RuntimeMetricsCollector snapshot recording and counters
"""

import pytest
from app.agents.runtime.runtime_metrics import (
    RuntimeMetricsCollector,
    RuntimeSpan,
    RuntimeTracer,
)


@pytest.mark.asyncio
async def test_runtime_span_and_tracer_success():
    tracer = RuntimeTracer()

    async with tracer.start_span(
        name="execute_planner_graph",
        trace_id="trace-abc",
        span_id="span-123",
    ) as span:
        span.set_attribute("tenant_id", "tenant-alpha")
        span.set_attribute("node_count", 15)

    spans = tracer.get_completed_spans()
    assert len(spans) == 1
    s = spans[0]
    assert s.name == "execute_planner_graph"
    assert s.trace_id == "trace-abc"
    assert s.span_id == "span-123"
    assert s.status == "OK"
    assert s.attributes["tenant_id"] == "tenant-alpha"
    assert s.attributes["node_count"] == 15
    assert s.end_time is not None
    assert (s.end_time - s.start_time) >= 0


@pytest.mark.asyncio
async def test_runtime_tracer_error_handling():
    tracer = RuntimeTracer()

    with pytest.raises(RuntimeError):
        async with tracer.start_span("failing_tool_call") as span:
            span.set_attribute("tool", "ocr")
            raise RuntimeError("OCR service unavailable")

    spans = tracer.get_completed_spans()
    assert len(spans) == 1
    assert "ERROR: OCR service unavailable" in spans[0].status


def test_runtime_metrics_collector_snapshot():
    collector = RuntimeMetricsCollector()

    collector.record_startup_time(125.5)
    collector.record_shutdown_time(45.2)
    collector.set_registered_services(8)
    collector.record_session_started()

    snap = collector.get_snapshot()
    assert snap.startup_time_ms == 125.5
    assert snap.boot_duration_ms == 125.5
    assert snap.shutdown_time_ms == 45.2
    assert snap.registered_services_count == 8
    assert snap.total_sessions_created == 1
    assert snap.active_sessions == 1
    assert snap.uptime_seconds >= 0.0

    collector.record_session_closed()
    snap2 = collector.get_snapshot()
    assert snap2.active_sessions == 0
