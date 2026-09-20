"""
Planning Subsystem Injectable Factory.
Wires PlanManager, PlanRepository, PlanValidator, PlanCache, and PlanningMetricsCollector.
"""

from typing import Optional
from app.agents.planning.cache import PlanCache
from app.agents.planning.interfaces import IPlanRepository, IPlanValidator
from app.agents.planning.manager import PlanManager
from app.agents.planning.metrics import PlanningMetricsCollector
from app.agents.planning.repository import PlanRepository
from app.agents.planning.validation import PlanValidator


class PlanningFactory:
    """Factory container wiring planning subsystem components."""

    @staticmethod
    def create_planning_subsystem(
        repository: Optional[IPlanRepository] = None,
        validator: Optional[IPlanValidator] = None
    ):
        repo = repository or PlanRepository()
        val = validator or PlanValidator()
        cache = PlanCache()
        manager = PlanManager(repository=repo, validator=val, cache=cache)
        metrics = PlanningMetricsCollector()
        return manager, val, metrics
