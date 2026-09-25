"""
Strongly Typed Execution Result Domain Models.
Eliminates arbitrary dictionary returns by providing serializable, strongly typed result contracts.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.agents.domain.artifacts import ExecutionArtifact
from app.agents.domain.enums import ResultStatus
from app.agents.domain.value_objects import (
    ConfidenceScore,
    ExecutionCost,
    ExecutionDuration,
    RetryCount,
    TokenUsage,
)


class BaseDomainResult(BaseModel):
    """Base domain result contract."""
    status: ResultStatus = Field(default=ResultStatus.SUCCESS)
    success: bool = Field(default=True)
    failure_reason: Optional[str] = Field(default=None)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    confidence: ConfidenceScore = Field(default_factory=ConfidenceScore)
    duration: ExecutionDuration = Field(default_factory=ExecutionDuration)
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    retry_count: RetryCount = Field(default_factory=RetryCount)
    artifacts: List[ExecutionArtifact] = Field(default_factory=list)
    cost: ExecutionCost = Field(default_factory=ExecutionCost)
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    next_suggested_action: Optional[str] = Field(default=None)


class PlanningResult(BaseDomainResult):
    """Result of agent goal planning phase."""
    plan_steps: List[Dict[str, Any]] = Field(default_factory=list)


class ExecutionResult(BaseDomainResult):
    """Result of step execution phase."""
    executed_step_count: int = Field(default=0, ge=0)


class ObservationResult(BaseDomainResult):
    """Result of environment observation phase."""
    environment_feedback: Dict[str, Any] = Field(default_factory=dict)


class ReflectionResult(BaseDomainResult):
    """Result of self-reflection phase."""
    quality_score: float = Field(default=1.0, ge=0.0, le=1.0)
    requires_replanning: bool = Field(default=False)


class RecoveryResult(BaseDomainResult):
    """Result of error recovery phase."""
    recovered_successfully: bool = Field(default=False)
    recovery_action_taken: str = Field(default="NONE")


class TaskResult(BaseDomainResult):
    """Result of a single task execution."""
    task_id: str = Field(default="")


class ValidationResult(BaseDomainResult):
    """Result of schema or constraint validation."""
    is_schema_valid: bool = Field(default=True)


class ToolSelectionResult(BaseDomainResult):
    """Result of tool selection and invocation."""
    selected_tool_name: str = Field(default="")
    tool_output: Optional[Any] = Field(default=None)


class WorkflowResult(BaseDomainResult):
    """Result of workflow orchestration."""
    workflow_id: str = Field(default="")


class GoalResult(BaseDomainResult):
    """Result of overall goal evaluation."""
    goal_id: str = Field(default="")


class AgentResult(BaseDomainResult):
    """Aggregate result of complete agent run."""
    agent_name: str = Field(default="DocumentAgent")
    goal_result: Optional[GoalResult] = Field(default=None)
    planning_result: Optional[PlanningResult] = Field(default=None)
    execution_result: Optional[ExecutionResult] = Field(default=None)
    observation_result: Optional[ObservationResult] = Field(default=None)
    reflection_result: Optional[ReflectionResult] = Field(default=None)
