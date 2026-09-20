"""
Approval Executor.
Manages human-in-the-loop approval gates in the execution graph.
"""

from app.agents.planning.approvals import PlanApprovalGate


class ApprovalExecutor:
    """Evaluates approval gate clearance before execution proceeds."""

    def is_approved(self, gate: PlanApprovalGate) -> bool:
        return gate.is_approved
