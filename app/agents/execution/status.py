"""
Execution Status Domain Models.
"""

from typing import Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.execution.lifecycle import ExecutionLifecycleState


class NodeExecutionStatus(BaseModel):
    """Runtime execution status of a single graph node."""
    node_id: str
    state: ExecutionLifecycleState = Field(default=ExecutionLifecycleState.CREATED)
    assigned_worker_id: Optional[str] = Field(default=None)
    retry_count: int = Field(default=0, ge=0)
    error_message: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class ExecutionStatus(BaseModel):
    """Global execution session status snapshot."""
    execution_id: UUID
    state: ExecutionLifecycleState = Field(default=ExecutionLifecycleState.CREATED)
    node_statuses: Dict[str, NodeExecutionStatus] = Field(default_factory=dict)
    is_terminal: bool = Field(default=False)
    model_config = {"frozen": True}
