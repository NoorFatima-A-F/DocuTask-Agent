"""
Phase 13.20: Enterprise Multi-Stage Approval Workflow Engine.
Governs agent progression: Submit -> Security Review -> Business Owner Signoff -> Compliance Verification -> Production.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
from app.platform_ai_lifecycle.models.schemas import (
    AgentApproval,
    ApprovalStage,
    ApprovalDecision,
)


class ApprovalWorkflowEngine:
    def __init__(self):
        self._approvals: Dict[str, List[AgentApproval]] = {}
        self._seed_default_approvals()

    def _seed_default_approvals(self) -> None:
        ap1 = AgentApproval(
            approval_id="appr_01",
            agent_id="agt_acme_invoice_reconciler",
            version_tag="1.2.0",
            stage=ApprovalStage.FINAL_RELEASE,
            decision=ApprovalDecision.APPROVED,
            approver_id="usr_acme_admin",
            approver_email="admin@acmecorp.com",
            comments="Verified benchmark accuracy >=97% and SOC2 compliance passed.",
        )
        self._approvals["agt_acme_invoice_reconciler"] = [ap1]

    def submit_for_approval(
        self,
        agent_id: str,
        version_tag: str,
        submitter_id: str,
        submitter_email: str,
    ) -> AgentApproval:
        appr_id = f"appr_{uuid.uuid4().hex[:8]}"
        record = AgentApproval(
            approval_id=appr_id,
            agent_id=agent_id,
            version_tag=version_tag,
            stage=ApprovalStage.DEVELOPER_SUBMIT,
            decision=ApprovalDecision.PENDING,
            approver_id=submitter_id,
            approver_email=submitter_email,
            comments="Submitted by developer for automated & compliance review.",
        )
        if agent_id not in self._approvals:
            self._approvals[agent_id] = []
        self._approvals[agent_id].append(record)
        return record

    def review_and_decide(
        self,
        approval_id: str,
        stage: ApprovalStage,
        decision: ApprovalDecision,
        approver_id: str,
        approver_email: str,
        comments: str = "",
    ) -> AgentApproval:
        for app_list in self._approvals.values():
            for rec in app_list:
                if rec.approval_id == approval_id:
                    rec.stage = stage
                    rec.decision = decision
                    rec.approver_id = approver_id
                    rec.approver_email = approver_email
                    rec.comments = comments
                    rec.timestamp = datetime.now(timezone.utc).isoformat()
                    return rec
        raise ValueError(f"Approval record {approval_id} not found")

    def list_approvals(self, agent_id: str) -> List[AgentApproval]:
        return self._approvals.get(agent_id, [])
