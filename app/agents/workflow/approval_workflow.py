"""
Approval Workflow Engine.
Coordinates human-in-the-loop tasks, routing approvals or rejections to resume workflows.
"""

from typing import Dict, List, Optional
from uuid import UUID
from app.agents.workflow.human_task import HumanTask, HumanTaskStatus


class ApprovalWorkflowEngine:
    """Manages pending human approval tasks and handles approval decisions."""

    def __init__(self):
        self._tasks: Dict[UUID, HumanTask] = {}

    def create_approval_task(
        self,
        instance_id: UUID,
        title: str,
        assigned_to: str,
        description: str = ""
    ) -> HumanTask:
        task = HumanTask(
            workflow_instance_id=instance_id,
            title=title,
            assigned_user_or_role=assigned_to,
            description=description
        )
        self._tasks[task.task_id] = task
        return task

    def record_decision(
        self,
        task_id: UUID,
        approved: bool,
        user_id: str,
        reason: str = ""
    ) -> Optional[HumanTask]:
        task = self._tasks.get(task_id)
        if not task:
            return None
        updated = task.approve(user_id, reason) if approved else task.reject(user_id, reason)
        self._tasks[task_id] = updated
        return updated

    def get_pending_tasks_for_user(self, user_or_role: str) -> List[HumanTask]:
        return [
            t for t in self._tasks.values()
            if t.assigned_user_or_role == user_or_role and t.status == HumanTaskStatus.PENDING
        ]
