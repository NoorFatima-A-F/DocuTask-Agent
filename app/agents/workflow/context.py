"""
Workflow Context, Request, and Result Models.
Defines execution context, invocation requests, and structured workflow results.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.metadata import WorkflowIdentity, WorkflowStatistics


class WorkflowContext(BaseModel):
    """Operational limits and execution parameters for a workflow instance."""
    tenant_id: str = Field(default="default")
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    max_duration_seconds: float = Field(default=86400.0, gt=0.0)  # 24 hours default
    enable_saga_compensation: bool = True
    auto_checkpoint: bool = True
    parameters: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class WorkflowRequest(BaseModel):
    """Request payload to instantiate and execute a workflow."""
    definition_id: UUID
    input_data: Dict[str, Any] = Field(default_factory=dict)
    context: WorkflowContext = Field(default_factory=WorkflowContext)
    parent_instance_id: Optional[UUID] = None

    model_config = {"frozen": True}


class WorkflowResult(BaseModel):
    """Execution outcome produced upon workflow termination."""
    identity: WorkflowIdentity
    lifecycle_state: WorkflowLifecycleState = Field(default=WorkflowLifecycleState.COMPLETED)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    statistics: WorkflowStatistics = Field(default_factory=WorkflowStatistics)
    errors: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}
