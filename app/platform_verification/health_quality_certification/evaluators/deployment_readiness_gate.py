"""
Phase 3H.5.11.5 & 3H.5.11.9: Production Readiness Deployment Gatekeeper
"""
from typing import List
from ..domain.models import (
    DeploymentGateReport,
    DeploymentGateCheckItem,
    DeploymentDecision,
    SREReliabilityMetrics,
    RegressionReport,
)
from ..domain.interfaces import IDeploymentGatekeeper


class DeploymentReadinessGate(IDeploymentGatekeeper):
    """
    Evaluates CI/CD deployment readiness based on:
    - Minimum overall score >= 90.0
    - Critical requirements mandatory pass (Liveness >= 90, Readiness >= 90, Security >= 95, Failure Detection >= 90)
    - Zero score regression block
    - SRE Availability SLO compliance
    """

    def __init__(self, minimum_score: float = 90.0, block_on_failure: bool = True):
        self.minimum_score = minimum_score
        self.block_on_failure = block_on_failure

    def evaluate_deployment_gate(
        self,
        overall_score: float,
        liveness_score: float,
        readiness_score: float,
        security_score: float,
        failure_detection_score: float,
        sre_metrics: SREReliabilityMetrics,
        regression_report: RegressionReport,
    ) -> DeploymentGateReport:
        checks: List[DeploymentGateCheckItem] = []

        # 1. Overall Score Check
        overall_passed = overall_score >= self.minimum_score
        checks.append(
            DeploymentGateCheckItem(
                check_name="Overall Quality Score Threshold",
                required_threshold=f">= {self.minimum_score}%",
                actual_value=f"{overall_score:.2f}%",
                passed=overall_passed,
                is_critical_requirement=True,
            )
        )

        # 2. Critical Pillar: Liveness
        liveness_passed = liveness_score >= 90.0
        checks.append(
            DeploymentGateCheckItem(
                check_name="Critical Pillar: Liveness Reliability",
                required_threshold=">= 90.0%",
                actual_value=f"{liveness_score:.2f}%",
                passed=liveness_passed,
                is_critical_requirement=True,
            )
        )

        # 3. Critical Pillar: Readiness
        readiness_passed = readiness_score >= 90.0
        checks.append(
            DeploymentGateCheckItem(
                check_name="Critical Pillar: Readiness Accuracy",
                required_threshold=">= 90.0%",
                actual_value=f"{readiness_score:.2f}%",
                passed=readiness_passed,
                is_critical_requirement=True,
            )
        )

        # 4. Critical Pillar: Security
        security_passed = security_score >= 95.0
        checks.append(
            DeploymentGateCheckItem(
                check_name="Critical Pillar: Security & Secret Sanitization",
                required_threshold=">= 95.0%",
                actual_value=f"{security_score:.2f}%",
                passed=security_passed,
                is_critical_requirement=True,
            )
        )

        # 5. Critical Pillar: Failure Detection
        detection_passed = failure_detection_score >= 90.0
        checks.append(
            DeploymentGateCheckItem(
                check_name="Critical Pillar: Failure Detection MTTD",
                required_threshold=">= 90.0%",
                actual_value=f"{failure_detection_score:.2f}%",
                passed=detection_passed,
                is_critical_requirement=True,
            )
        )

        # 6. SRE SLO Compliance
        slo_passed = sre_metrics.slo_compliant
        checks.append(
            DeploymentGateCheckItem(
                check_name="SRE Availability SLO (99.9%)",
                required_threshold=">= 99.90%",
                actual_value=f"{sre_metrics.availability_pct:.2f}%",
                passed=slo_passed,
                is_critical_requirement=False,
            )
        )

        # 7. Regression Policy
        regression_passed = regression_report.regression_policy_passed
        checks.append(
            DeploymentGateCheckItem(
                check_name="Quality Regression Policy",
                required_threshold="Delta >= -2.0%",
                actual_value=f"{regression_report.overall_delta:+.2f}%",
                passed=regression_passed,
                is_critical_requirement=True,
            )
        )

        critical_met = all(c.passed for c in checks if c.is_critical_requirement)
        all_passed = all(c.passed for c in checks)

        if all_passed and critical_met:
            decision = DeploymentDecision.APPROVED
            reason = "All production readiness checks, SRE metrics, and quality gates successfully passed."
        elif critical_met:
            decision = DeploymentDecision.ESCALATION_REQUIRED
            reason = "Critical requirements met, but non-critical warning triggered."
        else:
            decision = DeploymentDecision.BLOCKED
            reason = "One or more critical production readiness requirements failed."

        return DeploymentGateReport(
            report_title="Production Readiness Deployment Gate Report",
            deployment_id="deploy-prod-3h511",
            minimum_score_required=self.minimum_score,
            actual_score=round(overall_score, 2),
            critical_requirements_met=critical_met,
            block_on_failure=self.block_on_failure,
            decision=decision,
            checks=checks,
            reason=reason,
        )
