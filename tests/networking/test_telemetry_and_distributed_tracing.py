"""Tests for Communication Telemetry, Golden Signals, and Distributed Tracing."""

import pytest
from app.networking.telemetry.logs import MeshAccessLogRecord, MeshAccessLogger
from app.networking.telemetry.metrics import MeshMetricsCollector
from app.networking.telemetry.traces import TraceContextPropagator


def test_mesh_metrics_golden_signals():
    collector = MeshMetricsCollector()

    # Record some latencies
    collector.record_call("svc-a", "svc-b", status_code=200, duration_ms=10.0)
    collector.record_call("svc-a", "svc-b", status_code=200, duration_ms=20.0)
    collector.record_call("svc-a", "svc-b", status_code=500, duration_ms=50.0)

    summary = collector.get_summary()
    assert summary.total_requests == 3
    assert summary.successful_requests == 2
    assert summary.failed_requests == 1
    assert summary.error_rate_pct == pytest.approx(33.33, rel=1e-2)
    assert summary.p50_latency_ms > 0


def test_w3c_trace_context_propagation():
    trace_id = TraceContextPropagator.generate_trace_id()
    span_id = TraceContextPropagator.generate_span_id()
    headers = {}

    TraceContextPropagator.inject_w3c_headers(trace_id, span_id, headers)
    assert "traceparent" in headers
    assert "x-b3-traceid" in headers

    ext_trace, ext_span, sampled = TraceContextPropagator.extract_context(headers)
    assert ext_trace == trace_id
    assert ext_span == span_id
    assert sampled is True


def test_mesh_access_logger():
    logger = MeshAccessLogger()
    record = MeshAccessLogRecord(
        timestamp=1000.0,
        request_id="req-123",
        trace_id="trace-abc",
        source_service="client",
        target_service="api",
        method="POST",
        path="/v1/documents",
        status_code=200,
        duration_ms=12.5,
    )
    logger.log_access(record)

    logs = logger.query_logs(service_name="api")
    assert len(logs) == 1
    assert logs[0].request_id == "req-123"
