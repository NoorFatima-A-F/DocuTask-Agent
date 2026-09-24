"""
Execution Stream Dispatcher for Planner Visualizations.

Bridges planner graph state changes to live WebSockets and SSE streams.
"""

from __future__ import annotations

from typing import Any, Dict
from app.runtime.planning.graph.dag import ExecutionDAG
from app.runtime.planning.visualization.graph_snapshot import VisualGraphSnapshot


class PlannerExecutionStream:
    """Manages real-time visual state push to subscribers."""

    @classmethod
    def create_state_payload(
        cls, dag: ExecutionDAG, active_worker_count: int = 4
    ) -> Dict[str, Any]:
        """Creates complete visual packet for WebSocket transmission."""
        snapshot = VisualGraphSnapshot.generate_snapshot(dag)
        return {
            "type": "PLANNER_GRAPH_UPDATE",
            "mission_id": dag.mission_id,
            "generation": dag.generation,
            "snapshot": snapshot,
            "active_worker_count": active_worker_count,
        }
