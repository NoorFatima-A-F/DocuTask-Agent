"""Alert Fatigue Scorer (3H.4.8.11).

Computes 6-category weighted composite score for alert fatigue prevention and signal optimization:
- Deduplication accuracy (20%)
- Correlation quality (20%)
- Severity accuracy (15%)
- Noise reduction (15%)
- Routing correctness (15%)
- Safety controls (15%)
"""

from datetime import datetime, timezone
from ..domain.models import (
    FatigueArchitectureReport,
    DeduplicationReport,
    CorrelationReport,
    SeverityOptimizationReport,
    RoutingReport,
    SuppressionReport,
    GroupingReport,
    NoiseMetricsReport,
    AlertStormReport,
    MachinePrioritizationReport,
    AlertFatigueScorecard,
    AlertIntelligenceTier,
)
from ..domain.interfaces import IAlertFatigueScorer


class AlertFatigueScorer(IAlertFatigueScorer):
    """Calculates weighted operational readiness score for alert fatigue reduction."""

    def score_fatigue(
        self,
        arch_rep: FatigueArchitectureReport,
        dedup_rep: DeduplicationReport,
        corr_rep: CorrelationReport,
        sev_rep: SeverityOptimizationReport,
        route_rep: RoutingReport,
        supp_rep: SuppressionReport,
        group_rep: GroupingReport,
        noise_rep: NoiseMetricsReport,
        storm_rep: AlertStormReport,
        ml_rep: MachinePrioritizationReport,
    ) -> AlertFatigueScorecard:
        # Category scores (0-100)
        dedup_score = 100.0 if (dedup_rep.status == "PASS" and dedup_rep.deduplication_accuracy_percentage >= 95.0) else 50.0
        corr_score = 100.0 if (corr_rep.status == "PASS" and corr_rep.root_cause_accuracy_percentage >= 95.0) else 50.0
        sev_score = 100.0 if (sev_rep.status == "PASS" and sev_rep.misclassification_count == 0) else 50.0
        noise_score = 100.0 if (noise_rep.status == "PASS" and noise_rep.targets_met) else 50.0
        route_score = 100.0 if (route_rep.status == "PASS" and route_rep.routing_accuracy_percentage >= 95.0) else 50.0
        safety_score = 100.0 if (supp_rep.status == "PASS" and supp_rep.safety_overrides_functional and storm_rep.critical_signals_preserved) else 50.0

        # Weighted calculation
        overall = (
            dedup_score * 0.20
            + corr_score * 0.20
            + sev_score * 0.15
            + noise_score * 0.15
            + route_score * 0.15
            + safety_score * 0.15
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = AlertIntelligenceTier.ENTERPRISE_ALERT_INTELLIGENCE_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = AlertIntelligenceTier.PRODUCTION_ALERTING_READY
            verdict = "CONDITIONAL_PASS"
            passed = True
        elif overall >= 80.0:
            tier = AlertIntelligenceTier.IMPROVEMENT_REQUIRED
            verdict = "REMEDIATION_REQUIRED"
            passed = False
        else:
            tier = AlertIntelligenceTier.FAILED
            verdict = "FAILED"
            passed = False

        return AlertFatigueScorecard(
            deduplication_accuracy_score=dedup_score,
            correlation_quality_score=corr_score,
            severity_accuracy_score=sev_score,
            noise_reduction_score=noise_score,
            routing_correctness_score=route_score,
            safety_controls_score=safety_score,
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
