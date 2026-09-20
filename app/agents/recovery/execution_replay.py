"""
Execution Replay Engine.
Coordinates re-execution requests through the ExecutionAdapter.
"""

from typing import Any, Dict, List
from uuid import UUID


class ExecutionReplayEngine:
    """Dispatches execution replay requests to the execution runtime."""

    def prepare_replay_payload(self, execution_id: UUID, target_node_ids: List[str]) -> Dict[str, Any]:
        return {
            "execution_id": str(execution_id),
            "target_nodes": target_node_ids,
            "mode": "REPLAY"
        }
