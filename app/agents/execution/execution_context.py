"""
Task Execution Context.
Supplied to workers during node execution containing inputs, parameters, and telemetry metadata.
"""

from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TaskExecutionContext(BaseModel):
    """Contextual parameters provided to a worker for executing a task node."""
    execution_id: UUID
    node_id: str
    task_id: Optional[str] = None
    capability_requirement: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    inputs: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: float = Field(default=300.0, gt=0.0)
    retry_attempt: int = Field(default=0, ge=0)
    model_config = {"frozen": True}
