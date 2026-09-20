"""
Coordination Graph DAG Representation.
Represents the network of collaborating agents, supervision hierarchies, and delegation links as a DAG.
"""

from typing import Dict, List, Set
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.coordination.exceptions import CircularDelegationError


class CoordinationNode(BaseModel):
    """An agent node within the coordination topology."""
    node_id: str
    agent_id: UUID
    role: str
    assigned_tasks: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class CoordinationEdge(BaseModel):
    """Directed delegation or supervision link from one agent node to another."""
    source_node_id: str
    target_node_id: str
    relation: str = "DELEGATES_TO"  # SUPERVISES, DELEGATES_TO, COLLABORATES_WITH

    model_config = {"frozen": True}


class CoordinationGraph(BaseModel):
    """Directed graph representing multi-agent relationships and delegation flows."""
    graph_id: UUID = Field(default_factory=uuid4)
    nodes: Dict[str, CoordinationNode] = Field(default_factory=dict)
    edges: List[CoordinationEdge] = Field(default_factory=list)

    def add_node(self, node: CoordinationNode) -> None:
        """Adds an agent node to the graph."""
        self.nodes[node.node_id] = node

    def add_edge(self, source_id: str, target_id: str, relation: str = "DELEGATES_TO") -> None:
        """Adds a directed link and validates acyclicity."""
        self.edges.append(CoordinationEdge(
            source_node_id=source_id,
            target_node_id=target_id,
            relation=relation
        ))
        self.validate_acyclic()

    def validate_acyclic(self) -> None:
        """Ensures delegation links do not form a cycle."""
        in_degree: Dict[str, int] = {nid: 0 for nid in self.nodes}
        adj: Dict[str, List[str]] = {nid: [] for nid in self.nodes}

        for edge in self.edges:
            if edge.relation == "DELEGATES_TO":
                adj[edge.source_node_id].append(edge.target_node_id)
                in_degree[edge.target_node_id] += 1

        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        visited = 0

        while queue:
            curr = queue.pop(0)
            visited += 1
            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        if visited != len(self.nodes):
            raise CircularDelegationError("Cycle detected in agent delegation graph.")
