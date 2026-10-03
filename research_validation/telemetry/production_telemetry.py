"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 44: Production Telemetry & Observability Verification Laboratory

Validates end-to-end distributed telemetry, OpenTelemetry (OTel) traces, span hierarchy,
and platform metrics across Cloud Run, Vertex AI, Redis, and Cloud Pub/Sub.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class TelemetrySpan:
    """A distributed trace span conforming to OpenTelemetry specifications."""
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    start_time_ns: int
    end_time_ns: int
    status_code: str  # "OK", "ERROR", "UNSET"
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        return (self.end_time_ns - self.start_time_ns) / 1e6


@dataclass
class ServiceSLOStatus:
    """SLO evaluation for a specific service component."""
    service_name: str
    sli_type: str  # "LATENCY_P99", "AVAILABILITY", "ERROR_RATE", "THROUGHPUT"
    target_threshold: float
    observed_value: float
    is_compliant: bool


@dataclass
class TelemetryAuditReport:
    """Comprehensive production telemetry audit report."""
    total_spans_analyzed: int
    total_traces_analyzed: int
    orphaned_spans_count: int
    broken_traces_count: int
    span_completeness_ratio: float
    slo_evaluations: List[ServiceSLOStatus]
    all_slos_met: bool
    status: str  # "PASS", "DEGRADED", "FAIL"
    details: Dict[str, Any] = field(default_factory=dict)


class ProductionTelemetryValidator:
    """
    Validates trace graphs, span lineage, and SLO compliance across distributed subsystems.
    """

    @classmethod
    def validate_trace_graph(cls, spans: List[TelemetrySpan]) -> Tuple[int, int, float]:
        """
        Validates tree hierarchy of trace spans.
        Returns: (orphaned_spans, broken_traces, completeness_ratio)
        """
        if not spans:
            return 0, 0, 0.0

        traces: Dict[str, List[TelemetrySpan]] = {}
        for s in spans:
            traces.setdefault(s.trace_id, []).append(s)

        orphaned = 0
        broken_traces = 0

        for trace_id, trace_spans in traces.items():
            span_ids = {s.span_id for s in trace_spans}
            trace_broken = False

            # Check parent references
            root_spans = 0
            for s in trace_spans:
                if s.parent_span_id is None:
                    root_spans += 1
                elif s.parent_span_id not in span_ids:
                    orphaned += 1
                    trace_broken = True

            if root_spans == 0 or trace_broken:
                broken_traces += 1

        total_traces = len(traces)
        valid_traces = total_traces - broken_traces
        completeness = valid_traces / total_traces if total_traces > 0 else 0.0

        return orphaned, broken_traces, completeness

    @classmethod
    def evaluate_service_slos(
        cls,
        spans: List[TelemetrySpan],
        error_rate_threshold: float = 0.01,
        latency_p99_threshold_ms: float = 5000.0
    ) -> List[ServiceSLOStatus]:
        """
        Evaluate SLOs per service component from span data.
        """
        if not spans:
            return []

        services: Dict[str, List[TelemetrySpan]] = {}
        for s in spans:
            svc = s.attributes.get("service.name", "unknown_service")
            services.setdefault(svc, []).append(s)

        slo_results: List[ServiceSLOStatus] = []

        for svc_name, svc_spans in services.items():
            n = len(svc_spans)
            # Error rate SLI
            error_count = sum(1 for s in svc_spans if s.status_code == "ERROR")
            err_rate = error_count / n
            slo_results.append(ServiceSLOStatus(
                service_name=svc_name,
                sli_type="ERROR_RATE",
                target_threshold=error_rate_threshold,
                observed_value=err_rate,
                is_compliant=err_rate <= error_rate_threshold
            ))

            # Latency P99 SLI
            durations = sorted(s.duration_ms for s in svc_spans)
            p99_idx = min(int(0.99 * n), n - 1)
            p99_latency = durations[p99_idx]
            slo_results.append(ServiceSLOStatus(
                service_name=svc_name,
                sli_type="LATENCY_P99",
                target_threshold=latency_p99_threshold_ms,
                observed_value=p99_latency,
                is_compliant=p99_latency <= latency_p99_threshold_ms
            ))

        return slo_results

    @classmethod
    def run_telemetry_audit(
        cls,
        spans: List[TelemetrySpan],
        error_rate_threshold: float = 0.01,
        latency_p99_threshold_ms: float = 5000.0
    ) -> TelemetryAuditReport:
        """Run end-to-end telemetry and observability audit."""
        if not spans:
            return TelemetryAuditReport(
                total_spans_analyzed=0,
                total_traces_analyzed=0,
                orphaned_spans_count=0,
                broken_traces_count=0,
                span_completeness_ratio=0.0,
                slo_evaluations=[],
                all_slos_met=False,
                status="INSUFFICIENT_EVIDENCE"
            )

        unique_traces = len(set(s.trace_id for s in spans))
        orphaned, broken, completeness = cls.validate_trace_graph(spans)
        slos = cls.evaluate_service_slos(
            spans,
            error_rate_threshold=error_rate_threshold,
            latency_p99_threshold_ms=latency_p99_threshold_ms
        )

        all_slos_met = all(s.is_compliant for s in slos) if slos else False
        passed = (completeness >= 0.95) and (orphaned == 0) and all_slos_met
        status = "PASS" if passed else "DEGRADED" if completeness >= 0.80 else "FAIL"

        return TelemetryAuditReport(
            total_spans_analyzed=len(spans),
            total_traces_analyzed=unique_traces,
            orphaned_spans_count=orphaned,
            broken_traces_count=broken,
            span_completeness_ratio=completeness,
            slo_evaluations=slos,
            all_slos_met=all_slos_met,
            status=status,
            details={"cloud_services_observed": list(set(s.attributes.get("service.name", "") for s in spans))}
        )
