"""
Tests for Unified Telemetry Context, Sensitive Data Redaction, and Pipeline Exporters.
"""

import pytest

from app.infrastructure.observability.telemetry.context import (
    TelemetryContext,
    get_current_context,
    mask_sensitive_data,
    set_current_context,
)
from app.infrastructure.observability.telemetry.exporters import (
    InMemoryExporter,
    OTLPJsonExporter,
    TelemetryBatch,
)
from app.infrastructure.observability.telemetry.collector import (
    TelemetryCollectorPipeline,
)
from app.infrastructure.observability.telemetry.sdk import (
    TelemetrySDK,
)


def test_telemetry_context_fork_and_headers():
    parent_ctx = TelemetryContext(
        trace_id="0123456789abcdef0123456789abcdef",
        span_id="1111222233334444",
        tenant_id="tenant-alpha",
        service_name="api-gateway",
        region="us-east-1",
    )

    child_ctx = parent_ctx.fork_child_span(new_span_id="5555666677778888")
    assert child_ctx.trace_id == parent_ctx.trace_id
    assert child_ctx.parent_span_id == parent_ctx.span_id
    assert child_ctx.span_id == "5555666677778888"
    assert child_ctx.tenant_id == "tenant-alpha"

    headers = child_ctx.to_header_dict()
    assert headers["x-trace-id"] == parent_ctx.trace_id
    assert headers["x-span-id"] == "5555666677778888"
    assert headers["x-parent-span-id"] == "1111222233334444"

    hydrated = TelemetryContext.from_header_dict(headers)
    assert hydrated.trace_id == parent_ctx.trace_id
    assert hydrated.span_id == "5555666677778888"
    assert hydrated.parent_span_id == "1111222233334444"


def test_sensitive_data_masking():
    raw_api_key = "Authorization: api_key='sk-live-1234567890abcdef'"
    masked = mask_sensitive_data(raw_api_key)
    assert "sk-live" not in masked
    assert "***REDACTED***" in masked

    raw_email = "Contact user at alice.smith@example.com for support"
    masked_email = mask_sensitive_data(raw_email)
    assert "alice.smith" not in masked_email
    assert "***@***.***" in masked_email


def test_telemetry_collector_and_exporters():
    in_memory = InMemoryExporter()
    otlp = OTLPJsonExporter()
    pipeline = TelemetryCollectorPipeline(batch_size=5, default_exporter=in_memory)
    pipeline.add_exporter(otlp)

    pipeline.record_metric({"name": "test_counter", "value": 1.0})
    pipeline.record_log({"level": "INFO", "message": "User user@test.com logged in with bearer='xyz123'"})
    pipeline.record_trace({"operation_name": "process_doc", "duration_ms": 45.2})
    pipeline.record_event({"event_name": "cluster_scaled", "nodes": 8})

    batch = pipeline.flush()
    assert len(batch.metrics) == 1
    assert len(batch.logs) == 1
    assert len(batch.traces) == 1
    assert len(batch.events) == 1

    assert len(in_memory.metrics) == 1
    assert len(otlp.exported_payloads) == 1
    # Check that PII was masked in log record
    assert "user@test.com" not in in_memory.logs[0]["message"]


def test_telemetry_sdk_instrumentation():
    in_memory = InMemoryExporter()
    pipeline = TelemetryCollectorPipeline(batch_size=10, default_exporter=in_memory)
    sdk = TelemetrySDK(pipeline)

    sdk.counter("requests_total", 1.0, tags={"route": "/api/v1/ocr"})
    sdk.gauge("memory_usage_mb", 512.0)
    sdk.histogram("request_latency_ms", 12.5)
    sdk.log("INFO", "Processed batch document", doc_id="doc-99")
    sdk.event("document_classified", {"classification": "invoice"})

    with sdk.span("ocr_pipeline", attributes={"engine": "tesseract"}) as span_ctx:
        assert span_ctx.span_id is not None

    pipeline.flush()
    assert len(in_memory.metrics) == 3
    assert len(in_memory.logs) == 1
    assert len(in_memory.events) == 1
    assert len(in_memory.traces) == 1
    assert in_memory.traces[0]["operation_name"] == "ocr_pipeline"
