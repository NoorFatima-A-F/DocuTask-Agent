"""
Phase 3O: Infrastructure Risk Assessment Engine.
"""

from datetime import datetime, timezone
from typing import List

from ..domain.interfaces import IInfrastructureRiskAnalyzer
from ..domain.models import (
    NormalizedEvidenceItem,
    QualityScorecard,
    RiskAssessmentReport,
    RiskFinding,
    RiskLevel,
    VerificationStatus,
)


class InfrastructureRiskAnalyzer(IInfrastructureRiskAnalyzer):
    """
    Evaluates evidence findings to detect operational risks, security exposures,
    and automatic deployment failure conditions (Critical Risk Overrides).
    """

    def assess_risks(
        self,
        scorecard: QualityScorecard,
        evidence_items: List[NormalizedEvidenceItem],
    ) -> RiskAssessmentReport:
        findings: List[RiskFinding] = []

        for item in evidence_items:
            if item.status == VerificationStatus.FAILED or item.severity in [RiskLevel.CRITICAL, RiskLevel.HIGH, RiskLevel.MEDIUM]:
                is_blocker = item.severity in [RiskLevel.CRITICAL, RiskLevel.HIGH]
                findings.append(
                    RiskFinding(
                        risk_level=item.severity,
                        category=item.category,
                        title=f"Failure in {item.name}",
                        reason=item.details or f"Check {item.test_id} failed verification.",
                        impact=self._derive_impact(item.category, item.severity),
                        remediation=self._derive_remediation(item.category, item.name),
                        is_blocker=is_blocker,
                    )
                )

        critical_count = sum(1 for f in findings if f.risk_level == RiskLevel.CRITICAL)
        high_count = sum(1 for f in findings if f.risk_level == RiskLevel.HIGH)
        medium_count = sum(1 for f in findings if f.risk_level == RiskLevel.MEDIUM)
        low_count = sum(1 for f in findings if f.risk_level == RiskLevel.LOW)

        if critical_count > 0:
            highest = RiskLevel.CRITICAL
        elif high_count > 0:
            highest = RiskLevel.HIGH
        elif medium_count > 0:
            highest = RiskLevel.MEDIUM
        elif low_count > 0:
            highest = RiskLevel.LOW
        else:
            highest = RiskLevel.NONE

        blocker_present = critical_count > 0 or high_count > 0

        return RiskAssessmentReport(
            highest_risk=highest,
            total_risks=len(findings),
            critical_risks_count=critical_count,
            high_risks_count=high_count,
            medium_risks_count=medium_count,
            low_risks_count=low_count,
            production_blocker_present=blocker_present,
            risks=findings,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

    def _derive_impact(self, category: str, severity: RiskLevel) -> str:
        if severity == RiskLevel.CRITICAL:
            return "Immediate threat of data loss, service outage, or security breach in production."
        if severity == RiskLevel.HIGH:
            return "Potential service degradation or compliance violation under peak workload."
        if severity == RiskLevel.MEDIUM:
            return "Sub-optimal performance or slower recovery SLA during incident response."
        return "Minor operational variance with no direct SLA impact."

    def _derive_remediation(self, category: str, name: str) -> str:
        if "security" in category.lower():
            return "Harden security controls, rotate compromised secrets, and apply latest patches."
        if "recovery" in category.lower() or "backup" in category.lower():
            return "Verify backup snapshots, re-test point-in-time restore, and audit replica integrity."
        if "scalability" in category.lower():
            return "Tune connection pools, scale worker replicas, and optimize query indexing."
        return "Inspect component telemetry logs and adjust operational configuration."
