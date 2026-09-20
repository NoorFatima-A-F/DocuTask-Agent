"""
Planner API Service for Phase 13.2.
Aggregates planner lifecycle, DAG, scheduler, decision, and metric engines into unified query endpoints.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.runtime.planner_visualization.planner_lifecycle.lifecycle_engine import PlannerLifecycleEngine
from app.runtime.planner_visualization.planner_lifecycle.goal_analyzer import GoalAnalysisEngine
from app.runtime.planner_visualization.planner_lifecycle.task_decomposer import TaskDecompositionEngine
from app.runtime.planner_visualization.dag.dag_engine import DAGBuilderEngine
from app.runtime.planner_visualization.dag.dag_mutator import DAGMutationEngine
from app.runtime.planner_visualization.dag.critical_path import CriticalPathEngine
from app.runtime.planner_visualization.scheduler.scheduler_engine import SchedulerEngine
from app.runtime.planner_visualization.scheduler.queue_manager import RuntimeQueueManager
from app.runtime.planner_visualization.worker_assignment.worker_assigner import WorkerAssignmentEngine
from app.runtime.planner_visualization.replanning.replanning_coordinator import ReplanningCoordinator
from app.runtime.planner_visualization.graph_projection.dag_projection import DAGProjection
from app.runtime.planner_visualization.timeline.planner_timeline import PlannerTimelineService
from app.runtime.planner_visualization.metrics.planner_metrics import PlannerMetricsCalculator
from app.runtime.planner_visualization.metrics.decision_ledger import PlannerDecisionLedger


class PlannerAPIService:
    """
    Singleton aggregator service for Planner Execution Visualization (Phase 13.2).
    """

    _instances: Dict[str, PlannerAPIService] = {}

    def __init__(self, mission_id: str = "mission-001"):
        self.mission_id = mission_id
        self.lifecycle = PlannerLifecycleEngine(mission_id=mission_id)
        self.goal_analyzer = GoalAnalysisEngine(mission_id=mission_id)
        self.task_decomposer = TaskDecompositionEngine(mission_id=mission_id)
        self.dag_builder = DAGBuilderEngine(mission_id=mission_id)
        self.dag_mutator = DAGMutationEngine(self.dag_builder)
        self.scheduler = SchedulerEngine(mission_id=mission_id)
        self.queue_mgr = RuntimeQueueManager(mission_id=mission_id)
        self.worker_assigner = WorkerAssignmentEngine(mission_id=mission_id)
        self.replanner = ReplanningCoordinator(self.dag_builder, self.dag_mutator)
        self.projection = DAGProjection(mission_id=mission_id)
        self.timeline_svc = PlannerTimelineService(mission_id=mission_id)
        self.metrics_calc = PlannerMetricsCalculator(self.dag_builder)
        self.decision_ledger = PlannerDecisionLedger(mission_id=mission_id)

    @classmethod
    def get_instance(cls, mission_id: str = "mission-001") -> PlannerAPIService:
        if mission_id not in cls._instances:
            cls._instances[mission_id] = PlannerAPIService(mission_id)
        return cls._instances[mission_id]

    def get_state(self) -> Dict[str, Any]:
        return self.lifecycle.get_state()

    def get_lifecycle_timeline(self) -> List[Dict[str, Any]]:
        return self.lifecycle.get_timeline()

    def get_goal_analysis(self) -> Dict[str, Any]:
        return self.goal_analyzer.analyze_goal("Process and validate 2026 Q3 vendor audit invoices").model_dump()

    def get_task_decomposition(self) -> List[Dict[str, Any]]:
        nodes = self.task_decomposer.decompose("Process and validate 2026 Q3 vendor audit invoices")
        return [n.model_dump() for n in nodes]

    def get_dag_snapshot(self) -> Dict[str, Any]:
        return self.dag_builder.get_snapshot().model_dump()

    def get_critical_path(self) -> Dict[str, Any]:
        snapshot = self.dag_builder.get_snapshot()
        return CriticalPathEngine.compute_critical_path(snapshot.nodes, snapshot.edges)

    def get_queues(self) -> Dict[str, Any]:
        return self.queue_mgr.get_queues()

    def get_scheduler_status(self) -> Dict[str, Any]:
        return self.scheduler.get_scheduler_status()

    def get_workers(self) -> List[Dict[str, Any]]:
        assignments = self.worker_assigner.get_assignments()
        return [a.model_dump() for a in assignments]

    def get_replanning_history(self) -> List[Dict[str, Any]]:
        return self.replanner.get_history()

    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics_calc.compute_metrics().model_dump()

    def get_decisions(self) -> List[Dict[str, Any]]:
        decisions = self.decision_ledger.get_decisions()
        return [d.model_dump() for d in decisions]

    def get_timeline(self) -> List[Dict[str, Any]]:
        return self.timeline_svc.get_timeline()
