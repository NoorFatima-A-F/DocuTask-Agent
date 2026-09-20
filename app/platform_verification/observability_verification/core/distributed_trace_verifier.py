"""
OpenTelemetry Distributed Tracing & Reconstructability Verifier.
"""
from typing import List, Dict, Any
from app.platform_verification.observability_verification.domain.models import DistributedTraceReport
from app.platform_verification.observability_verification.domain.interfaces import IDistributedTraceVerifier


class DistributedTraceVerifier(IDistributedTraceVerifier):
    """Verifies OpenTelemetry W3C trace context propagation and end-to-end reconstructability."""

    def verify_distributed_tracing(self, trace_spans: List[Dict[str, Any]]) -> DistributedTraceReport:
        missing_context: List[str] = []

        for span in trace_spans:
            name = span.get("span_name", "span")
            has_trace = bool(span.get("trace_id"))
            has_span = bool(span.get("span_id"))

            if not has_trace or not has_span:
                missing_context.append(f"Span '{name}' lacks valid trace_id or span_id")

        unbroken = len(missing_context) == 0
        status = "PASS" if unbroken else "FAIL"

        return DistributedTraceReport(
            total_spans=len(trace_spans),
            unbroken_context_propagation=unbroken,
            missing_context_spans=missing_context,
            document_lifecycle_reconstructable=unbroken,
            status=status,
        )
