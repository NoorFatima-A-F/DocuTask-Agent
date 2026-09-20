"""
Resilience Score Engine for Operational Resilience Framework (Part 3G.5I).
Computes weighted composite resilience score across 6 core categories:
1. Detection (20%)
2. Recovery Automation (25%)
3. Data Integrity (20%)
4. Failure Containment (15%)
5. Operational Visibility (10%)
6. Documentation (10%)
"""
from typing import Dict, Any, List

from app.platform_verification.operational_resilience.domain.models import (
    ResilienceTier,
    FailureExperimentResult,
    SelfHealingReport,
    IncidentAutomationReport,
    RunbookValidationReport,
    DependencyResilienceReport,
    StateConsistencyReport,
    DrillResult,
    OperationalResilienceScorecard,
)
from app.platform_verification.operational_resilience.domain.interfaces import (
    IResilienceScoreEngine,
)


class ResilienceScoreEngine(IResilienceScoreEngine):
    """
    Evaluates enterprise resilience scoring model and assigns certification tiers.
    """

    WEIGHTS = {
        "detection": 0.20,
        "recovery_automation": 0.25,
        "data_integrity": 0.20,
        "failure_containment": 0.15,
        "operational_visibility": 0.10,
        "documentation": 0.10,
    }

    def calculate_scorecard(
        self,
        experiments: List[FailureExperimentResult],
        self_healing: SelfHealingReport,
        incidents: IncidentAutomationReport,
        runbooks: RunbookValidationReport,
        dependencies: DependencyResilienceReport,
        consistency: StateConsistencyReport,
        drill: DrillResult,
    ) -> OperationalResilienceScorecard:
        # 1. Detection Score (20%): All experiments detected with MTTD < 30s
        detection_rate = (
            sum(1 for e in experiments if e.detected and e.detection_time_seconds <= 30.0)
            / len(experiments)
            if experiments
            else 1.0
        )
        detection_score = round(detection_rate * 100.0, 2)

        # 2. Recovery Automation (25%): Automated recovery success & self-healing
        rec_rate = (
            sum(1 for e in experiments if e.recovered and e.recovery_duration_seconds <= 300.0)
            / len(experiments)
            if experiments
            else 1.0
        )
        healing_factor = 1.0 if self_healing.passed else 0.5
        recovery_score = round(((rec_rate * 0.7) + (healing_factor * 0.3)) * 100.0, 2)

        # 3. Data Integrity (20%): Zero data loss in experiments and state consistency
        zero_loss = 1.0 if all(not e.data_loss and e.data_integrity_verified for e in experiments) else 0.0
        consistency_factor = 1.0 if consistency.passed else 0.0
        data_integrity_score = round(((zero_loss * 0.5) + (consistency_factor * 0.5)) * 100.0, 2)

        # 4. Failure Containment (15%): Dependency resilience & circuit breakers
        containment_score = 100.0 if dependencies.passed else 50.0

        # 5. Operational Visibility (10%): Incident auto-ticketing, metrics & alerting
        visibility_score = 100.0 if incidents.passed else 60.0

        # 6. Documentation (10%): Runbook automated coverage
        doc_score = 100.0 if runbooks.passed else 50.0

        # Composite weighted score
        composite = (
            detection_score * self.WEIGHTS["detection"]
            + recovery_score * self.WEIGHTS["recovery_automation"]
            + data_integrity_score * self.WEIGHTS["data_integrity"]
            + containment_score * self.WEIGHTS["failure_containment"]
            + visibility_score * self.WEIGHTS["operational_visibility"]
            + doc_score * self.WEIGHTS["documentation"]
        )
        composite = round(composite, 2)

        if composite >= 95.0:
            tier = ResilienceTier.ENTERPRISE_RESILIENT
        elif composite >= 90.0:
            tier = ResilienceTier.PRODUCTION_RESILIENT
        elif composite >= 80.0:
            tier = ResilienceTier.ACCEPTABLE
        else:
            tier = ResilienceTier.REQUIRES_IMPROVEMENT

        passed = composite >= 95.0
        cert_verdict = "ENTERPRISE_RESILIENT_CERTIFIED" if passed else "CERTIFICATION_REJECTED"
        deployment_approved = passed

        details = {
            "weights": self.WEIGHTS,
            "category_scores": {
                "detection": detection_score,
                "recovery_automation": recovery_score,
                "data_integrity": data_integrity_score,
                "failure_containment": containment_score,
                "operational_visibility": visibility_score,
                "documentation": doc_score,
            },
            "tier_description": tier.value,
            "scoring_model_version": "3G.5-ENTERPRISE-RESILIENCE",
        }

        return OperationalResilienceScorecard(
            detection_score=detection_score,
            recovery_automation_score=recovery_score,
            data_integrity_score=data_integrity_score,
            failure_containment_score=containment_score,
            operational_visibility_score=visibility_score,
            documentation_score=doc_score,
            overall_resilience_score=composite,
            resilience_tier=tier,
            certification_verdict=cert_verdict,
            ci_cd_deployment_approved=deployment_approved,
            passed=passed,
            details=details,
        )
