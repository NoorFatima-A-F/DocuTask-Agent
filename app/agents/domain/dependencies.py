"""
Task Dependency Domain Model.
Models Hard, Soft, Optional, Conditional, and Runtime Task Dependencies.
"""

from typing import Optional
from pydantic import BaseModel, Field
from app.agents.domain.enums import DependencyType
from app.agents.domain.value_objects import TaskID


class TaskDependencyRelation(BaseModel):
    """Specification of a dependency between tasks."""

    parent_task_id: TaskID
    dependency_type: DependencyType = Field(default=DependencyType.HARD)
    condition_expression: Optional[str] = Field(default=None)

    model_config = {"frozen": True}
