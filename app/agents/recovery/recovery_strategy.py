"""
Recovery Strategy Models.
Defines the 14 canonical recovery strategies and policy definitions.
"""

from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, Field


class RecoveryStrategy(str, Enum):
    """Canonical recovery strategies for self-healing and failure remediation."""
    RETRY = "Retry"
    RETRY_SUBTREE = "RetrySubtree"
    RETRY_WORKFLOW = "RetryWorkflow"
    ALTERNATE_WORKER = "AlternateWorker"
    ALTERNATE_TOOL = "AlternateTool"
    RESTORE_CHECKPOINT = "RestoreCheckpoint"
    REPLAY_EXECUTION = "ReplayExecution"
    REPLAY_SUBTREE = "ReplaySubtree"
    REPLAY_WORKFLOW = "ReplayWorkflow"
    COMPENSATION = "Compensation"
    ROLLBACK = "Rollback"
    PLANNER_RE_ENTRY = "PlannerReEntry"
    HUMAN_APPROVAL = "HumanApproval"
    PERMANENT_FAILURE = "PermanentFailure"


class RecoveryStrategyDefinition(BaseModel):
    """Detailed definition and parameters of an assigned recovery strategy."""
    strategy: RecoveryStrategy
    parameters: Dict[str, Any] = Field(default_factory=dict)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    requires_human_gate: bool = Field(default=False)
    model_config = {"frozen": True}
