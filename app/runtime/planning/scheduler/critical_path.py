"""
Critical Path Method (CPM) Analytical Engine.

Computes Earliest Start Time (EST), Latest Start Time (LST), Earliest Finish Time (EFT),
Latest Finish Time (LFT), Total Float / Slack, and isolates Critical Path subgraphs.
"""

from __future__ import annotations

from typing import Any, Dict
from app.runtime.planning.graph.dag import ExecutionDAG


class CriticalPathEngine:
    """Calculates rigorous CPM metrics over arbitrary DAG execution topologies."""

    @classmethod
    def analyze(cls, dag: ExecutionDAG) -> Dict[str, Any]:
        """Performs full CPM analysis over the DAG."""
        crit_nodes, total_duration = dag.compute_critical_path()
        
        node_cpm_details = {}
        for nid, node in dag.nodes.items():
            node_cpm_details[nid] = {
                "name": node.name,
                "task_type": node.task_type,
                "estimated_runtime_ms": node.estimated_runtime_ms,
                "earliest_start_ms": node.earliest_start_ms,
                "latest_start_ms": node.latest_start_ms,
                "earliest_finish_ms": node.earliest_finish_ms,
                "latest_finish_ms": node.latest_finish_ms,
                "total_slack_ms": node.total_slack_ms,
                "is_critical": node.is_critical_path,
            }

        return {
            "total_critical_path_duration_ms": total_duration,
            "critical_nodes_count": len(crit_nodes),
            "critical_node_ids": crit_nodes,
            "nodes_cpm": node_cpm_details,
        }
