"""Compliance Evidence Mapping & Assessment Engine."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from ..storage.repository import AuditRepository
from ..evidence.manager import EvidenceManager
from .frameworks import ComplianceFramework, FRAMEWORK_PROFILES
from .controls import ComplianceControl, ControlStatus, DEFAULT_COMPLIANCE_CONTROLS


class ControlEvaluationResult(BaseModel):
    control: ComplianceControl
    status: ControlStatus
    evidence_count: int
    matching_events_count: int
    missing_evidence: List[str] = Field(default_factory=list)
    risk_level: str = "LOW"
    recommendations: List[str] = Field(default_factory=list)


class ComplianceAssessmentReport(BaseModel):
    tenant_id: str
    framework: ComplianceFramework
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    overall_compliance_score: float  # 0.0 to 100.0%
    total_controls: int
    compliant_controls: int
    non_compliant_controls: int
    control_evaluations: List[ControlEvaluationResult] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class ComplianceAssessmentEngine:
    """Evaluates audit trails and evidence artifacts against compliance frameworks."""

    def __init__(
        self,
        repository: Optional[AuditRepository] = None,
        evidence_manager: Optional[EvidenceManager] = None,
        controls: Optional[List[ComplianceControl]] = None,
    ):
        self.repository = repository or AuditRepository()
        self.evidence_manager = evidence_manager or EvidenceManager(self.repository)
        self.controls = controls or list(DEFAULT_COMPLIANCE_CONTROLS)

    def evaluate_compliance(
        self,
        tenant_id: str,
        framework: ComplianceFramework,
    ) -> ComplianceAssessmentReport:
        tenant_events = self.repository.list_by_tenant(tenant_id)
        tenant_artifacts = self.evidence_manager.list_artifacts(tenant_id)

        framework_controls = [c for c in self.controls if c.framework == framework]
        if not framework_controls:
            framework_controls = [c for c in DEFAULT_COMPLIANCE_CONTROLS if c.framework == framework]

        evaluations: List[ControlEvaluationResult] = []
        compliant_count = 0

        for ctrl in framework_controls:
            # Check matching events by category/type
            matching_events = [
                e for e in tenant_events
                if e.category.value in ctrl.required_evidence_types or e.event_type in ctrl.required_evidence_types
            ]
            # Check matching artifacts
            matching_artifacts = [
                a for a in tenant_artifacts
                if a.evidence_type.value in ctrl.required_evidence_types
            ]

            total_evidence = len(matching_events) + len(matching_artifacts)
            missing: List[str] = []

            for req in ctrl.required_evidence_types:
                has_req = any(e.category.value == req or e.event_type == req for e in matching_events) or \
                          any(a.evidence_type.value == req for a in matching_artifacts)
                if not has_req:
                    missing.append(f"Missing evidence type '{req}'")

            if total_evidence > 0 and len(missing) == 0:
                status = ControlStatus.COMPLIANT
                risk = "LOW"
                recs = []
                compliant_count += 1
            elif total_evidence > 0:
                status = ControlStatus.PARTIALLY_COMPLIANT
                risk = "MEDIUM"
                recs = [f"Collect additional evidence for requirement: {m}" for m in missing]
            else:
                # If there are simply no events yet recorded in this category
                status = ControlStatus.PENDING_REVIEW if len(tenant_events) == 0 else ControlStatus.NON_COMPLIANT
                risk = "HIGH" if status == ControlStatus.NON_COMPLIANT else "LOW"
                recs = [f"Implement logging and evidence collection for {ctrl.title}"]
                if status == ControlStatus.PENDING_REVIEW:
                    compliant_count += 1  # Give clean slate if no events yet

            evaluations.append(
                ControlEvaluationResult(
                    control=ctrl,
                    status=status,
                    evidence_count=len(matching_artifacts),
                    matching_events_count=len(matching_events),
                    missing_evidence=missing,
                    risk_level=risk,
                    recommendations=recs,
                )
            )

        total_ctrls = len(framework_controls)
        score = (compliant_count / total_ctrls * 100.0) if total_ctrls > 0 else 100.0

        return ComplianceAssessmentReport(
            tenant_id=tenant_id,
            framework=framework,
            overall_compliance_score=round(score, 1),
            total_controls=total_ctrls,
            compliant_controls=compliant_count,
            non_compliant_controls=total_ctrls - compliant_count,
            control_evaluations=evaluations,
            recommendations=[r for e in evaluations for r in e.recommendations if r],
        )
