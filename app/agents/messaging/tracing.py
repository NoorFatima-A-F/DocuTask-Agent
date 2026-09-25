"""
OpenTelemetry Tracing Integration.
Provides DistributedTrace context injection and extraction hooks.
"""

from typing import Dict
from app.agents.messaging.metadata import TraceContext


class TracingHook:
    """OpenTelemetry W3C distributed trace context handler."""

    @staticmethod
    def inject_trace(trace: TraceContext, carrier: Dict[str, str]) -> Dict[str, str]:
        """Injects traceparent W3C header into carrier dictionary."""
        carrier["traceparent"] = f"00-{trace.trace_id}-{trace.span_id}-{trace.trace_flags}"
        return carrier

    @staticmethod
    def extract_trace(carrier: Dict[str, str]) -> TraceContext:
        """Extracts traceparent W3C header from carrier dictionary."""
        header = carrier.get("traceparent", "")
        parts = header.split("-")
        if len(parts) == 4:
            return TraceContext(trace_id=parts[1], span_id=parts[2], trace_flags=parts[3])
        return TraceContext()
