"""
Phase 3H.4.11.11: Certification Decision Engine
"""
from typing import List
from ..domain.interfaces import ICertificationDecisionEngine
from ..domain.models import (
    CertificationResult,
    CertificationStatus,
    MaturityReport,
    OperationalRiskReport,
)


class CertificationDecisionEngine(ICertificationDecisionEngine):
    def evaluate_certification(
        self,
        composite_score: float,
        maturity_report: MaturityReport,
        risk_report: OperationalRiskReport,
    ) -> CertificationResult:
        blocking_issues: List[str] = [
            f"[{r.risk_id}] {r.description}" for r in risk_report.evaluated_risks if r.is_blocking
        ]

        if not risk_report.hard_gate_passed or composite_score < 80.0:
            status = CertificationStatus.FAILED_BLOCKED
            approved = False
        elif composite_score >= 95.0:
            status = CertificationStatus.ENTERPRISE_OBSERVABILITY_READY
            approved = True
        elif composite_score >= 90.0:
            status = CertificationStatus.PRODUCTION_READY
            approved = True
        else:
            status = CertificationStatus.IMPROVEMENT_REQUIRED
            approved = False

        return CertificationResult(
            certification=status,
            composite_score=round(composite_score, 2),
            risk_level=risk_report.overall_risk,
            maturity_level=maturity_report.level,
            release_approved=approved,
            blocking_issues=blocking_issues,
        )
