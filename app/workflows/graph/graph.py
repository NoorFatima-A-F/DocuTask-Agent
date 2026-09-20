"""
Enterprise Workflow Execution Graph (DAG Engine).
Provides dependency analysis, topological sorting, cycle detection, and branch traversal.
"""

from collections import defaultdict, deque
from typing import Dict, List, Optional, Set
from .nodes import GraphNode
from .edges import EdgeType, GraphEdge
from ..domain.exceptions import WorkflowValidationException


class ExecutionGraph:
    """Directed Acyclic Graph (DAG) representation of an executable workflow."""

    def __init__(self, workflow_id: str = "default_graph"):
        self.workflow_id = workflow_id
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: List[GraphEdge] = []
        self._incoming: Dict[str, List[GraphEdge]] = defaultdict(list)
        self._outgoing: Dict[str, List[GraphEdge]] = defaultdict(list)

    def add_node(self, node: GraphNode) -> None:
        """Add node to graph."""
        self._nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        """Add dependency edge between nodes."""
        self._edges.append(edge)
        self._outgoing[edge.source_node_id].append(edge)
        self._incoming[edge.target_node_id].append(edge)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self._nodes.get(node_id)

    def list_nodes(self) -> List[GraphNode]:
        return list(self._nodes.values())

    def list_edges(self) -> List[GraphEdge]:
        return list(self._edges)

    def get_incoming_edges(self, node_id: str) -> List[GraphEdge]:
        return list(self._incoming.get(node_id, []))

    def get_outgoing_edges(self, node_id: str) -> List[GraphEdge]:
        return list(self._outgoing.get(node_id, []))

    def get_dependencies(self, node_id: str) -> List[str]:
        """Get IDs of prerequisite nodes that must complete before this node."""
        return [e.source_node_id for e in self.get_incoming_edges(node_id) if e.edge_type == EdgeType.SUCCESS]

    def get_dependents(self, node_id: str) -> List[str]:
        """Get IDs of downstream nodes triggered after this node."""
        return [e.target_node_id for e in self.get_outgoing_edges(node_id) if e.edge_type == EdgeType.SUCCESS]

    def get_root_nodes(self) -> List[GraphNode]:
        """Nodes with no incoming success dependencies (entry points)."""
        roots = []
        for node_id, node in self._nodes.items():
            incoming_success = [e for e in self._incoming.get(node_id, []) if e.edge_type == EdgeType.SUCCESS]
            if not incoming_success:
                roots.append(node)
        return roots

    def get_leaf_nodes(self) -> List[GraphNode]:
        """Nodes with no outgoing success dependencies (terminal nodes)."""
        leaves = []
        for node_id, node in self._nodes.items():
            outgoing_success = [e for e in self._outgoing.get(node_id, []) if e.edge_type == EdgeType.SUCCESS]
            if not outgoing_success:
                leaves.append(node)
        return leaves

    def detect_cycles(self) -> List[List[str]]:
        """Tarjan / DFS cycle detection algorithm."""
        cycles: List[List[str]] = []
        visited: Dict[str, int] = {node_id: 0 for node_id in self._nodes}  # 0=unvisited, 1=visiting, 2=visited
        path: List[str] = []

        def dfs(curr: str):
            visited[curr] = 1
            path.append(curr)

            for edge in self._outgoing.get(curr, []):
                if edge.edge_type not in (EdgeType.SUCCESS, EdgeType.CONDITIONAL):
                    continue
                neighbor = edge.target_node_id
                if neighbor not in self._nodes:
                    continue
                if visited[neighbor] == 1:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])
                elif visited[neighbor] == 0:
                    dfs(neighbor)

            path.pop()
            visited[curr] = 2

        for node_id in self._nodes:
            if visited[node_id] == 0:
                dfs(node_id)

        return cycles

    def topological_sort(self) -> List[GraphNode]:
        """Topological sort using Kahn's algorithm."""
        cycles = self.detect_cycles()
        if cycles:
            raise WorkflowValidationException(f"Graph contains cycles: {cycles}")

        in_degree = {node_id: 0 for node_id in self._nodes}
        for node_id in self._nodes:
            in_degree[node_id] = len([e for e in self._incoming.get(node_id, []) if e.edge_type in (EdgeType.SUCCESS, EdgeType.CONDITIONAL)])

        queue = deque([node_id for node_id, deg in in_degree.items() if deg == 0])
        ordered: List[GraphNode] = []

        while queue:
            curr_id = queue.popleft()
            ordered.append(self._nodes[curr_id])

            for edge in self._outgoing.get(curr_id, []):
                if edge.edge_type not in (EdgeType.SUCCESS, EdgeType.CONDITIONAL):
                    continue
                neighbor_id = edge.target_node_id
                in_degree[neighbor_id] -= 1
                if in_degree[neighbor_id] == 0:
                    queue.append(neighbor_id)

        return ordered
