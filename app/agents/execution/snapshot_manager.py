"""
Snapshot Manager.
Manages runtime and worker snapshots.
"""

from typing import Dict, List
from pydantic import BaseModel, Field
from app.agents.execution.checkpoint_manager import CheckpointManager, ExecutionSnapshot
from app.agents.execution.worker import Worker


class WorkerSnapshot(BaseModel):
    """Snapshot of active workers and allocations."""
    workers: List[Worker]
    model_config = {"frozen": True}


class SnapshotManager:
    """Coordinates snapshots between graph state and worker state."""

    def __init__(self, checkpoint_manager: CheckpointManager):
        self.checkpoint_manager = checkpoint_manager

    def capture_worker_snapshot(self, workers: List[Worker]) -> WorkerSnapshot:
        return WorkerSnapshot(workers=list(workers))
