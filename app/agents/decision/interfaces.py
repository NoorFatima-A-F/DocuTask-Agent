"""
Decision Subsystem Interfaces.
Defines IDecisionEngine, IPolicyEvaluator, and IRuleEvaluator contracts.
"""

from abc import ABC, abstractmethod
from typing import Any
from app.agents.decision.context import DecisionContext
from app.agents.decision.policies import CostPolicy
from app.agents.decision.rules import BusinessRule


class IRuleEvaluator(ABC):
    @abstractmethod
    def evaluate_rule(self, rule: BusinessRule, context: DecisionContext) -> bool:
        pass


class IPolicyEvaluator(ABC):
    @abstractmethod
    def evaluate_cost_policy(self, policy: CostPolicy, context: DecisionContext) -> bool:
        pass


class IDecisionEngine(ABC):
    @abstractmethod
    async def evaluate(self, context: DecisionContext) -> Any:
        pass
