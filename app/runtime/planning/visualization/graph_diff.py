"""
Execution Graph Structural Diff Engine.

Calculates the delta between two DAG generations ($G_A \to G_B$):
identifies added nodes, removed nodes, rewired edges, and critical path shifts.
"""

from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel
from app.runtime.planning.graph.dag import ExecutionDAG


class GraphDiffResult(BaseModel):
    mission_id: str
    generation_from: int
    generation_to: int
    added_nodes: List[Dict[str, Any]]
    removed_node_ids: List[str]
    added_edges: List[Dict[str, Any]]
    removed_edge_ids: List[str]
    critical_path_delta_ms: float
    summary: str


class GraphDiffEngine:
    """Computes exact mathematical graph differences between DAG snapshots."""

    @classmethod
    def compute_diff(cls, dag_a: ExecutionDAG, dag_b: ExecutionDAG) -> GraphDiffResult:
        """Computes structural diff between dag_a and dag_b."""
        nodes_a = set(dag_a.nodes.keys())
        nodes_b = set(dag_b.nodes.keys())

        added_node_ids = nodes_b - nodes_a
        removed_node_ids = nodes_a - nodes_b

        edges_a = set(dag_a.edges.keys())
        edges_b = set(dag_b.edges.keys())

        added_edge_ids = edges_b - edges_a
        removed_edge_ids = edges_a - edges_b

        _, crit_dur_a = dag_a.compute_critical_path()
        _, crit_dur_b = dag_b.compute_critical_path()

        added_nodes_info = [
            {"node_id": nid, "name": dag_b.nodes[nid].name, "task_type": dag_b.nodes[nid].task_type}
            for nid in added_node_ids
        ]

        added_edges_info = [
            {"edge_id": eid, "source": dag_b.edges[eid].source_node_id, "target": dag_b.edges[eid].target_node_id}
            for eid in added_edge_ids
        ]

        summary = (
            f"Generation {dag_a.generation} -> {dag_b.generation}: "
            f"+{len(added_node_ids)} nodes, -{len(removed_node_ids)} nodes, "
            f"+{len(added_edge_ids)} edges, -{len(removed_edge_ids)} edges. "
            f"Critical path shifted {crit_dur_b - crit_dur_a:+.1f}ms."
        )

        return GraphDiffResult(
            mission_id=dag_b.mission_id,
            generation_from=dag_a.generation,
            generation_to=dag_b.generation,
            added_nodes=added_nodes_info,
            removed_node_ids=list(removed_node_ids),
            added_edges=added_edges_info,
            removed_edge_ids=list(removed_edge_ids),
            critical_path_delta_ms=round(crit_dur_b - crit_dur_a, 2),
            summary=summary,
        )
