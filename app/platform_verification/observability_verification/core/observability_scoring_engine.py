"""
Weighted Observability Quality Scoring and Certification Engine.
"""
from app.platform_verification.observability_verification.domain.models import (
    LoggingQualityReport,
    MetricsInventoryReport,
    DistributedTraceReport,
    AlertQualityReport,
    SloComplianceReport,
    IncidentResponseReport,
    ObservabilityCertificationReport,
    ObservabilityCertificationTier,
)
from app.platform_verification.observability_verification.domain.interfaces import IObservabilityScoringEngine


class ObservabilityScoringEngine(IObservabilityScoringEngine):
    """Calculates weighted composite scorecard across 6 observability pillars."""

    # Weights: Logging (15%), Metrics (20%), Tracing (20%), Alerting (15%), SLO (15%), Incident Response (15%)
    WEIGHT_LOGGING = 0.15
    WEIGHT_METRICS = 0.20
    WEIGHT_TRACING = 0.20
    WEIGHT_ALERTING = 0.15
    WEIGHT_SLO = 0.15
    WEIGHT_INCIDENT = 0.15

    def calculate_scorecard(
        self,
        log_rep: LoggingQualityReport,
        metric_rep: MetricsInventoryReport,
        trace_rep: DistributedTraceReport,
        alert_rep: AlertQualityReport,
        slo_rep: SloComplianceReport,
        inc_rep: IncidentResponseReport,
    ) -> ObservabilityCertificationReport:
        log_s = log_rep.logging_quality_score
        metric_s = 100.0 if metric_rep.golden_signals_complete and metric_rep.ai_metrics_complete else 70.0
        trace_s = 100.0 if trace_rep.unbroken_context_propagation else 50.0
        alert_s = alert_rep.alert_quality_score
        slo_s = slo_rep.slo_compliance_score
        inc_s = inc_rep.recovery_success_rate

        composite = (
            (log_s * self.WEIGHT_LOGGING)
            + (metric_s * self.WEIGHT_METRICS)
            + (trace_s * self.WEIGHT_TRACING)
            + (alert_s * self.WEIGHT_ALERTING)
            + (slo_s * self.WEIGHT_SLO)
            + (inc_s * self.WEIGHT_INCIDENT)
        )
        composite = round(composite, 2)

        if composite >= 95.0 and len(log_rep.sensitive_data_leaks_detected) == 0 and trace_rep.unbroken_context_propagation:
            tier = ObservabilityCertificationTier.ENTERPRISE_OBSERVABILITY_READY
        elif composite >= 90.0:
            tier = ObservabilityCertificationTier.PRODUCTION_READY
        elif composite >= 80.0:
            tier = ObservabilityCertificationTier.IMPROVEMENT_REQUIRED
        else:
            tier = ObservabilityCertificationTier.FAILED

        return ObservabilityCertificationReport(
            logging_quality_score=round(log_s, 2),
            metrics_coverage_score=round(metric_s, 2),
            distributed_tracing_score=round(trace_s, 2),
            alerting_score=round(alert_s, 2),
            slo_management_score=round(slo_s, 2),
            incident_response_score=round(inc_s, 2),
            composite_score=composite,
            tier=tier,
        )
