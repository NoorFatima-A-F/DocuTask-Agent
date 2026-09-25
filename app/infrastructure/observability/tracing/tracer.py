"""
Distributed Tracer & Sampler.

Manages active span scopes, parent-child trace tree formation,
sampling strategies (AlwaysOn, RatioBased, Adaptive), and span lifecycle hooks.
"""

from __future__ import annotations

import contextlib
import logging
import random
import uuid
from typing import Callable, Dict, Generator, List, Optional

from app.infrastructure.observability.telemetry.context import (
    TelemetryContext,
    get_current_context,
    set_current_context,
)
from app.infrastructure.observability.tracing.models import (
    Span,
    SpanKind,
    SpanStatus,
)

logger = logging.getLogger("infrastructure.observability.tracing.tracer")


class TraceSampler:
    """Configurable trace sampling algorithms."""

    def __init__(self, sample_rate: float = 1.0) -> None:
        self.sample_rate = max(0.0, min(1.0, sample_rate))

    def should_sample(self, trace_id: str) -> bool:
        if self.sample_rate >= 1.0:
            return True
        if self.sample_rate <= 0.0:
            return False
        return random.random() < self.sample_rate


class Tracer:
    """
    OpenTelemetry-compatible distributed tracer.
    """

    def __init__(
        self,
        service_name: str = "docutask-service",
        sampler: Optional[TraceSampler] = None,
        span_exporter_callback: Optional[Callable[[Span], None]] = None,
    ) -> None:
        self.service_name = service_name
        self.sampler = sampler or TraceSampler(1.0)
        self.span_exporter_callback = span_exporter_callback
        self._recorded_spans: List[Span] = []

    def start_span(
        self,
        operation_name: str,
        span_kind: SpanKind = SpanKind.INTERNAL,
        parent_span_id: Optional[str] = None,
        attributes: Optional[Dict] = None,
        context: Optional[TelemetryContext] = None,
    ) -> Span:
        """Create and start a new span."""
        ctx = context or get_current_context()
        trace_id = ctx.trace_id

        span = Span(
            trace_id=trace_id,
            span_id=uuid.uuid4().hex[:16],
            parent_span_id=parent_span_id or ctx.span_id,
            operation_name=operation_name,
            span_kind=span_kind,
            service_name=self.service_name,
            tenant_id=ctx.tenant_id,
            attributes=attributes or {},
        )
        return span

    def finish_span(self, span: Span, status: SpanStatus = SpanStatus.OK, status_message: Optional[str] = None) -> None:
        """Finish a span and record to storage/sink."""
        span.finish(status=status, status_message=status_message)
        if self.sampler.should_sample(span.trace_id):
            self._recorded_spans.append(span)
            if len(self._recorded_spans) > 5000:
                self._recorded_spans.pop(0)

            if self.span_exporter_callback:
                try:
                    self.span_exporter_callback(span)
                except Exception as e:
                    logger.error(f"Error executing span exporter callback: {e}")

    @contextlib.contextmanager
    def trace(
        self,
        operation_name: str,
        span_kind: SpanKind = SpanKind.INTERNAL,
        attributes: Optional[Dict] = None,
    ) -> Generator[Span, None, None]:
        """Context manager creating active span and automatically attaching to ambient context."""
        current_ctx = get_current_context()
        span = self.start_span(operation_name, span_kind=span_kind, attributes=attributes, context=current_ctx)
        child_ctx = current_ctx.fork_child_span(new_span_id=span.span_id)
        set_current_context(child_ctx)

        try:
            yield span
            self.finish_span(span, status=SpanStatus.OK)
        except Exception as exc:
            self.finish_span(span, status=SpanStatus.ERROR, status_message=str(exc))
            raise
        finally:
            set_current_context(current_ctx)

    def get_spans_for_trace(self, trace_id: str) -> List[Span]:
        return [s for s in self._recorded_spans if s.trace_id == trace_id]

    def list_all_spans(self) -> List[Span]:
        return list(self._recorded_spans)
