"""
Interfaces and Abstract Protocols for Disaster Recovery Simulation Framework (Part 3G.3).
"""
from abc import ABC, abstractmethod
from typing import List
from app.platform_verification.disaster_recovery_simulation.domain.models import (
    ScenarioSimulationResult,
    ChaosExperimentResult,
    IncidentDetectionResult,
    PostRecoveryValidationReport,
    TabletopExerciseResult,
    ResilienceScorecard,
)


class IDisasterScenario(ABC):
    @abstractmethod
    def execute_simulation(self) -> ScenarioSimulationResult:
        pass


class IChaosInjector(ABC):
    @abstractmethod
    def inject_failure(self) -> ChaosExperimentResult:
        pass


class IIncidentDetector(ABC):
    @abstractmethod
    def test_incident_detection(self) -> IncidentDetectionResult:
        pass


class IRecoveryValidationEngine(ABC):
    @abstractmethod
    def validate_post_recovery_system(self) -> PostRecoveryValidationReport:
        pass


class IResilienceMetricsEngine(ABC):
    @abstractmethod
    def compute_resilience_scorecard(
        self,
        scenario_results: List[ScenarioSimulationResult],
        chaos_results: List[ChaosExperimentResult],
        detection_result: IncidentDetectionResult,
        validation_report: PostRecoveryValidationReport,
        tabletop_result: TabletopExerciseResult,
    ) -> ResilienceScorecard:
        pass
