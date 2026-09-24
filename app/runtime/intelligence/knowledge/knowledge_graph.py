"""
Knowledge Graph Evolution Model for Phase 10 (AISLCOP).

Provides evidence-linked semantic graph linking:
Mission -> Entities -> Relationships -> Strategies -> Policies -> Evidence -> Outcomes.
Every edge explicitly references cryptographic evidence hashes.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class GraphNode:
    node_id: str
    node_type: str  # MISSION, ENTITY, STRATEGY, POLICY, EVIDENCE, OUTCOME
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass
class GraphEdge:
    edge_id: str
    source_id: str
    target_id: str
    relationship: str  # EXTRACTED_FROM, APPLIES_STRATEGY, GOVERNED_BY, SUPPORTED_BY_EVIDENCE, PRODUCED_OUTCOME
    weight: float = 1.0
    evidence_hash: str = ""  # Cryptographic proof link
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


class AdaptiveKnowledgeGraph:
    """
    Evidence-linked knowledge graph that evolves with operational learning.
    """

    def __init__(self):
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: Dict[str, GraphEdge] = {}
        self._adjacency: Dict[str, List[str]] = {}  # source_id -> list of edge_ids
        self._reverse_adj: Dict[str, List[str]] = {}  # target_id -> list of edge_ids

    def add_node(self, node: GraphNode) -> str:
        self._nodes[node.node_id] = node
        if node.node_id not in self._adjacency:
            self._adjacency[node.node_id] = []
        if node.node_id not in self._reverse_adj:
            self._reverse_adj[node.node_id] = []
        return node.node_id

    def add_edge(self, edge: GraphEdge) -> str:
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            # Auto-create stub nodes if missing
            if edge.source_id not in self._nodes:
                self.add_node(GraphNode(node_id=edge.source_id, node_type="UNKNOWN", label=edge.source_id))
            if edge.target_id not in self._nodes:
                self.add_node(GraphNode(node_id=edge.target_id, node_type="UNKNOWN", label=edge.target_id))

        self._edges[edge.edge_id] = edge
        self._adjacency[edge.source_id].append(edge.edge_id)
        self._reverse_adj[edge.target_id].append(edge.edge_id)
        return edge.edge_id

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)

    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        return self._edges.get(edge_id)

    def get_neighbors(self, node_id: str) -> List[GraphNode]:
        edge_ids = self._adjacency.get(node_id, [])
        target_ids = [self._edges[eid].target_id for eid in edge_ids]
        return [self._nodes[tid] for tid in target_ids if tid in self._nodes]

    def get_subgraph(self, root_node_id: str, max_depth: int = 2) -> Dict[str, Any]:
        """Traverses BFS subgraph up to max_depth with nodes and edges."""
        visited_nodes: Set[str] = set()
        visited_edges: Set[str] = set()
        queue = [(root_node_id, 0)]

        while queue:
            curr, depth = queue.pop(0)
            if curr in visited_nodes or depth > max_depth:
                continue
            visited_nodes.add(curr)

            if curr in self._adjacency:
                for eid in self._adjacency[curr]:
                    edge = self._edges[eid]
                    visited_edges.add(eid)
                    if edge.target_id not in visited_nodes:
                        queue.append((edge.target_id, depth + 1))

        return {
            "root_node_id": root_node_id,
            "nodes": [asdict(self._nodes[nid]) for nid in visited_nodes if nid in self._nodes],
            "edges": [asdict(self._edges[eid]) for eid in visited_edges if eid in self._edges],
        }

    def serialize_full_graph(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self._nodes),
            "total_edges": len(self._edges),
            "nodes": [asdict(n) for n in self._nodes.values()],
            "edges": [asdict(e) for e in self._edges.values()],
        }
