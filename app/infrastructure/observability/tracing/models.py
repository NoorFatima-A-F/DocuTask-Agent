"""
Distributed Tracing Models & OpenTelemetry Alignment.

Defines OpenTelemetry-compatible Span, SpanKind, SpanStatus, SpanEvent, and SpanLink models.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SpanKind(str, enum.Enum):
    """OpenTelemetry span kind classifications."""
    INTERNAL = "INTERNAL"
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"


class SpanStatus(str, enum.Enum):
    """Execution outcome status of a span."""
    UNSET = "UNSET"
    OK = "OK"
    ERROR = "ERROR"


class SpanEvent(BaseModel):
    """Timestamped event annotation within a span."""
    name: str
    timestamp: float = Field(default_factory=lambda: datetime.now(timezone.utc).timestamp())
    attributes: Dict[str, Any] = Field(default_factory=dict)


class SpanLink(BaseModel):
    """Cross-trace causal link."""
    trace_id: str
    span_id: str
    attributes: Dict[str, Any] = Field(default_factory=dict)


class Span(BaseModel):
    """OpenTelemetry-compatible distributed trace span."""
    trace_id: str
    span_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    parent_span_id: Optional[str] = None
    operation_name: str
    span_kind: SpanKind = SpanKind.INTERNAL
    start_time: float = Field(default_factory=lambda: datetime.now(timezone.utc).timestamp())
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    status: SpanStatus = SpanStatus.UNSET
    status_message: Optional[str] = None
    service_name: str = "docutask-service"
    service_version: str = "3.1.0"
    tenant_id: str = "global"
    attributes: Dict[str, Any] = Field(default_factory=dict)
    events: List[SpanEvent] = Field(default_factory=list)
    links: List[SpanLink] = Field(default_factory=list)

    def finish(self, status: SpanStatus = SpanStatus.OK, status_message: Optional[str] = None) -> None:
        """Mark span as finished and calculate duration."""
        self.end_time = datetime.now(timezone.utc).timestamp()
        self.duration_ms = (self.end_time - self.start_time) * 1000.0
        self.status = status
        self.status_message = status_message

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        self.events.append(SpanEvent(name=name, attributes=attributes or {}))

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value
