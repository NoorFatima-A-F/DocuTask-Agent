"""
Enterprise Human Task & Approval Engine.
Coordinates human-in-the-loop task assignments, escalations, voting aggregation, and state resolution.
"""

from typing import Dict, List, Optional
from .models import ApprovalRequest, ApprovalStatus, ApprovalType, ApprovalVote
from ..domain.exceptions import WorkflowExecutionException


class ApprovalEngine:
    """Manages human approval requests, multi-party votes, and task delegation."""

    def __init__(self):
        # Key: request_id -> ApprovalRequest
        self._requests: Dict[str, ApprovalRequest] = {}
        # Key: execution_id -> List of request_ids
        self._execution_requests: Dict[str, List[str]] = {}

    def create_approval_request(
        self,
        execution_id: str,
        task_id: str,
        required_role: str = "manager",
        approval_type: ApprovalType = ApprovalType.SINGLE,
        min_approvals: int = 1,
        assigned_to: Optional[str] = None,
    ) -> ApprovalRequest:
        """Create a new human approval gate."""
        req = ApprovalRequest(
            execution_id=execution_id,
            task_id=task_id,
            required_role=required_role,
            approval_type=approval_type,
            min_approvals=min_approvals,
            assigned_to=assigned_to,
        )
        self._requests[req.request_id] = req
        if execution_id not in self._execution_requests:
            self._execution_requests[execution_id] = []
        self._execution_requests[execution_id].append(req.request_id)
        return req

    def submit_vote(
        self,
        request_id: str,
        approver: str,
        decision: ApprovalStatus,
        comment: str = "",
    ) -> ApprovalRequest:
        """Submit a vote for an approval request and evaluate consensus."""
        req = self._requests.get(request_id)
        if not req:
            raise WorkflowExecutionException(f"Approval request '{request_id}' not found")

        if req.status != ApprovalStatus.PENDING:
            raise WorkflowExecutionException(f"Approval request '{request_id}' is already finalized with status: {req.status.value}")

        vote = ApprovalVote(approver=approver, decision=decision, comment=comment)
        req.votes.append(vote)

        # Evaluate consensus
        approvals = [v for v in req.votes if v.decision == ApprovalStatus.APPROVED]
        rejections = [v for v in req.votes if v.decision == ApprovalStatus.REJECTED]

        if decision == ApprovalStatus.REJECTED and req.approval_type in (ApprovalType.SINGLE, ApprovalType.SEQUENTIAL):
            req.status = ApprovalStatus.REJECTED
        elif len(approvals) >= req.min_approvals:
            req.status = ApprovalStatus.APPROVED
        elif req.approval_type == ApprovalType.MAJORITY_VOTE:
            if len(approvals) > len(rejections) and len(req.votes) >= req.min_approvals:
                req.status = ApprovalStatus.APPROVED
            elif len(rejections) >= req.min_approvals:
                req.status = ApprovalStatus.REJECTED

        return req

    def get_request(self, request_id: str) -> Optional[ApprovalRequest]:
        return self._requests.get(request_id)

    def get_pending_for_execution(self, execution_id: str) -> List[ApprovalRequest]:
        req_ids = self._execution_requests.get(execution_id, [])
        return [self._requests[rid] for rid in req_ids if self._requests[rid].status == ApprovalStatus.PENDING]
