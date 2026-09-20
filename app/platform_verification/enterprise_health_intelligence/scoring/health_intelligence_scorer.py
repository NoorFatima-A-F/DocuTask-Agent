"""
Phase 3H.5: Health Intelligence Scorer
"""
from typing import Dict, Any
from ..domain.interfaces import IHealthIntelligenceScorer
from ..domain.models import (
    HealthEventArchitectureReport,
    FailureClassificationReport,
    EventCorrelationReport,
    RCAReport,
    RemediationDecisionReport,
    RecoveryExecutionReport,
    SelfHealingValidationReport,
    RemediationSecurityReport,
    HealthDashboardReport,
    ChaosHealthReport,
    HealthIntelligenceScorecard,
    IntelligenceCertificationTier,
)


class HealthIntelligenceScorer(IHealthIntelligenceScorer):
    def calculate_scorecard(
        self,
        event_report: HealthEventArchitectureReport,
        class_report: FailureClassificationReport,
        corr_report: EventCorrelationReport,
        rca_report: RCAReport,
        remed_report: RemediationDecisionReport,
        recov_report: RecoveryExecutionReport,
        self_heal_report: SelfHealingValidationReport,
        safety_report: RemediationSecurityReport,
        obs_report: HealthDashboardReport,
        chaos_report: ChaosHealthReport,
    ) -> HealthIntelligenceScorecard:
        # 1. Failure detection (15%)
        det_score = 100.0 if (event_report.architecture_valid and len(event_report.events) >= 7) else 80.0

        # 2. Diagnosis accuracy (20%)
        diag_score = 100.0 if (class_report.classification_valid and class_report.classification_accuracy_pct >= 95.0) else 80.0

        # 3. Event correlation (15%)
        corr_score = 100.0 if (corr_report.correlation_valid and corr_report.noise_reduction_pct >= 50.0) else 80.0

        # 4. RCA quality (15%)
        rca_score = 100.0 if (rca_report.rca_valid and rca_report.mean_confidence_score >= 0.95) else 80.0

        # 5. Recovery automation (20%)
        recov_score = 100.0 if (
            recov_report.all_recoveries_successful
            and self_heal_report.self_healing_certified
            and chaos_report.all_chaos_tests_passed
        ) else 80.0

        # 6. Safety controls (15%)
        safety_score = 100.0 if (
            remed_report.safety_classification_enforced
            and safety_report.security_score_pct >= 95.0
            and obs_report.all_dashboards_active
        ) else 80.0

        composite = (
            det_score * 0.15
            + diag_score * 0.20
            + corr_score * 0.15
            + rca_score * 0.15
            + recov_score * 0.20
            + safety_score * 0.15
        )

        composite = round(composite, 2)

        if composite >= 95.0:
            tier = IntelligenceCertificationTier.AUTONOMOUS_RELIABILITY_READY
            certified = True
        elif composite >= 90.0:
            tier = IntelligenceCertificationTier.PRODUCTION_RELIABILITY_READY
            certified = True
        elif composite >= 80.0:
            tier = IntelligenceCertificationTier.IMPROVEMENT_REQUIRED
            certified = False
        else:
            tier = IntelligenceCertificationTier.FAILED
            certified = False

        return HealthIntelligenceScorecard(
            failure_detection_score=round(det_score, 2),
            diagnosis_accuracy_score=round(diag_score, 2),
            event_correlation_score=round(corr_score, 2),
            rca_quality_score=round(rca_score, 2),
            recovery_automation_score=round(recov_score, 2),
            safety_controls_score=round(safety_score, 2),
            composite_score=composite,
            tier=tier,
            certified_enterprise_ready=certified,
        )
