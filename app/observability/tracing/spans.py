"""OpenTelemetry-Compatible Span and SpanContext Data Models."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class SpanStatus(str, Enum):
    UNSET = "UNSET"
    OK = "OK"
    ERROR = "ERROR"


class SpanKind(str, Enum):
    INTERNAL = "INTERNAL"
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"


@dataclass
class SpanEvent:
    name: str
    timestamp: float = field(default_factory=time.time)
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SpanContext:
    trace_id: str
    span_id: str
    trace_flags: str = "01"
    trace_state: str = ""
    is_sampled: bool = True


@dataclass
class Span:
    name: str
    context: SpanContext
    parent_span_id: Optional[str] = None
    kind: SpanKind = SpanKind.INTERNAL
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: SpanStatus = SpanStatus.UNSET
    status_description: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[SpanEvent] = field(default_factory=list)
    error_message: Optional[str] = None

    @property
    def span_id(self) -> str:
        return self.context.span_id

    @property
    def trace_id(self) -> str:
        return self.context.trace_id

    def __enter__(self) -> Span:
        tracer = getattr(self, "_tracer", None)
        if tracer:
            if not hasattr(tracer._active_spans, "stack"):
                tracer._active_spans.stack = []
            tracer._active_spans.stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_val:
            self.record_exception(exc_val)
        self.finish()
        tracer = getattr(self, "_tracer", None)
        if tracer and getattr(tracer._active_spans, "stack", None):
            if tracer._active_spans.stack and tracer._active_spans.stack[-1] is self:
                tracer._active_spans.stack.pop()

    @property
    def duration_seconds(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    @property
    def duration_ms(self) -> float:
        return self.duration_seconds * 1000.0

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        self.events.append(SpanEvent(name=name, attributes=attributes or {}))

    def set_status(self, status: SpanStatus, description: str = "") -> None:
        self.status = status
        self.status_description = description

    def record_exception(self, exception: Exception) -> None:
        self.status = SpanStatus.ERROR
        self.error_message = str(exception)
        self.add_event(
            "exception",
            {
                "exception.type": type(exception).__name__,
                "exception.message": str(exception),
            },
        )

    def finish(self, status: Optional[SpanStatus] = None) -> None:
        self.end_time = time.time()
        if status:
            self.status = status
        elif self.status == SpanStatus.UNSET:
            self.status = SpanStatus.OK
