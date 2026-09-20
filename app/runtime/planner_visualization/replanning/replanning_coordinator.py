"""
Replanning Coordinator for Phase 13.2.
Coordinates in-flight replanning, strategy adaptation, and recovery node injection upon failure.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from app.runtime.planner_visualization.dag.dag_engine import DAGBuilderEngine
from app.runtime.planner_visualization.dag.dag_mutator import DAGMutationEngine
from app.runtime.planner_visualization.ui_models.models import PlannerStateEnum
from app.runtime.events.bus.event_bus import get_global_event_bus
from app.runtime.events.models.planner_event import PlannerEventFactory


class ReplanningCoordinator:
    """
    Handles autonomous replanning when failures occur, mutating the DAG and reassigning workers.
    """

    def __init__(self, dag_builder: DAGBuilderEngine, dag_mutator: DAGMutationEngine):
        self.dag_builder = dag_builder
        self.dag_mutator = dag_mutator
        self.replan_history: List[Dict[str, Any]] = []

    def trigger_replan_on_failure(self, failed_node_id: str, reason: str, alternative_strategy: str = "FALLBACK_OCR") -> Dict[str, Any]:
        # 1. Inject recovery branch into DAG (emits replanned event)
        mutation_res = self.dag_mutator.inject_recovery_node(failed_node_id, recovery_strategy=alternative_strategy)

        replan_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "failed_node_id": failed_node_id,
            "reason": reason,
            "strategy": alternative_strategy,
            "new_version": self.dag_builder.version,
            "status": "REPLANNED_AND_RESUMED",
        }
        self.replan_history.append(replan_record)

        return {
            "status": "SUCCESS",
            "replan_record": replan_record,
            "updated_snapshot": self.dag_builder.get_snapshot(),
        }

    def get_history(self) -> List[Dict[str, Any]]:
        return self.replan_history
