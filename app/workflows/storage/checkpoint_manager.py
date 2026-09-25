"""
Enterprise Workflow Checkpoint System.
Captures immutable checkpoints after task transitions, approvals, and decisions for deterministic crash recovery.
"""

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from ..domain.models import Checkpoint, ExecutionState


class CheckpointManager:
    """Manages creation, indexing, and recovery from execution checkpoints."""

    def __init__(self):
        # Key: checkpoint_id
        self._checkpoints: Dict[str, Checkpoint] = {}
        # Key: execution_id -> List of checkpoint_ids in chronological order
        self._execution_checkpoints: Dict[str, List[str]] = {}

    def create_checkpoint(
        self,
        execution_id: str,
        execution_state: ExecutionState,
        variables: Dict[str, Any],
        completed_tasks: List[str],
        pending_tasks: List[str],
    ) -> Checkpoint:
        """Create and store a durable snapshot checkpoint."""
        chk = Checkpoint(
            checkpoint_id=str(uuid.uuid4()),
            execution_id=execution_id,
            execution_state=execution_state,
            variables=deepcopy(variables),
            completed_tasks=list(completed_tasks),
            pending_tasks=list(pending_tasks),
            timestamp=datetime.now(timezone.utc),
        )
        self._checkpoints[chk.checkpoint_id] = chk
        if execution_id not in self._execution_checkpoints:
            self._execution_checkpoints[execution_id] = []
        self._execution_checkpoints[execution_id].append(chk.checkpoint_id)
        return chk

    def get_latest_checkpoint(self, execution_id: str) -> Optional[Checkpoint]:
        """Retrieve the latest checkpoint for an execution."""
        chk_ids = self._execution_checkpoints.get(execution_id, [])
        if not chk_ids:
            return None
        latest_id = chk_ids[-1]
        return self._checkpoints.get(latest_id)

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        return self._checkpoints.get(checkpoint_id)

    def list_checkpoints(self, execution_id: str) -> List[Checkpoint]:
        """List all historical checkpoints for an execution."""
        chk_ids = self._execution_checkpoints.get(execution_id, [])
        return [self._checkpoints[cid] for cid in chk_ids if cid in self._checkpoints]
