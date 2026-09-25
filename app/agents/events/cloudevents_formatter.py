"""
CNCF CloudEvents 1.0 Formatter and W3C Distributed Tracing Envelope for AAOS.
Standardizes domain events into the open CNCF CloudEvents specification with
traceparent/tracestate W3C context propagation and schema validation.
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.agents.events.event_types import AgentEvent

logger = logging.getLogger(__name__)


@dataclass
class CloudEventV1:
    """Standard CNCF CloudEvents 1.0 JSON Specification."""

    id: str
    source: str
    type: str
    specversion: str = "1.0"
    datacontenttype: str = "application/json"
    time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    data: Dict[str, Any] = field(default_factory=dict)
    # W3C Distributed Tracing Extension Attributes
    traceparent: Optional[str] = None
    tracestate: Optional[str] = None
    # Enterprise Extensions
    idempotencykey: Optional[str] = None
    correlationid: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serializes CloudEvent to dictionary."""
        d = {
            "specversion": self.specversion,
            "id": self.id,
            "source": self.source,
            "type": self.type,
            "datacontenttype": self.datacontenttype,
            "time": self.time,
            "data": self.data,
        }
        if self.traceparent:
            d["traceparent"] = self.traceparent
        if self.tracestate:
            d["tracestate"] = self.tracestate
        if self.idempotencykey:
            d["idempotencykey"] = self.idempotencykey
        if self.correlationid:
            d["correlationid"] = self.correlationid
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class CloudEventsFormatter:
    """
    Transforms internal AgentEvent instances into CloudEvents v1.0 specifications
    and parses inbound external CloudEvents with schema integrity checks.
    """

    @classmethod
    def from_agent_event(
        cls,
        event: AgentEvent,
        source: str = "/aaos/runtime/decision_loop",
        traceparent: Optional[str] = None,
    ) -> CloudEventV1:
        """Encapsulates an internal AgentEvent into standard CloudEvents 1.0."""
        evt_id = str(event.event_id)
        # Generate W3C traceparent if not provided: 00-{trace_id}-{parent_id}-01
        w3c_trace = traceparent or (
            f"00-{event.trace_id or uuid.uuid4().hex}-{uuid.uuid4().hex[:16]}-01"
        )

        return CloudEventV1(
            id=evt_id,
            source=source,
            type=f"com.google.aaos.event.{event.event_type.lower()}",
            time=event.timestamp.isoformat(),
            data=event.payload,
            traceparent=w3c_trace,
            correlationid=event.correlation_id or event.execution_id,
            idempotencykey=f"idemp_{evt_id[:12]}",
        )

    @classmethod
    def validate_cloudevent(cls, event_dict: Dict[str, Any]) -> bool:
        """Validates that incoming dictionary strictly complies with CloudEvents 1.0."""
        required_fields = ["specversion", "id", "source", "type"]
        if not all(rf in event_dict for rf in required_fields):
            return False
        if event_dict.get("specversion") != "1.0":
            return False
        return True
