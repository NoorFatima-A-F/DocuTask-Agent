"""
Automated Root Cause Analysis (RCA) Engine.

Correlates distributed trace failure paths, log exception stack traces, and metric deviations
into structured RCA diagnostic reports.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.observability.logs.models import LogRecord
from app.infrastructure.observability.tracing.models import Span, SpanStatus

logger = logging.getLogger("infrastructure.observability.diagnostics.root_cause")


class RCAEvidence(BaseModel):
    """Correlated evidence piece supporting the root cause finding."""
    evidence_type: str  # TRACE_SPAN, ERROR_LOG, METRIC_ANOMALY
    source: str
    description: str
    details: Dict[str, Any] = Field(default_factory=dict)


class RCAReport(BaseModel):
    """Structured Root Cause Analysis conclusion."""
    report_id: str
    incident_title: str
    root_cause_service: str
    root_cause_summary: str
    confidence_score: float = Field(default=0.85, ge=0.0, le=1.0)
    evidence: List[RCAEvidence] = Field(default_factory=list)
    recommended_mitigation: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RootCauseAnalyzer:
    """
    Correlates traces, logs, and metrics to diagnose platform incidents.
    """

    def analyze_incident(
        self,
        report_id: str,
        spans: Optional[List[Span]] = None,
        logs: Optional[List[LogRecord]] = None,
        incident_title: str = "Incident Diagnostic",
    ) -> RCAReport:
        """Derive root cause hypothesis from correlated telemetry signals."""
        spans_list = spans or []
        logs_list = logs or []
        evidence: List[RCAEvidence] = []

        root_service = "unknown"
        root_summary = "Inconclusive telemetry correlation."
        mitigation = "Investigate system logs and restart affected services."

        # 1. Inspect failed spans
        failed_spans = [s for s in spans_list if s.status == SpanStatus.ERROR]
        if failed_spans:
            # Find the deepest failed span in the tree
            deepest_failed = failed_spans[-1]
            root_service = deepest_failed.service_name
            root_summary = f"Operation '{deepest_failed.operation_name}' in service '{root_service}' failed: {deepest_failed.status_message or 'Error status'}"
            evidence.append(RCAEvidence(
                evidence_type="TRACE_SPAN",
                source=f"{deepest_failed.service_name}:{deepest_failed.operation_name}",
                description="Deepest failed span in distributed trace tree",
                details={"span_id": deepest_failed.span_id, "error": deepest_failed.status_message},
            ))

        # 2. Inspect error logs
        error_logs = [l for l in logs_list if l.level.value in ("ERROR", "CRITICAL", "FATAL")]
        if error_logs:
            primary_log = error_logs[0]
            if root_service == "unknown":
                root_service = primary_log.service_name
                root_summary = f"Exception in '{primary_log.service_name}': {primary_log.message}"

            evidence.append(RCAEvidence(
                evidence_type="ERROR_LOG",
                source=primary_log.service_name,
                description=f"High severity log ({primary_log.level.value}): {primary_log.message}",
                details={"log_id": primary_log.log_id, "exception": primary_log.exception},
            ))

        if "timeout" in root_summary.lower() or "connection" in root_summary.lower():
            mitigation = "Check network connectivity, downstream dependency health, and retry configuration."
        elif "memory" in root_summary.lower() or "oom" in root_summary.lower():
            mitigation = "Scale up worker memory limits or restart leaking worker processes."
        elif "rate limit" in root_summary.lower() or "429" in root_summary.lower():
            mitigation = "Enable circuit breaker fallback to secondary model provider or request quota increase."

        confidence = 0.95 if (failed_spans and error_logs) else (0.80 if (failed_spans or error_logs) else 0.50)

        return RCAReport(
            report_id=report_id,
            incident_title=incident_title,
            root_cause_service=root_service,
            root_cause_summary=root_summary,
            confidence_score=confidence,
            evidence=evidence,
            recommended_mitigation=mitigation,
        )
