"""
Execution Checkpoint Manager.
Creates deterministic point-in-time runtime snapshots before tool execution,
after task completion, after branch completion, and periodically.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.execution.lifecycle import ExecutionLifecycleState


class CheckpointMetadata(BaseModel):
    """Metadata describing a captured checkpoint."""
    checkpoint_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    trigger: str = Field(default="POST_TASK")  # PRE_TOOL, POST_TASK, POST_BRANCH, PERIODIC
    captured_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    checksum: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    model_config = {"frozen": True}


class ExecutionSnapshot(BaseModel):
    """Immutable point-in-time snapshot of the execution graph and runtime state."""
    metadata: CheckpointMetadata
    node_states: Dict[str, ExecutionLifecycleState]
    accumulated_outputs: Dict[str, Any]
    completed_node_ids: List[str]
    model_config = {"frozen": True}


class CheckpointManager:
    """Manages creation, storage, and restoration of execution checkpoints."""

    def __init__(self):
        self._checkpoints: Dict[UUID, ExecutionSnapshot] = {}
        self._execution_index: Dict[UUID, List[UUID]] = {}

    def create_checkpoint(
        self,
        execution_id: UUID,
        trigger: str,
        node_states: Dict[str, ExecutionLifecycleState],
        outputs: Dict[str, Any],
        completed_nodes: List[str]
    ) -> ExecutionSnapshot:
        meta = CheckpointMetadata(execution_id=execution_id, trigger=trigger)
        snapshot = ExecutionSnapshot(
            metadata=meta,
            node_states=dict(node_states),
            accumulated_outputs=dict(outputs),
            completed_node_ids=list(completed_nodes)
        )
        self._checkpoints[meta.checkpoint_id] = snapshot
        if execution_id not in self._execution_index:
            self._execution_index[execution_id] = []
        self._execution_index[execution_id].append(meta.checkpoint_id)
        return snapshot

    def get_latest_checkpoint(self, execution_id: UUID) -> ExecutionSnapshot | None:
        ids = self._execution_index.get(execution_id, [])
        if not ids:
            return None
        return self._checkpoints.get(ids[-1])

    def get_checkpoint(self, checkpoint_id: UUID) -> ExecutionSnapshot | None:
        return self._checkpoints.get(checkpoint_id)
