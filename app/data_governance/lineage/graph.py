"""Enterprise Data Lineage Graph Engine (Phase 8B).

Provides directed acyclic graph (DAG) storage and traversal for end-to-end data provenance.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set
from app.data_governance.lineage.nodes import LineageNode, LineageNodeType
from app.data_governance.lineage.edges import LineageEdge, LineageEdgeType


class LineageGraphEngine:
    """Manages lineage topology, upstream/downstream impact analysis, and root cause tracing."""

    def __init__(self):
        # node_id -> LineageNode
        self._nodes: Dict[str, LineageNode] = {}
        # edge_id -> LineageEdge
        self._edges: Dict[str, LineageEdge] = {}
        # source_node_id -> List[LineageEdge] (outgoing / downstream)
        self._outgoing: Dict[str, List[LineageEdge]] = {}
        # target_node_id -> List[LineageEdge] (incoming / upstream)
        self._incoming: Dict[str, List[LineageEdge]] = {}

    def add_node(self, node: LineageNode) -> LineageNode:
        """Add a node to the lineage graph."""
        self._nodes[node.node_id] = node
        if node.node_id not in self._outgoing:
            self._outgoing[node.node_id] = []
        if node.node_id not in self._incoming:
            self._incoming[node.node_id] = []
        return node

    def add_edge(self, edge: LineageEdge) -> LineageEdge:
        """Add a directed edge connecting source -> target."""
        self._edges[edge.edge_id] = edge
        if edge.source_node_id not in self._outgoing:
            self._outgoing[edge.source_node_id] = []
        self._outgoing[edge.source_node_id].append(edge)

        if edge.target_node_id not in self._incoming:
            self._incoming[edge.target_node_id] = []
        self._incoming[edge.target_node_id].append(edge)
        return edge

    def get_node(self, node_id: str) -> Optional[LineageNode]:
        """Retrieve node by ID."""
        return self._nodes.get(node_id)

    def get_upstream_lineage(self, node_id: str, max_depth: int = 10) -> List[LineageNode]:
        """Traverse upstream dependencies (parents / data origins)."""
        visited: Set[str] = set()
        queue = [(node_id, 0)]
        upstream_nodes: List[LineageNode] = []

        while queue:
            curr_id, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self._incoming.get(curr_id, []):
                parent_id = edge.source_node_id
                if parent_id not in visited:
                    visited.add(parent_id)
                    parent_node = self._nodes.get(parent_id)
                    if parent_node:
                        upstream_nodes.append(parent_node)
                        queue.append((parent_id, depth + 1))

        return upstream_nodes

    def get_downstream_lineage(self, node_id: str, max_depth: int = 10) -> List[LineageNode]:
        """Traverse downstream dependents (impact analysis / consumers)."""
        visited: Set[str] = set()
        queue = [(node_id, 0)]
        downstream_nodes: List[LineageNode] = []

        while queue:
            curr_id, depth = queue.pop(0)
            if depth >= max_depth:
                continue

            for edge in self._outgoing.get(curr_id, []):
                child_id = edge.target_node_id
                if child_id not in visited:
                    visited.add(child_id)
                    child_node = self._nodes.get(child_id)
                    if child_node:
                        downstream_nodes.append(child_node)
                        queue.append((child_id, depth + 1))

        return downstream_nodes
