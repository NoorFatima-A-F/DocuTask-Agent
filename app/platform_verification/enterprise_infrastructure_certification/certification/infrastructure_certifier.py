"""
Phase 3O: Infrastructure Production Certifier & Decision Engine.
"""

from datetime import datetime, timezone
from typing import List

from ..domain.interfaces import IInfrastructureCertifier
from ..domain.models import (
    CertificationDecision,
    CertificationLevel,
    QualityScorecard,
    RiskAssessmentReport,
    VerificationStatus,
)


class InfrastructureCertifier(IInfrastructureCertifier):
    """
    Synthesizes multi-pillar scores with risk assessments to issue formal production readiness certifications.
    Enforces the Critical Risk Override: High/Critical risks automatically block deployment regardless of numerical score.
    """

    def evaluate_certification(
        self,
        scorecard: QualityScorecard,
        risk_report: RiskAssessmentReport,
    ) -> CertificationDecision:
        blockers: List[str] = []
        recommendations: List[str] = []

        # Check for Critical Risk Overrides
        if risk_report.production_blocker_present:
            for risk in risk_report.risks:
                if risk.is_blocker:
                    blockers.append(f"[{risk.risk_level.value}] {risk.title}: {risk.reason}")
                    recommendations.append(f"Remediate {risk.category}: {risk.remediation}")

        # Check category minimums (no single pillar should be catastrophic)
        for cat_name, cat_score in scorecard.categories.items():
            if cat_score.score < 60.0:
                blockers.append(f"Category '{cat_name}' score {cat_score.score:.1f}% below minimum viable threshold (60%).")
                recommendations.append(f"Prioritize re-architecting {cat_name} infrastructure.")
            elif cat_score.score < 90.0:
                recommendations.append(f"Improve {cat_name} test coverage to reach enterprise 95%+ standard.")

        # Determine certification level & approval
        if blockers:
            level = CertificationLevel.BLOCKED
            status = VerificationStatus.FAILED
            approved = False
        else:
            if scorecard.overall_score >= 95.0:
                level = CertificationLevel.ENTERPRISE_READY
                status = VerificationStatus.PASSED
                approved = True
                recommendations.append("Maintain continuous verification telemetry and automated regression gates.")
            elif scorecard.overall_score >= 90.0:
                level = CertificationLevel.PRODUCTION_READY
                status = VerificationStatus.PASSED
                approved = True
                recommendations.append("Schedule quarterly disaster recovery and soak performance reviews.")
            elif scorecard.overall_score >= 80.0:
                level = CertificationLevel.TESTING_READY
                status = VerificationStatus.WARNING
                approved = False
                blockers.append("Score below 90% production readiness threshold.")
            elif scorecard.overall_score >= 60.0:
                level = CertificationLevel.DEVELOPMENT_READY
                status = VerificationStatus.WARNING
                approved = False
                blockers.append("Score below 80% staging threshold.")
            else:
                level = CertificationLevel.BLOCKED
                status = VerificationStatus.FAILED
                approved = False
                blockers.append("Score below 60% development baseline.")

        cat_scores = {name: data.score for name, data in scorecard.categories.items()}
        risks_map = {
            "CRITICAL": risk_report.critical_risks_count,
            "HIGH": risk_report.high_risks_count,
            "MEDIUM": risk_report.medium_risks_count,
            "LOW": risk_report.low_risks_count,
        }

        return CertificationDecision(
            project="DocuTask Agent",
            overall_score=scorecard.overall_score,
            certification=level,
            status=status,
            deployment_approved=approved,
            blocker_reasons=blockers,
            recommendations=recommendations,
            categories=cat_scores,
            risks_summary=risks_map,
            issued_at=datetime.now(timezone.utc).isoformat(),
        )
