"""
Composite Scorer for Part 3I: Enterprise Observability Infrastructure (Logging + Metrics)
"""
from datetime import datetime, timezone
from ..domain.models import (
    LoggingCertificationReport,
    MetricsCertificationReport,
    UnifiedObservabilityCertification,
    ObservabilityCertificationTier,
)


class ObservabilityCompositeScorer:
    """
    Blends Part 3I.1 (Logging, 50%) and Part 3I.2 (Metrics, 50%) to produce the Unified Observability Certification.
    """

    def calculate_unified_certification(
        self,
        logging_cert: LoggingCertificationReport,
        metrics_cert: MetricsCertificationReport,
    ) -> UnifiedObservabilityCertification:
        log_score = logging_cert.overall_score_pct
        met_score = metrics_cert.overall_score_pct
        composite_score = round((log_score * 0.5) + (met_score * 0.5), 2)

        if composite_score >= 95.0 and logging_cert.certification_granted and metrics_cert.certification_granted:
            tier = ObservabilityCertificationTier.ENTERPRISE_OBSERVABILITY_CERTIFIED
            granted = True
        elif composite_score >= 90.0:
            tier = ObservabilityCertificationTier.PRODUCTION_OBSERVABILITY_READY
            granted = True
        elif composite_score >= 80.0:
            tier = ObservabilityCertificationTier.IMPROVEMENT_REQUIRED
            granted = False
        else:
            tier = ObservabilityCertificationTier.FAILED
            granted = False

        return UnifiedObservabilityCertification(
            report_title="Part 3I Unified Enterprise Observability Infrastructure Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            logging_score_pct=log_score,
            metrics_score_pct=met_score,
            overall_score_pct=composite_score,
            certification_tier=tier,
            certification_granted=granted,
            auditor="DocuTask Enterprise Observability & SRE Certification Engine"
        )
