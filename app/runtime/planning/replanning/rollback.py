"""
Transactional DAG State Rollback Engine.

Manages checkpointing and atomic rollback of execution states and uncommitted node payloads.
"""

from __future__ import annotations

import copy
import time
from typing import Dict, List, Optional
from app.runtime.planning.graph.dag import ExecutionDAG


class DAGCheckpoint:
    def __init__(self, checkpoint_id: str, dag: ExecutionDAG) -> None:
        self.checkpoint_id = checkpoint_id
        self.dag_snapshot = dag.clone()
        self.timestamp = time.time()


class DAGRollbackEngine:
    """Provides atomic checkpointing and rollback capabilities."""

    def __init__(self) -> None:
        self._checkpoints: Dict[str, DAGCheckpoint] = {}

    def create_checkpoint(self, checkpoint_id: str, dag: ExecutionDAG) -> DAGCheckpoint:
        cp = DAGCheckpoint(checkpoint_id, dag)
        self._checkpoints[checkpoint_id] = cp
        return cp

    def rollback_to(self, checkpoint_id: str) -> Optional[ExecutionDAG]:
        if checkpoint_id not in self._checkpoints:
            return None
        return self._checkpoints[checkpoint_id].dag_snapshot.clone()
