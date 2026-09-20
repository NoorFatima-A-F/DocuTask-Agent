"""
Phase 3H.5.6: Interfaces for Failure Learning, RCA & Recovery Optimization
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    FailureEventReport,
    RootCauseReport,
    PatternAnalysisReport,
    KnowledgeBaseReport,
    RecoveryOptimizationReport,
    PolicyImprovementReport,
    FailurePreventionReport,
    AutonomyMatrixReport,
    SimulationReport,
    FailureLearningScorecard,
)


class IFailureEventCollector(ABC):
    @abstractmethod
    def collect_failure_events(self) -> FailureEventReport:
        pass


class IRootCauseEngine(ABC):
    @abstractmethod
    def analyze_root_causes(self) -> RootCauseReport:
        pass


class IPatternRecognitionVerifier(ABC):
    @abstractmethod
    def analyze_patterns(self) -> PatternAnalysisReport:
        pass


class IIncidentKnowledgeBase(ABC):
    @abstractmethod
    def build_knowledge_base(self) -> KnowledgeBaseReport:
        pass


class IRecoveryOptimizationEngine(ABC):
    @abstractmethod
    def optimize_recovery_decisions(self) -> RecoveryOptimizationReport:
        pass


class IPolicyImprovementVerifier(ABC):
    @abstractmethod
    def evaluate_policy_improvements(self) -> PolicyImprovementReport:
        pass


class IFailurePreventionVerifier(ABC):
    @abstractmethod
    def verify_failure_prevention(self) -> FailurePreventionReport:
        pass


class IAutonomyGovernanceVerifier(ABC):
    @abstractmethod
    def verify_autonomy_matrix(self) -> AutonomyMatrixReport:
        pass


class IFailureLearningSimulator(ABC):
    @abstractmethod
    def run_simulation_tests(self) -> SimulationReport:
        pass


class IFailureLearningScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        event_report: FailureEventReport,
        rca_report: RootCauseReport,
        pattern_report: PatternAnalysisReport,
        kb_report: KnowledgeBaseReport,
        optimization_report: RecoveryOptimizationReport,
        policy_report: PolicyImprovementReport,
        prevention_report: FailurePreventionReport,
        autonomy_report: AutonomyMatrixReport,
        simulation_report: SimulationReport,
    ) -> FailureLearningScorecard:
        pass
