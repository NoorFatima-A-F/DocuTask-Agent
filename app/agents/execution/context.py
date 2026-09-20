"""
Execution Runtime Context Models.
Defines RuntimeContext, ExecutionRequest, and ExecutionResult.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.execution.lifecycle import ExecutionLifecycleState
from app.agents.execution.metadata import ExecutionIdentity, ExecutionMetadata, ExecutionStatistics
from app.agents.planning.contracts import Plan


class RuntimeContext(BaseModel):
    """Execution runtime parameters, environment limits, and tenant boundaries."""
    tenant_id: str = Field(default="default")
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    max_concurrency: int = Field(default=4, ge=1)
    timeout_seconds: float = Field(default=3600.0, gt=0.0)
    token_budget_limit: int = Field(default=50000, ge=0)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class ExecutionRequest(BaseModel):
    """Request payload to initiate execution of a validated Plan."""
    plan: Plan
    context: RuntimeContext = Field(default_factory=RuntimeContext)
    initial_inputs: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class ExecutionResult(BaseModel):
    """Structured execution outcome payload."""
    execution_id: UUID
    plan_id: UUID
    lifecycle_state: ExecutionLifecycleState = Field(default=ExecutionLifecycleState.COMPLETED)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    statistics: ExecutionStatistics = Field(default_factory=ExecutionStatistics)
    errors: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}
