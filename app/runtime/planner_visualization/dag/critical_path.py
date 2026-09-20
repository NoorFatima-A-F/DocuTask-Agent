"""
Critical Path Engine (CPM) for Phase 13.2.
Calculates longest execution path, bottleneck nodes, and slack times across the DAG.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set
from app.runtime.planner_visualization.ui_models.models import PlannerDAGNode, PlannerDAGEdge


class CriticalPathEngine:
    """
    Implements Critical Path Method (CPM) for calculating total estimated mission duration
    and identifying bottleneck nodes.
    """

    @classmethod
    def compute_critical_path(cls, nodes: List[PlannerDAGNode], edges: List[PlannerDAGEdge]) -> Dict[str, Any]:
        if not nodes:
            return {"critical_path_nodes": [], "total_duration_ms": 0.0, "bottlenecks": []}

        node_map = {n.node_id: n for n in nodes}
        adj: Dict[str, List[str]] = {n.node_id: [] for n in nodes}
        in_degrees: Dict[str, int] = {n.node_id: 0 for n in nodes}

        for edge in edges:
            if edge.source in adj and edge.target in in_degrees:
                adj[edge.source].append(edge.target)
                in_degrees[edge.target] += 1

        # Topological sorting
        queue = [nid for nid, deg in in_degrees.items() if deg == 0]
        topo_order = []
        while queue:
            curr = queue.pop(0)
            topo_order.append(curr)
            for neighbor in adj[curr]:
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    queue.append(neighbor)

        # Forward pass: Earliest Start (ES) & Earliest Finish (EF)
        es: Dict[str, float] = {nid: 0.0 for nid in topo_order}
        ef: Dict[str, float] = {nid: 0.0 for nid in topo_order}
        parent_on_path: Dict[str, str] = {}

        for nid in topo_order:
            dur = node_map[nid].estimated_duration_ms
            ef[nid] = es[nid] + dur
            for neighbor in adj[nid]:
                if ef[nid] > es[neighbor]:
                    es[neighbor] = ef[nid]
                    parent_on_path[neighbor] = nid

        # Find max finish node
        if not ef:
            return {"critical_path_nodes": [], "total_duration_ms": 0.0, "bottlenecks": []}

        max_node = max(ef.keys(), key=lambda k: ef[k])
        max_duration = ef[max_node]

        # Trace back critical path
        curr = max_node
        path = []
        while curr:
            path.append(curr)
            curr = parent_on_path.get(curr)

        critical_path = list(reversed(path))

        # Identify top bottleneck (node with highest duration on critical path)
        bottlenecks = sorted(
            [{"node_id": nid, "duration_ms": node_map[nid].estimated_duration_ms, "name": node_map[nid].name} for nid in critical_path],
            key=lambda x: x["duration_ms"],
            reverse=True,
        )

        return {
            "critical_path_nodes": critical_path,
            "total_duration_ms": max_duration,
            "bottlenecks": bottlenecks,
        }
