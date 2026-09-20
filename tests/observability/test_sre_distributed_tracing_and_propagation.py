"""Tests for Tracing Engine, Span Scopes, and W3C Header Propagation."""

import pytest
from app.observability.tracing.propagation import TraceContextPropagator
from app.observability.tracing.spans import SpanContext, SpanKind, SpanStatus
from app.observability.tracing.tracer import SamplingStrategy, TracingEngine


def test_tracing_engine_span_hierarchy():
    tracer = TracingEngine(service_name="order-service")

    with tracer.start_as_current_span("root_operation") as root:
        root.set_attribute("tenant_id", "tenant-1")
        assert tracer.get_current_span() == root

        with tracer.start_as_current_span("child_operation") as child:
            assert child.parent_span_id == root.context.span_id
            assert child.context.trace_id == root.context.trace_id
            assert tracer.get_current_span() == child

        # After child exits, root is active again
        assert tracer.get_current_span() == root

    trace = tracer.get_trace(root.context.trace_id)
    assert len(trace) == 2
    assert root.status == SpanStatus.OK
    assert root.duration_ms >= 0


def test_w3c_trace_context_propagation():
    ctx = SpanContext(
        trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
        span_id="00f067aa0ba902b7",
        trace_flags="01",
    )
    headers = {}
    baggage = {"tenant": "acme", "user": "alice"}

    TraceContextPropagator.inject(ctx, headers, baggage=baggage)
    assert headers["traceparent"] == "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
    assert "baggage" in headers

    extracted = TraceContextPropagator.extract(headers)
    assert extracted is not None
    assert extracted.trace_id == ctx.trace_id
    assert extracted.span_id == ctx.span_id
    assert extracted.is_sampled is True

    ext_baggage = TraceContextPropagator.extract_baggage(headers)
    assert ext_baggage["tenant"] == "acme"
