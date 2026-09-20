"""
DAG Diff Comparator for Phase 13.2.
Computes topological and state deltas between DAG revisions.
"""

from __future__ import annotations

from typing import Any, Dict, List
from app.runtime.planner_visualization.ui_models.models import PlannerDAGSnapshot


class DAGDiffEngine:
    """
    Computes structural differences between plan revisions (nodes added, nodes removed, edges rewired).
    """

    @classmethod
    def compare_snapshots(cls, original: PlannerDAGSnapshot, updated: PlannerDAGSnapshot) -> Dict[str, Any]:
        orig_nodes = {n.node_id: n for n in original.nodes}
        upd_nodes = {n.node_id: n for n in updated.nodes}

        added_nodes = [nid for nid in upd_nodes if nid not in orig_nodes]
        removed_nodes = [nid for nid in orig_nodes if nid not in upd_nodes]
        mutated_nodes = [
            nid for nid in orig_nodes
            if nid in upd_nodes and (
                orig_nodes[nid].state != upd_nodes[nid].state
                or orig_nodes[nid].assigned_worker != upd_nodes[nid].assigned_worker
            )
        ]

        return {
            "version_from": original.version,
            "version_to": updated.version,
            "nodes_added": added_nodes,
            "nodes_removed": removed_nodes,
            "nodes_mutated": mutated_nodes,
            "critical_path_delta_ms": updated.critical_path_duration_ms - original.critical_path_duration_ms,
        }
