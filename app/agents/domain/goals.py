"""
Strongly Typed Goal Domain Model & Aggregates.
Represents structured business and technical execution objectives, priorities, constraints, sub-goals, and metadata.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

from app.agents.domain.constraints import DomainConstraint
from app.agents.domain.enums import GoalType, PriorityLevel
from app.agents.domain.policies import ExecutionPolicy
from app.agents.domain.value_objects import (
    CorrelationID,
    ExecutionID,
    GoalID,
    WorkflowID,
)


class GoalMetadata(BaseModel):
    """Immutable Goal Audit & Traceability Metadata."""

    document_id: Optional[UUID] = Field(default=None)
    user_id: Optional[UUID] = Field(default=None)
    correlation_id: CorrelationID = Field(default_factory=CorrelationID)
    workflow_id: Optional[WorkflowID] = Field(default=None)
    execution_id: Optional[ExecutionID] = Field(default=None)
    tenant_id: str = Field(default="default")
    tags: List[str] = Field(default_factory=list)
    labels: Dict[str, str] = Field(default_factory=dict)
    version: str = Field(default="v1.0")
    custom_metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class Goal(BaseModel):
    """
    Strongly Typed Goal Aggregate.
    Represents an objective statement, goal type, priority, constraints, and sub-goals.
    """

    goal_id: GoalID = Field(default_factory=GoalID)
    statement: str
    goal_type: GoalType = Field(default=GoalType.BUSINESS)
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    is_active: bool = Field(default=True)
    
    owner: str = Field(default="system")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deadline: Optional[datetime] = Field(default=None)
    
    constraints: List[DomainConstraint] = Field(default_factory=list)
    expected_outputs: List[str] = Field(default_factory=list)
    execution_policy: ExecutionPolicy = Field(default_factory=ExecutionPolicy)
    metadata: GoalMetadata = Field(default_factory=GoalMetadata)
    
    # Sub-goals for composite goals
    sub_goals: List["Goal"] = Field(default_factory=list)

    model_config = {"frozen": True}

    def add_sub_goal(self, sub_goal: "Goal") -> "Goal":
        """Returns a new Goal instance with the added sub-goal."""
        new_sub_goals = list(self.sub_goals)
        new_sub_goals.append(sub_goal)
        return Goal(
            goal_id=self.goal_id,
            statement=self.statement,
            goal_type=self.goal_type,
            priority=self.priority,
            is_active=self.is_active,
            owner=self.owner,
            created_at=self.created_at,
            deadline=self.deadline,
            constraints=self.constraints,
            expected_outputs=self.expected_outputs,
            execution_policy=self.execution_policy,
            metadata=self.metadata,
            sub_goals=new_sub_goals
        )
