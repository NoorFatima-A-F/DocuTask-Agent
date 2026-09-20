"""
Task Assignment Models.
Defines assignment envelopes, matrices, and allocation states.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TaskAssignment(BaseModel):
    """Assignment of a task to a specific agent with timestamp and lease parameters."""
    assignment_id: UUID = Field(default_factory=uuid4)
    task_id: str
    assigned_agent_id: UUID
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    model_config = {"frozen": True}


class AssignmentMatrix(BaseModel):
    """Current matrix of all task-to-agent assignments."""
    assignments: Dict[str, TaskAssignment] = Field(default_factory=dict)

    def assign(self, task_id: str, agent_id: UUID) -> TaskAssignment:
        assignment = TaskAssignment(task_id=task_id, assigned_agent_id=agent_id)
        self.assignments[task_id] = assignment
        return assignment

    def unassign(self, task_id: str) -> None:
        if task_id in self.assignments:
            del self.assignments[task_id]
