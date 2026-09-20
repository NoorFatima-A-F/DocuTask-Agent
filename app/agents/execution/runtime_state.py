"""
Runtime State Representation.
Snapshot of global in-flight execution state across all workers and graph nodes.
"""

from typing import Any, Dict, List
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.execution.lifecycle import ExecutionLifecycleState
from app.agents.execution.metadata import ExecutionStatistics


class RuntimeState(BaseModel):
    """Point-in-time runtime state of an active execution session."""
    execution_id: UUID
    state: ExecutionLifecycleState = Field(default=ExecutionLifecycleState.CREATED)
    active_node_ids: List[str] = Field(default_factory=list)
    completed_node_ids: List[str] = Field(default_factory=list)
    failed_node_ids: List[str] = Field(default_factory=list)
    accumulated_outputs: Dict[str, Any] = Field(default_factory=dict)
    statistics: ExecutionStatistics = Field(default_factory=ExecutionStatistics)
    model_config = {"frozen": True}
