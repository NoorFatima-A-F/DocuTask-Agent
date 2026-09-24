"""
Tests for Distributed Tracing, W3C/B3 Context Propagation, and Trace Tree Analysis.
"""

import time

from app.infrastructure.observability.tracing.models import (
    Span,
    SpanStatus,
)
from app.infrastructure.observability.tracing.propagation import (
    TraceContextPropagator,
)
from app.infrastructure.observability.tracing.tracer import (
    Tracer,
)
from app.infrastructure.observability.tracing.spans import (
    TraceTreeAnalyzer,
)


def test_w3c_and_b3_propagation():
    trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"
    span_id = "00f067aa0ba902b7"

    # W3C
    w3c_headers = TraceContextPropagator.inject_w3c(trace_id, span_id, sampled=True)
    assert "traceparent" in w3c_headers
    assert w3c_headers["traceparent"] == f"00-{trace_id}-{span_id}-01"

    ext_t, ext_s, sampled = TraceContextPropagator.extract_w3c(w3c_headers)
    assert ext_t == trace_id
    assert ext_s == span_id
    assert sampled is True

    # B3
    b3_headers = TraceContextPropagator.inject_b3(trace_id, span_id, sampled=True)
    assert b3_headers["x-b3-traceid"] == trace_id
    b3_t, b3_s, _, b3_sampled = TraceContextPropagator.extract_b3(b3_headers)
    assert b3_t == trace_id
    assert b3_s == span_id
    assert b3_sampled is True


def test_tracer_nested_spans():
    tracer = Tracer(service_name="workflow-engine")

    with tracer.trace("root_workflow") as root_span:
        root_span.set_attribute("workflow_id", "wf-100")
        time.sleep(0.01)

        with tracer.trace("fetch_knowledge") as child_span:
            child_span.add_event("cache_miss")
            time.sleep(0.01)

    spans = tracer.list_all_spans()
    assert len(spans) == 2
    root = next(s for s in spans if s.operation_name == "root_workflow")
    child = next(s for s in spans if s.operation_name == "fetch_knowledge")

    assert child.parent_span_id == root.span_id
    assert root.duration_ms > 0
    assert child.duration_ms > 0
    assert len(child.events) == 1


def test_trace_tree_analyzer_and_critical_path():
    spans = [
        Span(
            trace_id="tr-abc",
            span_id="span-root",
            parent_span_id=None,
            operation_name="gateway_request",
            service_name="api-gateway",
            start_time=100.0,
            end_time=100.1,
            duration_ms=100.0,
            status=SpanStatus.OK,
        ),
        Span(
            trace_id="tr-abc",
            span_id="span-agent",
            parent_span_id="span-root",
            operation_name="agent_planning",
            service_name="agent-runtime",
            start_time=100.01,
            end_time=100.08,
            duration_ms=70.0,
            status=SpanStatus.OK,
        ),
        Span(
            trace_id="tr-abc",
            span_id="span-llm",
            parent_span_id="span-agent",
            operation_name="model_inference",
            service_name="model-gateway",
            start_time=100.02,
            end_time=100.07,
            duration_ms=50.0,
            status=SpanStatus.OK,
        ),
    ]

    report = TraceTreeAnalyzer.analyze_trace(spans)
    assert report is not None
    assert report.trace_id == "tr-abc"
    assert report.total_spans == 3
    assert report.root_service == "api-gateway"
    assert "agent-runtime" in report.services_involved
    assert "model-gateway" in report.services_involved
    assert len(report.critical_path) == 3
    assert report.critical_path[0] == "api-gateway:gateway_request"
