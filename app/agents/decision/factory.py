"""
Decision Subsystem Injectable Factory.
"""

from app.agents.decision.engine import DecisionEngine
from app.agents.decision.governance import GovernanceFramework
from app.agents.decision.manager import DecisionManager
from app.agents.decision.metrics import DecisionMetricsCollector


class DecisionFactory:
    @staticmethod
    def create_decision_subsystem():
        gov = GovernanceFramework()
        engine = DecisionEngine(governance=gov)
        manager = DecisionManager(engine=engine)
        metrics = DecisionMetricsCollector()
        return manager, engine, metrics
