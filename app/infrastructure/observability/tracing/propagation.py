"""
Distributed Trace Context Propagation.

Implements W3C TraceContext (traceparent, tracestate) and B3 header injection/extraction
across HTTP, gRPC, and asynchronous message queues.
"""

from __future__ import annotations

import logging
import uuid
from typing import Dict, Optional, Tuple

logger = logging.getLogger("infrastructure.observability.tracing.propagation")


class TraceContextPropagator:
    """
    Serializes and deserializes distributed trace identifiers across process boundaries.
    """

    @staticmethod
    def inject_w3c(trace_id: str, span_id: str, sampled: bool = True) -> Dict[str, str]:
        """Generate W3C traceparent header format: 00-{trace_id}-{span_id}-{flags}."""
        flags = "01" if sampled else "00"
        # Pad trace_id to 32 chars and span_id to 16 chars
        t_id = trace_id.rjust(32, "0")[:32]
        s_id = span_id.rjust(16, "0")[:16]
        return {
            "traceparent": f"00-{t_id}-{s_id}-{flags}",
        }

    @staticmethod
    def extract_w3c(headers: Dict[str, str]) -> Optional[Tuple[str, str, bool]]:
        """Extract trace_id, span_id, and sampled flag from W3C traceparent header."""
        lower = {k.lower(): v for k, v in headers.items()}
        tp = lower.get("traceparent")
        if not tp:
            return None

        parts = tp.split("-")
        if len(parts) != 4 or parts[0] != "00":
            return None

        trace_id = parts[1]
        span_id = parts[2]
        sampled = (parts[3] == "01")
        return trace_id, span_id, sampled

    @staticmethod
    def inject_b3(trace_id: str, span_id: str, parent_span_id: Optional[str] = None, sampled: bool = True) -> Dict[str, str]:
        """Generate Zipkin/B3 compatible headers."""
        headers = {
            "x-b3-traceid": trace_id,
            "x-b3-spanid": span_id,
            "x-b3-sampled": "1" if sampled else "0",
        }
        if parent_span_id:
            headers["x-b3-parentspanid"] = parent_span_id
        return headers

    @staticmethod
    def extract_b3(headers: Dict[str, str]) -> Optional[Tuple[str, str, Optional[str], bool]]:
        """Extract B3 headers."""
        lower = {k.lower(): v for k, v in headers.items()}
        trace_id = lower.get("x-b3-traceid")
        span_id = lower.get("x-b3-spanid")
        if not trace_id or not span_id:
            return None

        parent_span_id = lower.get("x-b3-parentspanid")
        sampled = (lower.get("x-b3-sampled", "1") == "1")
        return trace_id, span_id, parent_span_id, sampled
