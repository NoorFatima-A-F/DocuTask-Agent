"""
Phase 3H.11: Enterprise Health Failure Simulation & Chaos Verification — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    ChaosArchitectureReport,
    ScenarioRegistryReport,
    DatabaseFailureReport,
    QueueFailureReport,
    WorkerFailureReport,
    AIProviderFailureReport,
    ResourceFailureReport,
    FailureDetectionMetricsReport,
    RollbackValidationReport,
    ChaosSafetyReport,
    ChaosCertificationReport,
)


class IChaosArchitectureVerifier(ABC):
    @abstractmethod
    def verify_chaos_architecture(self) -> ChaosArchitectureReport:
        pass


class IScenarioRegistryVerifier(ABC):
    @abstractmethod
    def verify_scenario_registry(self) -> ScenarioRegistryReport:
        pass


class IDatabaseFailureVerifier(ABC):
    @abstractmethod
    def verify_database_failure(self) -> DatabaseFailureReport:
        pass


class IQueueFailureVerifier(ABC):
    @abstractmethod
    def verify_queue_failure(self) -> QueueFailureReport:
        pass


class IWorkerFailureVerifier(ABC):
    @abstractmethod
    def verify_worker_failure(self) -> WorkerFailureReport:
        pass


class IAIProviderFailureVerifier(ABC):
    @abstractmethod
    def verify_ai_failure(self) -> AIProviderFailureReport:
        pass


class IResourceFailureVerifier(ABC):
    @abstractmethod
    def verify_resource_failure(self) -> ResourceFailureReport:
        pass


class IFailureDetectionMetricsVerifier(ABC):
    @abstractmethod
    def verify_detection_metrics(self) -> FailureDetectionMetricsReport:
        pass


class IRollbackValidationVerifier(ABC):
    @abstractmethod
    def verify_rollback(self) -> RollbackValidationReport:
        pass


class IChaosSafetyVerifier(ABC):
    @abstractmethod
    def verify_safety(self) -> ChaosSafetyReport:
        pass


class IChaosReliabilityScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        arch_report: ChaosArchitectureReport,
        registry_report: ScenarioRegistryReport,
        db_report: DatabaseFailureReport,
        queue_report: QueueFailureReport,
        worker_report: WorkerFailureReport,
        ai_report: AIProviderFailureReport,
        resource_report: ResourceFailureReport,
        detection_report: FailureDetectionMetricsReport,
        rollback_report: RollbackValidationReport,
        safety_report: ChaosSafetyReport,
    ) -> ChaosCertificationReport:
        pass


class IChaosEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: ChaosArchitectureReport,
        registry_report: ScenarioRegistryReport,
        db_report: DatabaseFailureReport,
        queue_report: QueueFailureReport,
        worker_report: WorkerFailureReport,
        ai_report: AIProviderFailureReport,
        resource_report: ResourceFailureReport,
        detection_report: FailureDetectionMetricsReport,
        rollback_report: RollbackValidationReport,
        safety_report: ChaosSafetyReport,
        certification_report: ChaosCertificationReport,
    ) -> Dict[str, Any]:
        pass
