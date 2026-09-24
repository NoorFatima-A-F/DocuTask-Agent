"""Compliance Audit Readiness Assessment and Gap Analysis."""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from .evaluator import ComplianceEvaluator, FrameworkComplianceScore


class ComplianceGap(BaseModel):
    framework: str
    control_id: str
    severity: str  # MEDIUM, HIGH, CRITICAL
    finding: str
    remediation_step: str


class AuditReadinessReport(BaseModel):
    tenant_id: str
    overall_readiness_score: float = 100.0  # 0.0 to 100.0
    audit_readiness_status: str = "AUDIT_READY" # AUDIT_READY, MINOR_GAPS, AT_RISK, NON_COMPLIANT
    framework_scores: Dict[str, FrameworkComplianceScore] = Field(default_factory=dict)
    identified_gaps: List[ComplianceGap] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ComplianceReportingEngine:
    """Generates comprehensive audit readiness assessments and gap analysis."""

    def __init__(self, evaluator: Optional[ComplianceEvaluator] = None):
        self.evaluator = evaluator or ComplianceEvaluator()

    def generate_audit_readiness_report(self, tenant_id: str = "*") -> AuditReadinessReport:
        framework_scores = self.evaluator.evaluate_all_frameworks(tenant_id=tenant_id)
        scores = [fs.score for fs in framework_scores.values()]
        avg_score = (sum(scores) / len(scores)) if scores else 100.0

        gaps: List[ComplianceGap] = []
        for fw_name, fs in framework_scores.items():
            for ctrl in fs.controls:
                if ctrl.status == "NON_COMPLIANT":
                    gaps.append(
                        ComplianceGap(
                            framework=fw_name,
                            control_id=ctrl.control_id,
                            severity="HIGH",
                            finding=f"Control {ctrl.control_id} ({ctrl.control_name}) recorded compliance failures.",
                            remediation_step=f"Inspect related safety and audit event logs for framework {fw_name}.",
                        )
                    )

        if avg_score >= 95.0 and not gaps:
            status = "AUDIT_READY"
        elif avg_score >= 80.0:
            status = "MINOR_GAPS"
        elif avg_score >= 60.0:
            status = "AT_RISK"
        else:
            status = "NON_COMPLIANT"

        return AuditReadinessReport(
            tenant_id=tenant_id,
            overall_readiness_score=round(avg_score, 2),
            audit_readiness_status=status,
            framework_scores=framework_scores,
            identified_gaps=gaps,
        )
