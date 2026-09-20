"""
AMAEOP Pillar 1 - Hierarchy & Escalation Manager
Manages organizational reporting structures, escalation trees, and dynamic chain-of-command routing.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from app.runtime.organization.department import CANONICAL_DEPARTMENTS


@dataclass
class EscalationPath:
    origin_department_id: str
    escalation_reason: str
    target_department_id: str
    approver_role: str
    max_resolution_time_sec: float
    fallback_policy: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HierarchyManager:
    """Evaluates reporting hierarchies, escalation pathways, and supervisor delegation."""

    @classmethod
    def get_escalation_path(cls, origin_department_id: str, issue_severity: str = "HIGH") -> EscalationPath:
        if issue_severity == "CRITICAL" or origin_department_id == "dept_governance":
            return EscalationPath(
                origin_department_id=origin_department_id,
                escalation_reason=f"{issue_severity} severity operational exception",
                target_department_id="dept_executive",
                approver_role="Chief Executive Agent",
                max_resolution_time_sec=60.0,
                fallback_policy="SAFE_CIRCUIT_BREAK_AND_NOTIFY_HUMAN_SUPERVISOR",
            )
        elif origin_department_id in ["dept_ocr", "dept_extraction"]:
            return EscalationPath(
                origin_department_id=origin_department_id,
                escalation_reason="Document parsing anomaly or token quota breach",
                target_department_id="dept_research",
                approver_role="Director of Autonomous Research",
                max_resolution_time_sec=120.0,
                fallback_policy="ROUTE_TO_FLASH_LITE_WITH_PROMPT_DEGRADATION",
            )
        else:
            return EscalationPath(
                origin_department_id=origin_department_id,
                escalation_reason="Standard verification or memory conflict",
                target_department_id="dept_qa",
                approver_role="Lead QA Sentinel",
                max_resolution_time_sec=180.0,
                fallback_policy="REPLAY_VALIDATION_WITH_EXPONENTIAL_BACKOFF",
            )

    @classmethod
    def get_reporting_chain(cls, department_id: str) -> List[Dict[str, str]]:
        chain = []
        curr = department_id
        while curr:
            dept = CANONICAL_DEPARTMENTS.get(curr)
            if not dept:
                break
            chain.append({"department_id": dept.department_id, "name": dept.name, "head": dept.head_agent})
            curr = dept.parent_department_id
        return chain
