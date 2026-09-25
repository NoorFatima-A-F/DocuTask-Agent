"""
Phase 3H.5.5: Enterprise Health Self-Healing - Abstract Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    FailureClassificationReport,
    RecoveryPolicyReport,
    RecoveryExecutionReport,
    HealthRecoveryReport,
    DependencyRestoreReport,
    WorkflowValidationReport,
    PerformanceRecoveryReport,
    StabilityWindowReport,
    RecoveryValidationReport,
    SelfHealingScorecard,
)


class ISelfHealingArchitectureVerifier(ABC):
    @abstractmethod
    def verify_architecture(self) -> Dict[str, Any]:
        pass


class IFailureClassificationVerifier(ABC):
    @abstractmethod
    def verify_failure_classification(self) -> FailureClassificationReport:
        pass


class IRecoveryPolicyEngine(ABC):
    @abstractmethod
    def evaluate_policies(self) -> RecoveryPolicyReport:
        pass


class IRecoveryExecutionVerifier(ABC):
    @abstractmethod
    def verify_recovery_executions(self) -> RecoveryExecutionReport:
        pass


class ILayer1HealthRecoveryVerifier(ABC):
    @abstractmethod
    def validate_service_health(self) -> HealthRecoveryReport:
        pass


class ILayer2DependencyRestoreVerifier(ABC):
    @abstractmethod
    def validate_dependency_restoration(self) -> DependencyRestoreReport:
        pass


class ILayer3WorkflowRecoveryVerifier(ABC):
    @abstractmethod
    def validate_functional_workflow(self) -> WorkflowValidationReport:
        pass


class ILayer4PerformanceRecoveryVerifier(ABC):
    @abstractmethod
    def validate_performance_recovery(self) -> PerformanceRecoveryReport:
        pass


class ILayer5StabilityWindowVerifier(ABC):
    @abstractmethod
    def validate_stability_window(self) -> StabilityWindowReport:
        pass


class ISelfHealingScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        classification_report: FailureClassificationReport,
        execution_report: RecoveryExecutionReport,
        validation_report: RecoveryValidationReport,
    ) -> SelfHealingScorecard:
        pass


class ISelfHealingEvidenceExporter(ABC):
    @abstractmethod
    def export_evidence_manifests(
        self,
        output_dir: str,
        validation_report: RecoveryValidationReport,
        scorecard: SelfHealingScorecard,
    ) -> List[str]:
        pass
