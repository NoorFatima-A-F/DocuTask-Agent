"""Distributed Tracing and Context Propagation (W3C / B3)."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class SpanKind(str, Enum):
    CLIENT = "CLIENT"
    SERVER = "SERVER"
    PROXY = "PROXY"
    INTERNAL = "INTERNAL"


@dataclass
class MeshSpan:
    span_id: str
    trace_id: str
    name: str
    parent_span_id: Optional[str] = None
    kind: SpanKind = SpanKind.CLIENT
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status_code: int = 200
    attributes: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000.0
        return (time.time() - self.start_time) * 1000.0

    def finish(self, status_code: int = 200) -> None:
        self.end_time = time.time()
        self.status_code = status_code


class TraceContextPropagator:
    """Injects and extracts distributed tracing headers across service boundaries."""

    @staticmethod
    def generate_trace_id() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def generate_span_id() -> str:
        return uuid.uuid4().hex[:16]

    @staticmethod
    def inject_w3c_headers(
        trace_id: str,
        span_id: str,
        headers: Dict[str, str],
        sampled: bool = True,
    ) -> Dict[str, str]:
        """Inject W3C traceparent header: 00-{trace_id}-{span_id}-{flags}."""
        flags = "01" if sampled else "00"
        headers["traceparent"] = f"00-{trace_id}-{span_id}-{flags}"
        # Also inject B3 headers for compatibility
        headers["x-b3-traceid"] = trace_id
        headers["x-b3-spanid"] = span_id
        headers["x-b3-sampled"] = "1" if sampled else "0"
        return headers

    @staticmethod
    def extract_context(headers: Dict[str, str]) -> tuple[str, Optional[str], bool]:
        """Extract (trace_id, parent_span_id, sampled) from incoming headers."""
        # 1. Try W3C traceparent
        traceparent = headers.get("traceparent") or headers.get("Traceparent")
        if traceparent:
            parts = traceparent.split("-")
            if len(parts) >= 4:
                return parts[1], parts[2], parts[3] == "01"

        # 2. Try B3 headers
        b3_trace = headers.get("x-b3-traceid") or headers.get("X-B3-TraceId")
        if b3_trace:
            b3_span = headers.get("x-b3-spanid") or headers.get("X-B3-SpanId")
            b3_sampled = (headers.get("x-b3-sampled") or headers.get("X-B3-Sampled")) == "1"
            return b3_trace, b3_span, b3_sampled

        # 3. Fallback fresh trace ID
        return TraceContextPropagator.generate_trace_id(), None, True
