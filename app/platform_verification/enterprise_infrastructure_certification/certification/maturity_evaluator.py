"""
Phase 3O: Infrastructure Maturity Model Evaluator.
"""

from datetime import datetime, timezone
from typing import Dict, List

from ..domain.interfaces import IMaturityEvaluator
from ..domain.models import (
    MaturityAssessment,
    MaturityLevel,
    QualityScorecard,
    RiskAssessmentReport,
)


class MaturityEvaluator(IMaturityEvaluator):
    """
    Evaluates infrastructure operational maturity across 6 levels (Level 0 - Level 5).
    """

    def assess_maturity(
        self,
        scorecard: QualityScorecard,
        risk_report: RiskAssessmentReport,
    ) -> MaturityAssessment:
        score = scorecard.overall_score
        pillar_ratings: Dict[str, str] = {}
        capabilities: List[str] = []
        next_reqs: List[str] = []

        for cat_name, cat_obj in scorecard.categories.items():
            if cat_obj.score >= 95.0:
                pillar_ratings[cat_name] = "Autonomous / Enterprise Mature"
            elif cat_obj.score >= 90.0:
                pillar_ratings[cat_name] = "Resilient / Production Capable"
            elif cat_obj.score >= 80.0:
                pillar_ratings[cat_name] = "Observable / Standardized"
            elif cat_obj.score >= 60.0:
                pillar_ratings[cat_name] = "Automated / Baseline"
            else:
                pillar_ratings[cat_name] = "Initial / Ad-Hoc"

        if score >= 95.0 and not risk_report.production_blocker_present:
            maturity = MaturityLevel.LEVEL_5
            capabilities = [
                "Continuous verification integrated in CI/CD pipeline",
                "Automated self-healing and proactive anomaly detection",
                "Chaos engineering hypotheses verified across distributed topology",
                "Zero-Trust container isolation & cryptographic SBOM attestations",
                "Multi-cloud portability with zero lock-in dependencies",
                "Sub-5-minute point-in-time disaster recovery verification",
            ]
            next_reqs = ["Sustain automated drift correction and cross-region autonomous routing."]
        elif score >= 90.0 and not risk_report.production_blocker_present:
            maturity = MaturityLevel.LEVEL_4
            capabilities = [
                "Full observability telemetry with OpenTelemetry distributed traces",
                "Hardened secret management & KMS envelope encryption",
                "Automated horizontal autoscaling under 10k burst loads",
                "Verified point-in-time database and storage recovery",
            ]
            next_reqs = [
                "Implement full autonomous remediation for transient microservice blips",
                "Achieve 100% test coverage on multi-region failover automation",
            ]
        elif score >= 80.0:
            maturity = MaturityLevel.LEVEL_3
            capabilities = [
                "Structured logging and Prometheus metrics collection active",
                "Automated container build and unit test suites",
                "Baseline secret isolation and role-based access control",
            ]
            next_reqs = [
                "Implement chaos injection to validate fault tolerance",
                "Automate disaster recovery failover drill testing",
            ]
        elif score >= 60.0:
            maturity = MaturityLevel.LEVEL_2
            capabilities = [
                "Automated deployment manifests and containerization",
                "Basic health check endpoints",
            ]
            next_reqs = [
                "Add distributed tracing and comprehensive metric instrumentation",
                "Establish automated rollback triggers in deployment pipelines",
            ]
        elif score >= 40.0:
            maturity = MaturityLevel.LEVEL_1
            capabilities = ["Manual or scripted container deployments"]
            next_reqs = ["Introduce automated testing and CI/CD quality gates"]
        else:
            maturity = MaturityLevel.LEVEL_0
            capabilities = ["Unverified legacy infrastructure"]
            next_reqs = ["Initialize baseline container and configuration verification"]

        return MaturityAssessment(
            maturity_level=maturity,
            maturity_score=round(score, 2),
            pillar_ratings=pillar_ratings,
            capabilities_achieved=capabilities,
            next_level_requirements=next_reqs,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
