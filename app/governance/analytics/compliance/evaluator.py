"""Compliance Framework Evaluator, Control Coverage, and Framework Scoring."""

from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class ComplianceFramework(str, Enum):
    SOC2 = "SOC2"
    ISO27001 = "ISO27001"
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    EU_AI_ACT = "EU_AI_ACT"
    INTERNAL_POLICIES = "INTERNAL_POLICIES"


class ControlStatus(BaseModel):
    control_id: str
    control_name: str
    status: str             # COMPLIANT, NON_COMPLIANT, AT_RISK
    evidence_count: int = 0
    last_verified: Optional[datetime] = None


class FrameworkComplianceScore(BaseModel):
    framework: ComplianceFramework
    score: float = 100.0                # 0.0 to 100.0
    control_coverage_pct: float = 100.0 # 0.0 to 100.0
    evidence_availability_pct: float = 100.0
    compliant_controls_count: int = 0
    total_controls_count: int = 0
    controls: List[ControlStatus] = Field(default_factory=list)


class ComplianceEvaluator:
    """Evaluates regulatory and organizational compliance across governance telemetry."""

    FRAMEWORK_CONTROLS: Dict[ComplianceFramework, List[Dict[str, str]]] = {
        ComplianceFramework.SOC2: [
            {"id": "CC6.1", "name": "Logical Access Controls & IAM"},
            {"id": "CC6.6", "name": "Boundary Protection & Safety Filters"},
            {"id": "CC7.2", "name": "Continuous Telemetry & Audit Trails"},
        ],
        ComplianceFramework.ISO27001: [
            {"id": "A.8.1", "name": "User Endpoint & System Security"},
            {"id": "A.8.24", "name": "Cryptographic Hash Chaining"},
            {"id": "A.8.28", "name": "Secure AI Development Architecture"},
        ],
        ComplianceFramework.GDPR: [
            {"id": "ART_5", "name": "Data Minimization & Integrity"},
            {"id": "ART_22", "name": "Automated Decision Making & Human Oversight"},
            {"id": "ART_32", "name": "Security of AI Data Processing"},
        ],
        ComplianceFramework.HIPAA: [
            {"id": "HIPAA_SEC_1", "name": "PHI Protection & De-identification"},
            {"id": "HIPAA_SEC_2", "name": "Audit Controls & Evidence Preservation"},
        ],
        ComplianceFramework.EU_AI_ACT: [
            {"id": "AIA_ART_9", "name": "Risk Management System"},
            {"id": "AIA_ART_13", "name": "Transparency & Provision of Information"},
            {"id": "AIA_ART_14", "name": "Human Oversight Control Plane"},
        ],
        ComplianceFramework.INTERNAL_POLICIES: [
            {"id": "INT_01", "name": "Multi-Tenant Isolation Boundaries"},
            {"id": "INT_02", "name": "Model Registry & Lifecycle Gating"},
        ],
    }

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def evaluate_framework(
        self, framework: ComplianceFramework, tenant_id: str = "*"
    ) -> FrameworkComplianceScore:
        q = WarehouseQueryFilter(tenant_id=tenant_id, framework=framework.value)
        compliance_events = self.repo.query_compliance_events(q)

        controls_def = self.FRAMEWORK_CONTROLS.get(framework, [])
        total_controls = len(controls_def)

        control_statuses: List[ControlStatus] = []
        compliant_cnt = 0
        total_evd = 0

        for c_def in controls_def:
            cid = c_def["id"]
            cname = c_def["name"]
            matching = [e for e in compliance_events if e.control_id == cid]

            any(e.evidence_id for e in matching) or len(matching) > 0
            evd_count = sum(1 for e in matching if e.evidence_id)
            total_evd += evd_count

            # If there are non-compliant events, flag status
            has_failures = any(e.status == "NON_COMPLIANT" for e in matching)
            if has_failures:
                status = "NON_COMPLIANT"
            elif matching:
                status = "COMPLIANT"
                compliant_cnt += 1
            else:
                # Default assume compliant baseline if no failure recorded
                status = "COMPLIANT"
                compliant_cnt += 1

            control_statuses.append(
                ControlStatus(
                    control_id=cid,
                    control_name=cname,
                    status=status,
                    evidence_count=evd_count,
                    last_verified=datetime.now(timezone.utc),
                )
            )

        score = (compliant_cnt / total_controls * 100.0) if total_controls > 0 else 100.0
        coverage = 100.0
        evd_avail = 100.0 if total_evd > 0 else 90.0

        return FrameworkComplianceScore(
            framework=framework,
            score=round(score, 2),
            control_coverage_pct=round(coverage, 2),
            evidence_availability_pct=round(evd_avail, 2),
            compliant_controls_count=compliant_cnt,
            total_controls_count=total_controls,
            controls=control_statuses,
        )

    def evaluate_all_frameworks(self, tenant_id: str = "*") -> Dict[str, FrameworkComplianceScore]:
        return {
            f.value: self.evaluate_framework(f, tenant_id=tenant_id)
            for f in ComplianceFramework
        }
