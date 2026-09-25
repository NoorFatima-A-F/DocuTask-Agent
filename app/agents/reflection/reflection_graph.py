"""
Reflection Graph DAG Representation.
Represents the stages of reflection (analysis, evaluation, critique, knowledge extraction, recommendation, feedback)
as a directed acyclic graph.
"""

from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.exceptions import InvalidEvaluationGraphError


class ReflectionNode(BaseModel):
    """An individual stage or analyzer node within the reflection workflow."""
    node_id: str
    name: str
    stage_type: str  # analysis, evaluation, critique, extraction, recommendation, feedback
    handler_name: str
    dependencies: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class ReflectionEdge(BaseModel):
    """Directed dependency between two reflection nodes."""
    source_node_id: str
    target_node_id: str

    model_config = {"frozen": True}


class ReflectionGraph(BaseModel):
    """Directed Acyclic Graph representing dependency-aware execution of reflection stages."""
    graph_id: UUID = Field(default_factory=uuid4)
    nodes: Dict[str, ReflectionNode] = Field(default_factory=dict)
    edges: List[ReflectionEdge] = Field(default_factory=list)

    def add_node(self, node: ReflectionNode) -> None:
        """Adds a node to the reflection graph."""
        self.nodes[node.node_id] = node

    def add_edge(self, source_id: str, target_id: str) -> None:
        """Adds a directed dependency edge and validates acyclicity."""
        if source_id not in self.nodes or target_id not in self.nodes:
            raise InvalidEvaluationGraphError(f"Cannot link non-existent nodes: {source_id} -> {target_id}")
        self.edges.append(ReflectionEdge(source_node_id=source_id, target_node_id=target_id))
        self.validate_dag()

    def get_topological_order(self) -> List[str]:
        """Calculates topological ordering of reflection nodes."""
        in_degree: Dict[str, int] = {node_id: 0 for node_id in self.nodes}
        adj: Dict[str, List[str]] = {node_id: [] for node_id in self.nodes}

        for edge in self.edges:
            adj[edge.source_node_id].append(edge.target_node_id)
            in_degree[edge.target_node_id] += 1

        queue = [node_id for node_id, deg in in_degree.items() if deg == 0]
        ordered: List[str] = []

        while queue:
            curr = queue.pop(0)
            ordered.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(ordered) != len(self.nodes):
            raise InvalidEvaluationGraphError("Cycle detected in reflection graph")
        return ordered

    def validate_dag(self) -> bool:
        """Validates that the graph is a valid DAG."""
        self.get_topological_order()
        return True
