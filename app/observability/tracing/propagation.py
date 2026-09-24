"""W3C TraceContext and B3 Header Propagation."""

from __future__ import annotations

import re
from typing import Dict, Optional

from .spans import SpanContext


class TraceContextPropagator:
    """Injects and extracts distributed trace headers across HTTP/gRPC boundaries."""

    @staticmethod
    def inject(context: SpanContext, carrier: Dict[str, str], baggage: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Inject W3C traceparent and B3 headers into carrier dict."""
        flags = context.trace_flags or "01"
        carrier["traceparent"] = f"00-{context.trace_id}-{context.span_id}-{flags}"
        if context.trace_state:
            carrier["tracestate"] = context.trace_state

        # B3 Compatibility
        carrier["x-b3-traceid"] = context.trace_id
        carrier["x-b3-spanid"] = context.span_id
        carrier["x-b3-sampled"] = "1" if context.is_sampled else "0"

        # Baggage
        if baggage:
            carrier["baggage"] = ",".join(f"{k}={v}" for k, v in baggage.items())

        return carrier

    @staticmethod
    def extract(carrier: Dict[str, str]) -> Optional[SpanContext]:
        """Extract SpanContext from carrier headers (supports W3C traceparent, B3 multi)."""
        # 1. Try W3C traceparent
        traceparent = carrier.get("traceparent") or carrier.get("Traceparent")
        if traceparent:
            match = re.match(r"^00-([0-9a-fA-F]{32})-([0-9a-fA-F]{16})-([0-9a-fA-F]{2})$", traceparent.strip())
            if match:
                trace_id, span_id, flags = match.groups()
                tracestate = carrier.get("tracestate", "")
                return SpanContext(
                    trace_id=trace_id.lower(),
                    span_id=span_id.lower(),
                    trace_flags=flags,
                    trace_state=tracestate,
                    is_sampled=(flags == "01"),
                )

        # 2. Try B3 headers
        b3_trace = carrier.get("x-b3-traceid") or carrier.get("X-B3-TraceId")
        b3_span = carrier.get("x-b3-spanid") or carrier.get("X-B3-SpanId")
        if b3_trace and b3_span:
            sampled_str = carrier.get("x-b3-sampled") or carrier.get("X-B3-Sampled") or "1"
            is_sampled = (sampled_str == "1")
            return SpanContext(
                trace_id=b3_trace.lower(),
                span_id=b3_span.lower(),
                trace_flags="01" if is_sampled else "00",
                is_sampled=is_sampled,
            )

        return None

    @staticmethod
    def extract_baggage(carrier: Dict[str, str]) -> Dict[str, str]:
        raw_baggage = carrier.get("baggage") or carrier.get("Baggage")
        if not raw_baggage:
            return {}
        result = {}
        for item in raw_baggage.split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                result[k.strip()] = v.strip()
        return result
