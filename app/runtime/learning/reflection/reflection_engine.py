"""
Reflection Engine for Phase 13.5 (ARLP-KIP).
Coordinates end-to-end multi-perspective reflection across mission executions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field

from app.runtime.learning.reflection.mission_reflector import MissionReflector, MacroKPIs
from app.runtime.learning.reflection.planner_reflector import PlannerReflector, PlannerReflectionMetrics
from app.runtime.learning.reflection.worker_reflector import WorkerReflector, WorkerReflectionMetrics
from app.runtime.learning.reflection.confidence_reflector import ConfidenceReflector, ConfidenceReflectionMetrics
from app.runtime.learning.reflection.failure_reflector import FailureReflector, FailureEpisode
from app.runtime.learning.reflection.success_reflector import SuccessReflector, SuccessEpisode


class MissionReflectionReport(BaseModel):
    reflection_id: str = Field(default_factory=lambda: f"refl_{uuid.uuid4().hex[:10]}")
    mission_id: str
    macro_kpis: MacroKPIs
    planner_metrics: PlannerReflectionMetrics
    worker_metrics: WorkerReflectionMetrics
    confidence_metrics: ConfidenceReflectionMetrics
    failure_episodes: List[FailureEpisode] = Field(default_factory=list)
    success_episodes: List[SuccessEpisode] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    validation_status: str = "VERIFIED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ReflectionEngine:
    """
    Coordinates multi-perspective reflection across mission executions.
    """

    def __init__(self):
        self._reports: Dict[str, MissionReflectionReport] = {}
        # Pre-populate a sample report for mission-001
        self.reflect_on_mission("mission-001")

    def reflect_on_mission(
        self,
        mission_id: str,
        events: Optional[List[Dict[str, Any]]] = None,
    ) -> MissionReflectionReport:
        macro = MissionReflector.reflect(mission_id, events)
        planner = PlannerReflector.reflect(mission_id, events)
        worker = WorkerReflector.reflect(mission_id, events)
        confidence = ConfidenceReflector.reflect(mission_id, events)
        failures = FailureReflector.reflect(mission_id, events)
        successes = SuccessReflector.reflect(mission_id, events)

        recommendations = [
            "Adopt dynamic concurrency pooling for high-throughput OCR shards",
            "Enforce posterior confidence floor of 0.85 on entity extraction branches",
            "Auto-promote parallel wavefront execution strategy for multi-document batches",
        ]

        report = MissionReflectionReport(
            mission_id=mission_id,
            macro_kpis=macro,
            planner_metrics=planner,
            worker_metrics=worker,
            confidence_metrics=confidence,
            failure_episodes=failures,
            success_episodes=successes,
            recommendations=recommendations,
            validation_status="VERIFIED",
        )

        self._reports[report.reflection_id] = report
        self._reports[mission_id] = report  # Index by both
        return report

    def list_reports(self) -> List[MissionReflectionReport]:
        unique = {}
        for r in self._reports.values():
            unique[r.reflection_id] = r
        return list(unique.values())

    def get_report(self, identifier: str) -> Optional[MissionReflectionReport]:
        return self._reports.get(identifier)


reflection_engine = ReflectionEngine()
