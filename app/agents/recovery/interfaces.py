"""
Recovery Subsystem Core Interfaces.
Defines IRecoveryEngine, IFailureClassifier, IRootCauseAnalyzer, IRecoveryStrategySelector, and IRecoveryPlanner.
"""

from abc import ABC, abstractmethod
from app.agents.recovery.context import RecoveryRequest, RecoveryResult
from app.agents.recovery.failure import Failure, FailureEvidence, FailureIdentity
from app.agents.recovery.recovery_graph import RecoveryGraph
from app.agents.recovery.recovery_strategy import RecoveryStrategyDefinition
from app.agents.recovery.root_cause import RootCauseReport


class IFailureClassifier(ABC):
    """Abstract classifier categorizing raw errors into typed Failures."""
    @abstractmethod
    def classify(self, identity: FailureIdentity, evidence: FailureEvidence) -> Failure:
        pass


class IRootCauseAnalyzer(ABC):
    """Abstract root cause diagnostic analyzer."""
    @abstractmethod
    def analyze(self, failure: Failure) -> RootCauseReport:
        pass


class IRecoveryStrategySelector(ABC):
    """Abstract strategy selector."""
    @abstractmethod
    def select_strategy(self, failure: Failure, root_cause: RootCauseReport) -> RecoveryStrategyDefinition:
        pass


class IRecoveryPlanner(ABC):
    """Abstract planner constructing RecoveryGraph DAGs."""
    @abstractmethod
    def plan_recovery(self, failure: Failure, strategy_def: RecoveryStrategyDefinition) -> RecoveryGraph:
        pass


class IRecoveryEngine(ABC):
    """Abstract interface for the autonomous recovery engine."""
    @abstractmethod
    async def recover(self, request: RecoveryRequest) -> RecoveryResult:
        pass
