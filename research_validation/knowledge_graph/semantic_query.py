"""
Semantic Query Engine (Phase 83C)
================================
Executes multi-hop graph traversals, semantic filtering, and path-finding
across the Scientific Knowledge Graph.
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

from research_validation.knowledge_graph.knowledge_node import KnowledgeNode
from research_validation.knowledge_graph.ontology import EntityType, RelationshipType
from research_validation.knowledge_graph.relationship_engine import (
    RelationshipEdge, RelationshipEngine
)


@dataclass(frozen=True)
class GraphPath:
    """A traversed path through knowledge nodes and edges."""
    nodes: List[KnowledgeNode]
    edges: List[RelationshipEdge]
    total_weight: float
    path_confidence: float


class SemanticQueryEngine:
    """
    Query executor for graph traversal and pattern matching.
    """

    def __init__(
        self,
        nodes: Dict[str, KnowledgeNode],
        rel_engine: RelationshipEngine,
    ):
        self.nodes = nodes
        self.rel_engine = rel_engine

    def find_nodes_by_type(self, entity_type: EntityType) -> List[KnowledgeNode]:
        return [n for n in self.nodes.values() if n.entity_type == entity_type]

    def find_nodes_by_property(self, key: str, value: Any) -> List[KnowledgeNode]:
        return [n for n in self.nodes.values() if n.properties.get(key) == value]

    def get_neighbors(
        self,
        node_id: str,
        relationship: Optional[RelationshipType] = None,
        direction: str = "OUT",  # "OUT", "IN", "BOTH"
    ) -> List[KnowledgeNode]:
        """Fetch neighbor nodes along specific relationship edges."""
        neighbors: List[KnowledgeNode] = []
        edges: List[RelationshipEdge] = []

        if direction in ("OUT", "BOTH"):
            edges.extend(self.rel_engine.get_outgoing_edges(node_id))
        if direction in ("IN", "BOTH"):
            edges.extend(self.rel_engine.get_incoming_edges(node_id))

        for e in edges:
            if relationship is None or e.relationship == relationship:
                nbr_id = e.target_id if e.source_id == node_id else e.source_id
                if nbr_id in self.nodes:
                    neighbors.append(self.nodes[nbr_id])

        return neighbors

    def find_shortest_path(
        self,
        start_id: str,
        target_id: str,
        max_depth: int = 6,
    ) -> Optional[GraphPath]:
        """BFS shortest-path finder between two scientific entities."""
        if start_id not in self.nodes or target_id not in self.nodes:
            return None
        if start_id == target_id:
            return GraphPath(nodes=[self.nodes[start_id]], edges=[], total_weight=0.0, path_confidence=1.0)

        queue: deque[Tuple[str, List[str], List[str]]] = deque([(start_id, [start_id], [])])
        visited: Set[str] = {start_id}

        while queue:
            curr_id, path_nodes, path_edges = queue.popleft()
            if len(path_nodes) > max_depth:
                continue

            for edge in self.rel_engine.get_outgoing_edges(curr_id):
                nbr_id = edge.target_id
                if nbr_id == target_id:
                    final_node_ids = path_nodes + [nbr_id]
                    final_edge_ids = path_edges + [edge.edge_id]
                    nodes_list = [self.nodes[nid] for nid in final_node_ids]
                    edges_list = [self.rel_engine.edges[eid] for eid in final_edge_ids]
                    tot_w = sum(e.weight for e in edges_list)
                    conf = 1.0
                    for e in edges_list:
                        conf *= e.confidence
                    return GraphPath(nodes=nodes_list, edges=edges_list, total_weight=tot_w, path_confidence=conf)

                if nbr_id not in visited and nbr_id in self.nodes:
                    visited.add(nbr_id)
                    queue.append((nbr_id, path_nodes + [nbr_id], path_edges + [edge.edge_id]))

        return None
