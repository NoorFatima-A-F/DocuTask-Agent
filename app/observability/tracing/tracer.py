"""Distributed Tracing Engine and OpenTelemetry-Compatible Scope Manager."""

from __future__ import annotations

import contextlib
import random
import threading
import time
import uuid
from enum import Enum
from typing import Any, Dict, Generator, List, Optional

from .spans import Span, SpanContext, SpanKind, SpanStatus


class SamplingStrategy(str, Enum):
    ALWAYS_ON = "ALWAYS_ON"
    ALWAYS_OFF = "ALWAYS_OFF"
    RATIO_BASED = "RATIO_BASED"
    ERROR_ONLY = "ERROR_ONLY"
    ADAPTIVE = "ADAPTIVE"


class TracingEngine:
    """Enterprise distributed tracing engine managing trace scopes and sampling."""

    def __init__(
        self,
        service_name: str = "docutask-service",
        sampling_strategy: SamplingStrategy = SamplingStrategy.ALWAYS_ON,
        sampling_ratio: float = 1.0,
    ):
        self.service_name = service_name
        self.sampling_strategy = sampling_strategy
        self.sampling_ratio = sampling_ratio
        # trace_id -> list of Spans
        self._traces: Dict[str, List[Span]] = {}
        self._active_spans = threading.local()
        self._lock = threading.Lock()

    def _should_sample(self) -> bool:
        if self.sampling_strategy == SamplingStrategy.ALWAYS_ON:
            return True
        elif self.sampling_strategy == SamplingStrategy.ALWAYS_OFF:
            return False
        elif self.sampling_strategy == SamplingStrategy.RATIO_BASED:
            return random.random() <= self.sampling_ratio
        return True

    def get_current_span(self) -> Optional[Span]:
        stack = getattr(self._active_spans, "stack", None)
        if stack:
            return stack[-1]
        return None

    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        parent_context: Optional[SpanContext] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Span:
        """Start a new span within the current or specified trace context."""
        sampled = self._should_sample()
        current_span = self.get_current_span()

        if parent_context:
            trace_id = parent_context.trace_id
            parent_span_id = parent_context.span_id
        elif current_span:
            trace_id = current_span.context.trace_id
            parent_span_id = current_span.context.span_id
        else:
            trace_id = uuid.uuid4().hex
            parent_span_id = None

        span_id = uuid.uuid4().hex[:16]
        ctx = SpanContext(
            trace_id=trace_id,
            span_id=span_id,
            trace_flags="01" if sampled else "00",
            is_sampled=sampled,
        )

        span_attrs = {"service.name": self.service_name}
        if attributes:
            span_attrs.update(attributes)

        span = Span(
            name=name,
            context=ctx,
            parent_span_id=parent_span_id,
            kind=kind,
            attributes=span_attrs,
        )

        with self._lock:
            if trace_id not in self._traces:
                self._traces[trace_id] = []
            self._traces[trace_id].append(span)

        return span

    @contextlib.contextmanager
    def start_as_current_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        parent_context: Optional[SpanContext] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[Span, None, None]:
        """Context manager to start a span and push it onto the active span stack."""
        span = self.start_span(name, kind=kind, parent_context=parent_context, attributes=attributes)
        if not hasattr(self._active_spans, "stack"):
            self._active_spans.stack = []
        self._active_spans.stack.append(span)

        try:
            yield span
        except Exception as ex:
            span.record_exception(ex)
            raise
        finally:
            span.finish()
            if self._active_spans.stack:
                self._active_spans.stack.pop()

    def get_trace(self, trace_id: str) -> List[Span]:
        """Retrieve all spans belonging to a trace ID."""
        with self._lock:
            return list(self._traces.get(trace_id, []))

    def clear(self) -> None:
        with self._lock:
            self._traces.clear()
