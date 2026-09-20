"""
Workflow Node Model.
Represents discrete steps in a workflow: tasks, sub-workflows, human approvals, event gateways, and timers.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class WorkflowNodeType(str, Enum):
    """Typology of workflow nodes."""
    TASK = "TASK"
    CHILD_WORKFLOW = "CHILD_WORKFLOW"
    HUMAN_APPROVAL = "HUMAN_APPROVAL"
    EVENT_GATEWAY = "EVENT_GATEWAY"
    TIMER = "TIMER"
    PARALLEL_SPLIT = "PARALLEL_SPLIT"
    PARALLEL_JOIN = "PARALLEL_JOIN"
    CONDITIONAL_BRANCH = "CONDITIONAL_BRANCH"
    SAGA_TRANSACTION = "SAGA_TRANSACTION"


class WorkflowNode(BaseModel):
    """An individual node / stage in a workflow DAG."""
    node_id: str
    name: str
    node_type: WorkflowNodeType = WorkflowNodeType.TASK
    handler: str  # Action handler or adapter method name
    parameters: Dict[str, Any] = Field(default_factory=dict)
    compensating_handler: Optional[str] = None  # Saga compensation
    timeout_seconds: float = Field(default=300.0, gt=0.0)
    retry_limit: int = Field(default=3, ge=0)

    model_config = {"frozen": True}
