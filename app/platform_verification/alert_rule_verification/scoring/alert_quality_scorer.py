"""Alert Quality Scorer (3H.4.5.14).

Computes weighted composite score across 6 key operational alert dimensions:
- Detection accuracy: 25%
- Severity correctness: 20%
- Message quality: 15%
- Routing correctness: 15%
- Noise reduction: 15%
- Performance: 10%
"""

from datetime import datetime, timezone
from ..domain.models import (
    ArchitectureReport,
    TaxonomyReport,
    CriticalAlertReport,
    WarningAlertReport,
    ConditionTestReport,
    SeverityReport,
    MessageQualityReport,
    RoutingReport,
    FatigueReport,
    FailureTestReport,
    PerformanceReport,
    AlertQualityScorecard,
    AlertCertificationTier,
)
from ..domain.interfaces import IAlertQualityScorer


class AlertQualityScorer(IAlertQualityScorer):
    """Calculates weighted operational readiness score for alert intelligence suite."""

    def score_alerts(
        self,
        arch_rep: ArchitectureReport,
        tax_rep: TaxonomyReport,
        crit_rep: CriticalAlertReport,
        warn_rep: WarningAlertReport,
        cond_rep: ConditionTestReport,
        sev_rep: SeverityReport,
        msg_rep: MessageQualityReport,
        route_rep: RoutingReport,
        fatigue_rep: FatigueReport,
        fail_rep: FailureTestReport,
        perf_rep: PerformanceReport,
    ) -> AlertQualityScorecard:
        # Category scores (0-100)
        det_acc = (
            100.0
            if (
                crit_rep.status == "PASS"
                and warn_rep.status == "PASS"
                and cond_rep.status == "PASS"
                and fail_rep.status == "PASS"
            )
            else 50.0
        )
        sev_corr = 100.0 if (sev_rep.status == "PASS" and sev_rep.zero_severity_misclassification) else 50.0
        msg_qual = 100.0 if (msg_rep.status == "PASS" and msg_rep.message_quality_score >= 95.0) else 50.0
        route_corr = 100.0 if (route_rep.status == "PASS" and route_rep.escalation_matrix_verified) else 50.0
        noise_red = 100.0 if (fatigue_rep.status == "PASS" and fatigue_rep.noise_reduction_ratio >= 0.90) else 50.0
        perf = 100.0 if (perf_rep.status == "PASS" and perf_rep.mttd_seconds < 30.0) else 50.0

        # Weighted calculation
        overall = (
            det_acc * 0.25
            + sev_corr * 0.20
            + msg_qual * 0.15
            + route_corr * 0.15
            + noise_red * 0.15
            + perf * 0.10
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = AlertCertificationTier.ENTERPRISE_ALERTING_CERTIFIED
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = AlertCertificationTier.PRODUCTION_ALERTING_READY
            verdict = "CONDITIONAL_PASS"
            passed = True
        elif overall >= 80.0:
            tier = AlertCertificationTier.IMPROVEMENT_REQUIRED
            verdict = "REMEDIATION_REQUIRED"
            passed = False
        else:
            tier = AlertCertificationTier.FAILED
            verdict = "FAILED"
            passed = False

        return AlertQualityScorecard(
            detection_accuracy_score=det_acc,
            severity_correctness_score=sev_corr,
            message_quality_score=msg_qual,
            routing_correctness_score=route_corr,
            noise_reduction_score=noise_red,
            performance_score=perf,
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
