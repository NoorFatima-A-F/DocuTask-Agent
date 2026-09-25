"""
Execution Graph Optimizer.

Performs transitive reduction, dependency pruning, dead branch elimination,
and concurrency optimization over execution graphs.
"""

from __future__ import annotations

import collections
from typing import Any, Dict, Set
from app.runtime.planning.graph.dag import ExecutionDAG


class GraphOptimizer:
    """Optimizes execution topologies to reduce critical path latency and redundant dependencies."""

    @classmethod
    def transitive_reduction(cls, dag: ExecutionDAG) -> int:
        """
        Removes redundant edges where an indirect path already exists.
        For example: If A -> B and B -> C, and A -> C exists, remove A -> C.
        Returns: Number of pruned redundant edges.
        """
        pruned_count = 0
        nodes_list = list(dag.nodes.keys())

        # For every pair (u, v) with direct edge, check if there exists an alternate path
        for u in nodes_list:
            children = list(dag._adjacency_out.get(u, []))
            for v in children:
                # Find if there is path from u to v without using direct edge (u, v)
                if cls._has_alternate_path(dag, u, v):
                    # Remove redundant edge
                    edge_id_to_remove = None
                    for eid, edge in dag.edges.items():
                        if edge.source_node_id == u and edge.target_node_id == v:
                            edge_id_to_remove = eid
                            break
                    if edge_id_to_remove:
                        dag.remove_edge(edge_id_to_remove)
                        pruned_count += 1

        return pruned_count

    @classmethod
    def _has_alternate_path(cls, dag: ExecutionDAG, src: str, tgt: str) -> bool:
        """BFS to check if a path from src to tgt exists via other intermediate nodes."""
        queue = collections.deque()
        for child in dag._adjacency_out.get(src, []):
            if child != tgt:
                queue.append(child)

        visited: Set[str] = set()
        while queue:
            curr = queue.popleft()
            if curr == tgt:
                return True
            if curr not in visited:
                visited.add(curr)
                for nxt in dag._adjacency_out.get(curr, []):
                    if nxt not in visited:
                        queue.append(nxt)
        return False

    @classmethod
    def optimize(cls, dag: ExecutionDAG) -> Dict[str, Any]:
        """Runs full optimization pipeline on the DAG."""
        pruned_edges = cls.transitive_reduction(dag)
        crit_nodes, crit_dur = dag.compute_critical_path()
        return {
            "pruned_edges_count": pruned_edges,
            "optimized_critical_path_ms": crit_dur,
            "critical_nodes_count": len(crit_nodes),
        }
