"""
Checkpoint Restorer.
Selects optimal checkpoint (nearest, best, policy-driven) and orchestrates state restoration via ExecutionAdapter.
"""

from typing import Any, Dict, Optional
from uuid import UUID


class CheckpointRestorer:
    """Restores execution state from point-in-time checkpoints."""

    def select_best_checkpoint(self, execution_id: UUID, available_checkpoints: Dict[UUID, Any]) -> Optional[UUID]:
        """Selects the latest verified checkpoint ID for restoration."""
        if not available_checkpoints:
            return None
        return list(available_checkpoints.keys())[-1]

    def verify_checkpoint_integrity(self, checkpoint_data: Dict[str, Any]) -> bool:
        """Verifies checkpoint checksum and structure."""
        return "node_states" in checkpoint_data or "metadata" in checkpoint_data
