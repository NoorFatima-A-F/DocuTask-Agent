"""
Phase 13.19: Human Collaboration & Approval Center.
Manages human-in-the-loop task queues, approvals, rejections, and role delegations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.runtime.business.models.schemas import (
    HumanApprovalTask,
    ApprovalStatus,
)


class HumanCollaborationEngine:
    def __init__(self):
        self._tasks: Dict[str, HumanApprovalTask] = {}
        self._seed_default_tasks()

    def _seed_default_tasks(self) -> None:
        """Seeds default human approval queue items."""
        t1 = HumanApprovalTask(
            task_id="appr_inv_9941",
            process_id="proc_invoice_enterprise_01",
            step_id="step_manager_approval",
            title="Invoice $45,000.00 Review (Vendor: Acme Global Tech)",
            description="Invoice amount exceeds standard $10k auto-approval threshold. Line items verified by AI Agent with 99.4% confidence.",
            department_id="dept_finance",
            assigned_role="role_finance_director",
            amount=45000.0,
            status=ApprovalStatus.PENDING,
        )
        self._tasks[t1.task_id] = t1

    def create_approval_task(self, task: HumanApprovalTask) -> HumanApprovalTask:
        task.created_at = datetime.now(timezone.utc).isoformat()
        self._tasks[task.task_id] = task
        return task

    def get_task(self, task_id: str) -> Optional[HumanApprovalTask]:
        return self._tasks.get(task_id)

    def list_tasks(self, status: Optional[ApprovalStatus] = None) -> List[HumanApprovalTask]:
        if status:
            return [t for t in self._tasks.values() if t.status == status]
        return list(self._tasks.values())

    def decide_task(self, task_id: str, decision: ApprovalStatus, rationale: str, decided_by: str) -> HumanApprovalTask:
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Approval task {task_id} not found")

        task.status = decision
        task.decision_rationale = rationale
        task.decided_by = decided_by
        task.decided_at = datetime.now(timezone.utc).isoformat()
        return task
