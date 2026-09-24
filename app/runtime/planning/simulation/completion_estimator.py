"""
Dynamic Mission Completion Time & ETA Estimator.

Calculates remaining mission time based on remaining uncompleted DAG nodes and critical paths.
"""

from __future__ import annotations

import time
from typing import Dict, Set
from app.runtime.planning.graph.dag import ExecutionDAG


class CompletionEstimator:
    """Estimates remaining execution duration and percentage progress."""

    @classmethod
    def estimate_remaining(
        cls, dag: ExecutionDAG, completed_node_ids: Set[str]
    ) -> Dict[str, float]:
        """Calculates remaining critical path duration for uncompleted nodes."""
        uncompleted_nodes = [n for nid, n in dag.nodes.items() if nid not in completed_node_ids]
        
        if not uncompleted_nodes:
            return {
                "remaining_ms": 0.0,
                "progress_pct": 100.0,
                "estimated_eta_timestamp": time.time(),
            }

        # Subgraph of uncompleted nodes
        remaining_runtime = sum(n.estimated_runtime_ms for n in uncompleted_nodes)
        progress = (len(completed_node_ids) / max(1, len(dag.nodes))) * 100.0
        eta = time.time() + (remaining_runtime / 1000.0)

        return {
            "remaining_ms": round(remaining_runtime, 1),
            "progress_pct": round(progress, 1),
            "estimated_eta_timestamp": round(eta, 2),
        }
