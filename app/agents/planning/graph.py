"""
Plan Graph Domain Representation.
Represents DAG topology, nodes, edges, entry points, and exit points.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.planning.edges import PlanEdge
from app.agents.planning.nodes import PlanNode


class PlanGraph(BaseModel):
    """Directed Acyclic Graph container for planning task execution."""
    graph_id: str
    nodes: Dict[str, PlanNode] = Field(default_factory=dict)
    edges: List[PlanEdge] = Field(default_factory=list)
    entry_node_ids: List[str] = Field(default_factory=list)
    exit_node_ids: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}

    def get_node(self, node_id: str) -> Optional[PlanNode]:
        """Retrieves node by node_id."""
        return self.nodes.get(node_id)

    def get_outgoing_edges(self, node_id: str) -> List[PlanEdge]:
        """Returns all outgoing edges originating from given node_id."""
        return [edge for edge in self.edges if edge.source_node_id == node_id]

    def get_incoming_edges(self, node_id: str) -> List[PlanEdge]:
        """Returns all incoming edges targeting given node_id."""
        return [edge for edge in self.edges if edge.target_node_id == node_id]
