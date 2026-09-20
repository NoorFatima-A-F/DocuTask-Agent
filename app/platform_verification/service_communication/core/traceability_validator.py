"""
End-to-End Request Traceability Validator.
"""
from typing import List, Dict, Any
from app.platform_verification.service_communication.domain.models import TraceabilityReport
from app.platform_verification.service_communication.domain.interfaces import ITraceabilityValidator


class TraceabilityValidator(ITraceabilityValidator):
    """Verifies propagation of request_id, trace_id, and correlation_id across all spans."""

    def validate_traceability(self, trace_spans: List[Dict[str, Any]]) -> TraceabilityReport:
        untraceable: List[str] = []
        req_ok = True
        trace_ok = True
        corr_ok = True

        for span in trace_spans:
            name = span.get("span_name", "span")
            has_req = bool(span.get("request_id"))
            has_trace = bool(span.get("trace_id"))
            has_corr = bool(span.get("correlation_id"))

            if not has_req:
                req_ok = False
                untraceable.append(f"{name}: missing request_id")
            if not has_trace:
                trace_ok = False
                untraceable.append(f"{name}: missing trace_id")
            if not has_corr:
                corr_ok = False
                untraceable.append(f"{name}: missing correlation_id")

        score = 100.0 - (len(untraceable) * 15.0)
        score = max(0.0, min(100.0, score))
        status = "PASS" if len(untraceable) == 0 else "FAIL"

        return TraceabilityReport(
            request_id_propagated=req_ok,
            trace_id_propagated=trace_ok,
            correlation_id_propagated=corr_ok,
            untraceable_spans=untraceable,
            reconstructability_score=score,
            status=status,
        )
