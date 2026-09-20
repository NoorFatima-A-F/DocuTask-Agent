"""
Planner Subsystem Injectable Factory.
Wires IntelligentPlanner, PlannerManager, PlanningPipeline, PlannerCache, and PlannerMetricsCollector.
"""

from typing import Optional
from app.agents.planner.cache import PlannerCache
from app.agents.planner.engine import PlanningEngine
from app.agents.planner.manager import PlannerManager
from app.agents.planner.metrics import PlannerMetricsCollector
from app.agents.planner.pipeline import PlanningPipeline
from app.agents.planner.planner import IntelligentPlanner
from app.agents.planner.repository import PlannerRepository


class PlannerFactory:
    """Factory container wiring intelligent planner subsystem components."""

    @staticmethod
    def create_planner_subsystem(
        pipeline: Optional[PlanningPipeline] = None
    ):
        pipe = pipeline or PlanningPipeline()
        engine = PlanningEngine(pipeline=pipe)
        planner = IntelligentPlanner(engine=engine)
        cache = PlannerCache()
        repo = PlannerRepository()
        manager = PlannerManager(planner=planner, cache=cache, repository=repo)
        metrics = PlannerMetricsCollector()
        return manager, planner, metrics
