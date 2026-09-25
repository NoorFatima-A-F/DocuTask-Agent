"""
Replay Engine.
Coordinates deterministic node replay, subtree replay, and execution replay.
"""

from typing import Any, Dict, List
from uuid import UUID
from pydantic import BaseModel, Field


class ReplayInstruction(BaseModel):
    """Instruction to re-execute a node or subtree from a known verified input state."""
    replay_id: str
    execution_id: UUID
    node_ids: List[str]
    inputs: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class ReplayEngine:
    """Coordinates replay instructions for deterministic task re-execution."""

    def build_node_replay(self, execution_id: UUID, node_id: str, inputs: Dict[str, Any]) -> ReplayInstruction:
        return ReplayInstruction(
            replay_id=f"replay_node_{node_id}",
            execution_id=execution_id,
            node_ids=[node_id],
            inputs=inputs
        )

    def build_subtree_replay(self, execution_id: UUID, subtree_node_ids: List[str], inputs: Dict[str, Any]) -> ReplayInstruction:
        return ReplayInstruction(
            replay_id=f"replay_subtree_{execution_id}",
            execution_id=execution_id,
            node_ids=subtree_node_ids,
            inputs=inputs
        )
