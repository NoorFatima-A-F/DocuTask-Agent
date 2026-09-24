"""
Phase 3H.4.12.7: CI/CD Verification Gate Evaluator
"""
from datetime import datetime, timezone
from typing import List
from ..domain.interfaces import ICICDVerificationGate
from ..domain.models import (
    CICDGateReport,
    CICDDecision,
    CertificationTier,
    ObservabilityCertificationReport,
)


class CICDVerificationGate(ICICDVerificationGate):
    def evaluate_deployment_gate(
        self,
        certification_report: ObservabilityCertificationReport,
    ) -> CICDGateReport:
        tier = certification_report.certification_tier
        score = certification_report.composite_score
        blocking_reasons: List[str] = []

        if tier == CertificationTier.ENTERPRISE_CERTIFIED:
            decision = CICDDecision.DEPLOY
            exit_code = 0
        elif tier == CertificationTier.PRODUCTION_READY:
            decision = CICDDecision.DEPLOY
            exit_code = 0
        elif tier == CertificationTier.OPERATIONALLY_READY:
            decision = CICDDecision.DEPLOY_WITH_WARNING
            exit_code = 0
        elif tier == CertificationTier.CONDITIONALLY_READY:
            decision = CICDDecision.MANUAL_APPROVAL_REQUIRED
            exit_code = 2
            blocking_reasons.append("Conditional readiness requires manual signoff from Staff SRE.")
        else:
            decision = CICDDecision.DEPLOYMENT_BLOCKED
            exit_code = 1
            blocking_reasons.append(f"Certification failed (Score: {score}%). Production deployment blocked.")

        return CICDGateReport(
            gate_decision=decision,
            composite_score=score,
            tier=tier,
            hard_gates_passed=(decision in [CICDDecision.DEPLOY, CICDDecision.DEPLOY_WITH_WARNING]),
            blocking_reasons=blocking_reasons,
            pipeline_exit_code=exit_code,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
