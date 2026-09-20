"""
Tests for Platform Observability (Logging, Metrics, Tracing, Health, Diagnostics).
"""

import pytest
import asyncio
from app.observability.metrics.metrics import MetricsRegistry
from app.observability.tracing.tracer import Tracer
from app.observability.health.manager import HealthManager
from app.observability.health.models import HealthLevel, HealthStatus
from app.platform.diagnostics.reporter import DiagnosticsReporter


def test_metrics_registry():
    metrics = MetricsRegistry()
    counter = metrics.counter("test_requests_total")
    counter.inc(1.0, labels={"env": "prod"})
    counter.inc(2.0, labels={"env": "prod"})

    assert counter.get_value(labels={"env": "prod"}) == 3.0

    gauge = metrics.gauge("test_active_workers")
    gauge.set(10.0)
    gauge.inc(2.0)
    gauge.dec(1.0)
    assert gauge.get_value() == 11.0

    timer = metrics.timer("test_duration_ms")
    with timer:
        pass  # instantaneous block
    assert metrics.histogram("test_duration_ms").get_count() == 1


def test_distributed_tracing():
    tracer = Tracer(service_name="test-service")
    with tracer.start_span("root_workflow") as root_span:
        root_span.set_attribute("tenant_id", "tenant-123")
        with tracer.start_span("child_agent_task") as child_span:
            child_span.add_event("tool_called", {"tool": "ocr_extract"})
            assert child_span.parent_span_id == root_span.span_id
            assert child_span.trace_id == root_span.trace_id

    finished = tracer.get_finished_spans()
    assert len(finished) == 2


def test_health_manager():
    hm = HealthManager()
    hm.set_ready(True)
    report = asyncio.run(hm.check_health())

    assert report.status == HealthStatus.HEALTHY
    assert report.ready is True
    assert "database" in report.checks


def test_diagnostics_reporter():
    reporter = DiagnosticsReporter()
    rep = asyncio.run(reporter.generate_report())

    assert rep.platform_version == "2.0.0"
    assert rep.status == "HEALTHY"
    assert "database" in rep.infrastructure_status
