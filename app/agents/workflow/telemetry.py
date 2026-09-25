"""
Workflow Telemetry.
OpenTelemetry distributed tracing, W3C trace context, and correlation propagation across workflow stages and child workflows.
"""

from typing import Dict, Optional
from uuid import uuid4


class WorkflowTelemetry:
    """Manages OpenTelemetry trace propagation and correlation IDs for workflow execution."""

    @staticmethod
    def generate_trace_context(correlation_id: Optional[str] = None) -> Dict[str, str]:
        """Generates standard W3C traceparent headers for workflow instance tracking."""
        corr = correlation_id or str(uuid4())
        trace_id = uuid4().hex
        span_id = uuid4().hex[:16]
        return {
            "traceparent": f"00-{trace_id}-{span_id}-01",
            "correlation-id": corr,
        }

    @staticmethod
    def extract_trace_context(headers: Dict[str, str]) -> Dict[str, Optional[str]]:
        """Extracts traceparent and correlation identifiers from carrier headers."""
        return {
            "traceparent": headers.get("traceparent"),
            "correlation-id": headers.get("correlation-id"),
        }
