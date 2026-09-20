"""
Workflow Graph DAG Model.
Represents directed acyclic graphs of workflow nodes and edges with topological sorting and cycle detection.
"""

from typing import Dict, List, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.workflow.exceptions import CyclicWorkflowGraphError
from app.agents.workflow.workflow_edge import WorkflowEdge
from app.agents.workflow.workflow_node import WorkflowNode


class WorkflowGraph(BaseModel):
    """Directed graph representing dependencies between workflow nodes."""
    graph_id: UUID = Field(default_factory=uuid4)
    nodes: Dict[str, WorkflowNode] = Field(default_factory=dict)
    edges: List[WorkflowEdge] = Field(default_factory=list)

    def add_node(self, node: WorkflowNode) -> None:
        """Adds a workflow node."""
        self.nodes[node.node_id] = node

    def add_edge(self, edge: WorkflowEdge) -> None:
        """Adds an edge and validates acyclicity."""
        self.edges.append(edge)
        self.validate_acyclic()

    def get_topological_order(self) -> List[str]:
        """Calculates topological execution ordering."""
        in_degree: Dict[str, int] = {nid: 0 for nid in self.nodes}
        adj: Dict[str, List[str]] = {nid: [] for nid in self.nodes}

        for edge in self.edges:
            adj[edge.source_node_id].append(edge.target_node_id)
            in_degree[edge.target_node_id] += 1

        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        order: List[str] = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        if len(order) != len(self.nodes):
            raise CyclicWorkflowGraphError("Cycle detected in workflow graph.")

        return order

    def validate_acyclic(self) -> None:
        """Validates that the graph is free of cycles."""
        self.get_topological_order()
