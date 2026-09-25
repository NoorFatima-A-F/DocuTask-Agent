"""
Coordination Telemetry.
OpenTelemetry tracing, W3C trace context, and correlation propagation across multi-agent messages.
"""

from typing import Dict, Optional
from uuid import uuid4


class CoordinationTelemetry:
    """Manages OpenTelemetry trace propagation and correlation IDs."""

    @staticmethod
    def generate_trace_context(correlation_id: Optional[str] = None) -> Dict[str, str]:
        """Generates standard W3C traceparent headers for agent message routing."""
        corr = correlation_id or str(uuid4())
        trace_id = uuid4().hex
        span_id = uuid4().hex[:16]
        return {
            "traceparent": f"00-{trace_id}-{span_id}-01",
            "correlation-id": corr
        }
