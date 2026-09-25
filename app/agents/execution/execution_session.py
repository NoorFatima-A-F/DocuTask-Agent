"""
Execution Session Aggregate Root.
Represents an ongoing or completed stateful execution session.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.agents.execution.context import RuntimeContext
from app.agents.execution.lifecycle import ExecutionLifecycleState
from app.agents.execution.metadata import ExecutionIdentity, ExecutionMetadata, ExecutionStatistics
from app.agents.planning.contracts import Plan


class ExecutionSession(BaseModel):
    """
    Stateful Execution Session Aggregate Root.
    Tracks execution identity, lifecycle state, plan reference, metadata, and final outputs.
    """
    identity: ExecutionIdentity
    plan: Plan
    context: RuntimeContext = Field(default_factory=RuntimeContext)
    lifecycle_state: ExecutionLifecycleState = Field(default=ExecutionLifecycleState.CREATED)
    metadata: ExecutionMetadata = Field(default_factory=ExecutionMetadata)
    statistics: ExecutionStatistics = Field(default_factory=ExecutionStatistics)
    final_outputs: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = Field(default=None)

    model_config = {"frozen": True}
