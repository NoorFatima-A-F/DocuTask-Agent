"""
Governance & Certification - Multi-Stage Governance Gate
Enforces approval workflows across automated checks, engineering signoff, and compliance.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict, field
import time


@dataclass
class GovernanceApprovalRecord:
    gate_id: str
    package_id: str
    stage: str  # AUTOMATED_CHECKS | PEER_REVIEW | COMPLIANCE_APPROVAL | DEPLOYED | REJECTED
    approver_role: str
    approver_identity: str
    comments: str
    approved_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GovernanceGateManager:
    """Manages governance gates and approval state transitions."""

    GATE_STAGES = [
        "AUTOMATED_CHECKS",
        "PEER_REVIEW",
        "COMPLIANCE_APPROVAL",
        "DEPLOYED",
    ]

    def __init__(self):
        self.approvals: Dict[str, List[GovernanceApprovalRecord]] = {}

    def record_signoff(
        self,
        package_id: str,
        stage: str,
        approver_role: str,
        approver_identity: str,
        comments: str = "",
    ) -> GovernanceApprovalRecord:
        if stage not in self.GATE_STAGES and stage != "REJECTED":
            raise ValueError(f"Unknown gate stage: {stage}")

        rec = GovernanceApprovalRecord(
            gate_id=f"gate_{stage.lower()}_{int(time.time())}",
            package_id=package_id,
            stage=stage,
            approver_role=approver_role,
            approver_identity=approver_identity,
            comments=comments,
        )

        if package_id not in self.approvals:
            self.approvals[package_id] = []
        self.approvals[package_id].append(rec)
        return rec

    def get_package_approval_status(self, package_id: str) -> Dict[str, Any]:
        history = self.approvals.get(package_id, [])
        stages_passed = [r.stage for r in history if r.stage != "REJECTED"]
        is_rejected = any(r.stage == "REJECTED" for r in history)

        current_stage = history[-1].stage if history else "PENDING_AUTOMATED_CHECKS"

        return {
            "package_id": package_id,
            "current_stage": current_stage,
            "stages_passed": stages_passed,
            "is_fully_approved": "DEPLOYED" in stages_passed,
            "is_rejected": is_rejected,
            "approval_count": len(history),
            "history": [r.to_dict() for r in history],
        }
