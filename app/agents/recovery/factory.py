"""
Recovery Subsystem Injectable Factory.
Wires RecoveryEngine, RecoveryManager, RecoveryRuntime, FailureClassifier,
RootCauseAnalyzer, RecoveryStrategySelector, and DeadLetterQueue.
"""

from typing import Optional
from app.agents.recovery.dead_letter import DeadLetterQueue
from app.agents.recovery.engine import RecoveryEngine
from app.agents.recovery.failure_classifier import FailureClassifier
from app.agents.recovery.incident_manager import IncidentManager
from app.agents.recovery.manager import RecoveryManager
from app.agents.recovery.metrics import RecoveryMetricsCollector
from app.agents.recovery.recovery_executor import RecoveryExecutor
from app.agents.recovery.recovery_planner import RecoveryPlanner
from app.agents.recovery.repository import RecoveryRepository
from app.agents.recovery.root_cause import RootCauseAnalyzer
from app.agents.recovery.runtime import RecoveryRuntime
from app.agents.recovery.strategy_selector import RecoveryStrategySelector


class RecoveryFactory:
    """Factory container wiring autonomous recovery components."""

    @staticmethod
    def create_recovery_subsystem():
        classifier = FailureClassifier()
        root_cause_analyzer = RootCauseAnalyzer()
        strategy_selector = RecoveryStrategySelector()
        planner = RecoveryPlanner()
        executor = RecoveryExecutor()

        engine = RecoveryEngine(
            classifier=classifier,
            root_cause_analyzer=root_cause_analyzer,
            strategy_selector=strategy_selector,
            planner=planner,
            executor=executor
        )

        dead_letter = DeadLetterQueue()
        incident_mgr = IncidentManager()
        manager = RecoveryManager(
            engine=engine,
            dead_letter_queue=dead_letter,
            incident_manager=incident_mgr
        )
        runtime = RecoveryRuntime(engine=engine)
        metrics = RecoveryMetricsCollector()
        repo = RecoveryRepository()

        return manager, runtime, engine, dead_letter, incident_mgr, metrics, repo
