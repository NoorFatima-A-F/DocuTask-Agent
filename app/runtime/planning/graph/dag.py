"""
Production Execution Directed Acyclic Graph (DAG) Engine.

Provides topological sorting (Kahn's algorithm), cycle detection (3-color DFS),
transitive reduction, concurrency wavefronts, and CPM (Critical Path Method) metrics.
"""

from __future__ import annotations

import collections
import copy
from typing import Any, Dict, List, Optional, Set, Tuple
from app.runtime.planning.graph.edge import DAGEdge, EdgeType
from app.runtime.planning.graph.node import DAGNode, DependencySpec, DependencyType, NodeStatus


class ExecutionDAG:
    """Core Directed Acyclic Graph representing an autonomous execution mission."""

    def __init__(self, dag_id: str, mission_id: str) -> None:
        self.dag_id = dag_id
        self.mission_id = mission_id
        self.nodes: Dict[str, DAGNode] = {}
        self.edges: Dict[str, DAGEdge] = {}
        self._adjacency_out: Dict[str, List[str]] = collections.defaultdict(list)
        self._adjacency_in: Dict[str, List[str]] = collections.defaultdict(list)
        self.generation: int = 1
        self.metadata: Dict[str, Any] = {}

    def add_node(self, node: DAGNode) -> None:
        """Adds a node to the DAG."""
        self.nodes[node.node_id] = node
        if node.node_id not in self._adjacency_out:
            self._adjacency_out[node.node_id] = []
        if node.node_id not in self._adjacency_in:
            self._adjacency_in[node.node_id] = []

    def remove_node(self, node_id: str) -> Optional[DAGNode]:
        """Removes a node and all connected incident edges."""
        if node_id not in self.nodes:
            return None
        node = self.nodes.pop(node_id)
        
        # Remove attached edges
        edges_to_remove = [
            e_id for e_id, e in self.edges.items()
            if e.source_node_id == node_id or e.target_node_id == node_id
        ]
        for e_id in edges_to_remove:
            self.remove_edge(e_id)

        self._adjacency_out.pop(node_id, None)
        self._adjacency_in.pop(node_id, None)
        return node

    def add_edge(self, edge: DAGEdge) -> None:
        """Adds an edge between existing nodes, ensuring no cycles."""
        if edge.source_node_id not in self.nodes or edge.target_node_id not in self.nodes:
            raise ValueError(f"Source {edge.source_node_id} or target {edge.target_node_id} does not exist in DAG.")
        
        self.edges[edge.edge_id] = edge
        self._adjacency_out[edge.source_node_id].append(edge.target_node_id)
        self._adjacency_in[edge.target_node_id].append(edge.source_node_id)

        # Synchronize node dependency spec
        target_node = self.nodes[edge.target_node_id]
        if not any(d.parent_node_id == edge.source_node_id for d in target_node.dependencies):
            target_node.dependencies.append(
                DependencySpec(
                    parent_node_id=edge.source_node_id,
                    dependency_type=DependencyType.HARD if edge.edge_type != EdgeType.CONDITIONAL_BRANCH else DependencyType.CONDITIONAL,
                    condition_expr=edge.condition_expression,
                )
            )

        if self.has_cycle():
            self.remove_edge(edge.edge_id)
            raise ValueError(f"Adding edge {edge.source_node_id} -> {edge.target_node_id} creates a directed cycle.")

    def remove_edge(self, edge_id: str) -> Optional[DAGEdge]:
        """Removes an edge and updates adjacency maps."""
        if edge_id not in self.edges:
            return None
        edge = self.edges.pop(edge_id)
        if edge.target_node_id in self._adjacency_out.get(edge.source_node_id, []):
            self._adjacency_out[edge.source_node_id].remove(edge.target_node_id)
        if edge.source_node_id in self._adjacency_in.get(edge.target_node_id, []):
            self._adjacency_in[edge.target_node_id].remove(edge.source_node_id)

        # Remove from target node dependencies
        if edge.target_node_id in self.nodes:
            self.nodes[edge.target_node_id].dependencies = [
                d for d in self.nodes[edge.target_node_id].dependencies
                if d.parent_node_id != edge.source_node_id
            ]
        return edge

    def has_cycle(self) -> bool:
        """Cycle detection using 3-color DFS (WHITE=0, GREY=1, BLACK=2)."""
        visited: Dict[str, int] = {nid: 0 for nid in self.nodes}

        def dfs(u: str) -> bool:
            visited[u] = 1  # Grey (in progress)
            for v in self._adjacency_out.get(u, []):
                if visited.get(v, 0) == 1:
                    return True  # Back-edge found -> cycle
                if visited.get(v, 0) == 0:
                    if dfs(v):
                        return True
            visited[u] = 2  # Black (finished)
            return False

        for node_id in self.nodes:
            if visited[node_id] == 0:
                if dfs(node_id):
                    return True
        return False

    def topological_sort(self) -> List[DAGNode]:
        """Returns nodes in topologically sorted order using Kahn's algorithm."""
        in_degree = {nid: len(self._adjacency_in.get(nid, [])) for nid in self.nodes}
        queue = collections.deque([nid for nid, deg in in_degree.items() if deg == 0])
        sorted_nodes: List[DAGNode] = []

        while queue:
            u = queue.popleft()
            sorted_nodes.append(self.nodes[u])
            for v in self._adjacency_out.get(u, []):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(sorted_nodes) != len(self.nodes):
            raise ValueError("Topological sort failed: DAG contains cycles.")
        return sorted_nodes

    def compute_concurrency_wavefronts(self) -> List[List[DAGNode]]:
        """Groups topologically sorted nodes into parallel execution wavefronts."""
        in_degree = {nid: len(self._adjacency_in.get(nid, [])) for nid in self.nodes}
        current_wave = [nid for nid, deg in in_degree.items() if deg == 0]
        wavefronts: List[List[DAGNode]] = []

        while current_wave:
            wavefronts.append([self.nodes[nid] for nid in current_wave])
            next_wave = []
            for u in current_wave:
                for v in self._adjacency_out.get(u, []):
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        next_wave.append(v)
            current_wave = next_wave

        return wavefronts

    def compute_critical_path(self) -> Tuple[List[str], float]:
        """
        Calculates CPM metrics: Earliest/Latest Start/Finish times and Slack.
        Returns: (critical_node_ids, total_critical_path_duration_ms)
        """
        if not self.nodes:
            return [], 0.0

        topo = self.topological_sort()
        
        # Forward pass: Earliest Start (ES) and Earliest Finish (EF)
        for node in topo:
            parents = self._adjacency_in.get(node.node_id, [])
            if not parents:
                node.earliest_start_ms = 0.0
            else:
                node.earliest_start_ms = max(self.nodes[p].earliest_finish_ms for p in parents)
            node.earliest_finish_ms = node.earliest_start_ms + max(node.estimated_runtime_ms, 1.0)

        # Total project duration
        total_duration = max(n.earliest_finish_ms for n in topo)

        # Backward pass: Latest Finish (LF) and Latest Start (LS)
        for node in reversed(topo):
            children = self._adjacency_out.get(node.node_id, [])
            if not children:
                node.latest_finish_ms = total_duration
            else:
                node.latest_finish_ms = min(self.nodes[c].latest_start_ms for c in children)
            node.latest_start_ms = node.latest_finish_ms - max(node.estimated_runtime_ms, 1.0)
            node.total_slack_ms = round(max(0.0, node.latest_start_ms - node.earliest_start_ms), 2)
            node.is_critical_path = (node.total_slack_ms == 0.0)

        critical_nodes = [n.node_id for n in topo if n.is_critical_path]
        return critical_nodes, round(total_duration, 2)

    def get_ready_nodes(self, completed_node_ids: Set[str]) -> List[DAGNode]:
        """Returns all nodes whose dependencies have succeeded and are waiting to run."""
        ready = []
        for node in self.nodes.values():
            if node.status in (NodeStatus.WAITING, NodeStatus.READY):
                if node.is_ready(completed_node_ids):
                    node.status = NodeStatus.READY
                    ready.append(node)
        return ready

    def clone(self) -> ExecutionDAG:
        """Deep copy clone of the DAG."""
        return copy.deepcopy(self)

    def get_summary(self) -> Dict[str, Any]:
        """Returns high-level graph metrics."""
        crit_nodes, crit_dur = self.compute_critical_path()
        wavefronts = self.compute_concurrency_wavefronts()
        max_parallel_width = max((len(w) for w in wavefronts), default=1)

        total_cost = sum(n.estimated_cost_usd for n in self.nodes.values())
        total_tokens = sum(n.estimated_tokens for n in self.nodes.values())

        return {
            "dag_id": self.dag_id,
            "mission_id": self.mission_id,
            "generation": self.generation,
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "critical_path_ms": crit_dur,
            "critical_nodes_count": len(crit_nodes),
            "structural_depth": len(wavefronts),
            "max_parallel_width": max_parallel_width,
            "total_estimated_cost_usd": round(total_cost, 5),
            "total_estimated_tokens": total_tokens,
        }
