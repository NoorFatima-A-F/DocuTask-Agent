"""
Recovery Graph Domain Representation.
Represents DAG of recovery actions, compensation branches, and checkpoint restoration gates.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class RecoveryNode(BaseModel):
    """Action step in a recovery workflow (e.g., ReleaseLease, RestoreCheckpoint, ReplayTask)."""
    node_id: str
    action: str
    target_id: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    is_executed: bool = Field(default=False)
    model_config = {"frozen": True}


class RecoveryEdge(BaseModel):
    """Directed prerequisite relationship between recovery nodes."""
    source_id: str
    target_id: str
    model_config = {"frozen": True}


class RecoveryGraph(BaseModel):
    """Directed Acyclic Graph orchestrating autonomous recovery steps."""
    graph_id: UUID = Field(default_factory=uuid4)
    nodes: Dict[str, RecoveryNode] = Field(default_factory=dict)
    edges: List[RecoveryEdge] = Field(default_factory=list)
    model_config = {"frozen": True}

    def get_node(self, node_id: str) -> Optional[RecoveryNode]:
        return self.nodes.get(node_id)
