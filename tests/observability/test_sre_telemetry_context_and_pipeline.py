"""Tests for ObservabilityContext and TelemetryPipeline."""

from app.observability.core.context import (
    ObservabilityContext,
)
from app.observability.core.events import EventCategory, EventStream, PlatformEvent
from app.observability.core.telemetry import (
    InMemoryTelemetryExporter,
    TelemetryPipeline,
    TelemetryRecord,
    TelemetryType,
)


def test_observability_context_fork_and_dict():
    ctx = ObservabilityContext(
        tenant_id="tenant-123",
        service_name="ocr-service",
        workflow_id="wf-99",
        agent_id="agent-01",
    )
    d = ctx.to_dict()
    assert d["tenant_id"] == "tenant-123"
    assert d["service_name"] == "ocr-service"
    assert d["workflow_id"] == "wf-99"

    # Fork child span context
    child = ctx.fork_span(new_service="db-service")
    assert child.trace_id == ctx.trace_id
    assert child.span_id != ctx.span_id
    assert child.service_name == "db-service"
    assert child.tenant_id == "tenant-123"


def test_telemetry_pipeline_batch_and_export():
    pipeline = TelemetryPipeline(buffer_size=100, batch_size=2)
    exporter = InMemoryTelemetryExporter()
    pipeline.add_exporter(exporter)

    rec1 = TelemetryRecord(telemetry_type=TelemetryType.METRIC, payload={"cpu": 45.0})
    rec2 = TelemetryRecord(telemetry_type=TelemetryType.LOG, payload={"msg": "hello"})

    pipeline.ingest(rec1)
    assert len(exporter.records) == 0  # not flushed yet (batch_size=2)

    pipeline.ingest(rec2)
    assert len(exporter.records) == 2  # automatically flushed

    metric_recs = exporter.get_by_type(TelemetryType.METRIC)
    assert len(metric_recs) == 1
    assert metric_recs[0].payload["cpu"] == 45.0


def test_event_stream_publish_and_subscribe():
    stream = EventStream()
    received = []

    def handler(evt: PlatformEvent):
        received.append(evt)

    stream.subscribe("agent.*", handler)

    # Matching event
    stream.publish(
        PlatformEvent(
            name="agent.tool_called",
            category=EventCategory.AGENT,
            payload={"tool": "search"},
        )
    )
    assert len(received) == 1

    # Non-matching event
    stream.publish(
        PlatformEvent(
            name="infra.cpu_spike",
            category=EventCategory.INFRASTRUCTURE,
        )
    )
    assert len(received) == 1  # unchanged
