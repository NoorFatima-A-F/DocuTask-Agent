"""
Approval Workflow Engine.
Coordinates human-in-the-loop tasks, routing approvals or rejections to resume workflows.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.workflow.human_task import HumanTask, HumanTaskStatus


class ApprovalWorkflowEngine:
    """Manages pending human approval tasks and handles approval decisions."""

    def __init__(self):
        self._tasks: Dict[UUID, HumanTask] = {}

    def create_human_task(
        self, workflow_id: UUID, node_id: str, title: str, approvers: List[str], description: str = ""
    ) -> HumanTask:
        task = HumanTask(
            workflow_id=workflow_id,
            workflow_instance_id=workflow_id,
            node_id=node_id,
            title=title,
            approvers=approvers,
            assigned_user_or_role=approvers[0] if approvers else "reviewer",
            description=description,
        )
        self._tasks[task.task_id] = task
        return task

    def decide_task(self, task_id: UUID, decision: Any, reviewer_id: str, notes: str = "") -> Optional[HumanTask]:
        task = self._tasks.get(task_id)
        if not task:
            return None
        from app.agents.workflow.human_task import HumanTaskDecision

        is_approved = decision in (HumanTaskDecision.APPROVED, HumanTaskDecision.APPROVE, True, "APPROVED", "APPROVE")
        updated = task.approve(reviewer_id, notes) if is_approved else task.reject(reviewer_id, notes)
        updated.reviewer_id = reviewer_id
        updated.notes = notes
        self._tasks[task_id] = updated
        return updated

    def create_approval_task(self, instance_id: UUID, title: str, assigned_to: str, description: str = "") -> HumanTask:
        task = HumanTask(
            workflow_instance_id=instance_id, title=title, assigned_user_or_role=assigned_to, description=description
        )
        self._tasks[task.task_id] = task
        return task

    def record_decision(self, task_id: UUID, approved: bool, user_id: str, reason: str = "") -> Optional[HumanTask]:
        task = self._tasks.get(task_id)
        if not task:
            return None
        updated = task.approve(user_id, reason) if approved else task.reject(user_id, reason)
        self._tasks[task_id] = updated
        return updated

    def get_pending_tasks_for_user(self, user_or_role: str) -> List[HumanTask]:
        return [
            t
            for t in self._tasks.values()
            if t.assigned_user_or_role == user_or_role and t.status == HumanTaskStatus.PENDING
        ]
