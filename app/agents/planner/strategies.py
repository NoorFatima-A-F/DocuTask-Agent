"""
Planning Strategy Selection and Handler Implementations.
"""

from abc import ABC, abstractmethod
from typing import List
from app.agents.planner.context import PlannerRequest
from app.agents.planner.strategy import PlanningStrategy
from app.agents.planning.contracts import Plan


class IPlanningStrategyHandler(ABC):
    """Abstract strategy handler."""
    @property
    @abstractmethod
    def strategy_name(self) -> PlanningStrategy:
        pass


class HierarchicalPlanningStrategy(IPlanningStrategyHandler):
    @property
    def strategy_name(self) -> PlanningStrategy:
        return PlanningStrategy.HIERARCHICAL


class TopDownPlanningStrategy(IPlanningStrategyHandler):
    @property
    def strategy_name(self) -> PlanningStrategy:
        return PlanningStrategy.TOP_DOWN


class LeastCostPlanningStrategy(IPlanningStrategyHandler):
    @property
    def strategy_name(self) -> PlanningStrategy:
        return PlanningStrategy.LEAST_COST


class LLMGuidedPlanningStrategy(IPlanningStrategyHandler):
    @property
    def strategy_name(self) -> PlanningStrategy:
        return PlanningStrategy.LLM_GUIDED
