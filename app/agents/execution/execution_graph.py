"""
Execution Graph Runtime Wrapper.
Wraps PlanGraph and PlanNodes with dynamic execution state, outputs, and runtime timestamps.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.execution.lifecycle import ExecutionLifecycleState
from app.agents.planning.edges import PlanEdge
from app.agents.planning.graph import PlanGraph
from app.agents.planning.nodes import PlanNode


class ExecutionNode(BaseModel):
    """Runtime wrapper around a PlanNode maintaining execution lifecycle state and output artifacts."""
    node: PlanNode
    state: ExecutionLifecycleState = Field(default=ExecutionLifecycleState.CREATED)
    assigned_worker_id: Optional[str] = Field(default=None)
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    retry_count: int = Field(default=0, ge=0)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    error_message: Optional[str] = Field(default=None)


class ExecutionGraph:
    """Dynamic graph maintaining runtime execution states for all nodes and edges."""

    def __init__(self, plan_graph: PlanGraph):
        self.graph_id = plan_graph.graph_id
        self.plan_graph = plan_graph
        self.nodes: Dict[str, ExecutionNode] = {
            node_id: ExecutionNode(node=node)
            for node_id, node in plan_graph.nodes.items()
        }
        self.edges: List[PlanEdge] = list(plan_graph.edges)

    def get_node(self, node_id: str) -> Optional[ExecutionNode]:
        return self.nodes.get(node_id)

    def get_incoming_edges(self, node_id: str) -> List[PlanEdge]:
        return [e for e in self.edges if e.target_node_id == node_id]

    def get_outgoing_edges(self, node_id: str) -> List[PlanEdge]:
        return [e for e in self.edges if e.source_node_id == node_id]

    def update_node_state(
        self,
        node_id: str,
        state: ExecutionLifecycleState,
        outputs: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> None:
        node = self.nodes.get(node_id)
        if node:
            node.state = state
            if outputs:
                node.outputs.update(outputs)
            if error_message:
                node.error_message = error_message
            if state == ExecutionLifecycleState.RUNNING and not node.started_at:
                node.started_at = datetime.now(timezone.utc)
            elif state in (ExecutionLifecycleState.COMPLETED, ExecutionLifecycleState.FAILED):
                node.completed_at = datetime.now(timezone.utc)
