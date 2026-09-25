"""Abstract interfaces for Phase 3H.3 Enterprise Readiness Verification Framework."""

from abc import ABC, abstractmethod
from typing import Dict
from .models import (
    ReadinessContractReport,
    DependencyReadinessReport,
    DatabaseReadinessReport,
    QueueReadinessReport,
    WorkerReadinessReport,
    AIProviderReadinessReport,
    StartupReadinessReport,
    FailureSimulationReport,
    OrchestrationReport,
    ReadinessMetricsReport,
    ReadinessCertificationScorecard,
)


class IReadinessContractVerifier(ABC):
    """Interface for verifying GET /ready contract (3H.3.1)."""
    @abstractmethod
    def verify_contract(self) -> ReadinessContractReport:
        pass


class IDependencyReadinessEngine(ABC):
    """Interface for evaluating multi-dependency readiness (3H.3.2)."""
    @abstractmethod
    def evaluate_dependencies(
        self,
        db_rep: DatabaseReadinessReport,
        queue_rep: QueueReadinessReport,
        worker_rep: WorkerReadinessReport,
        ai_rep: AIProviderReadinessReport,
    ) -> DependencyReadinessReport:
        pass


class IDatabaseReadinessVerifier(ABC):
    """Interface for database readiness verification (3H.3.3)."""
    @abstractmethod
    def verify_database(self) -> DatabaseReadinessReport:
        pass


class IQueueReadinessVerifier(ABC):
    """Interface for queue readiness verification (3H.3.4)."""
    @abstractmethod
    def verify_queue(self) -> QueueReadinessReport:
        pass


class IWorkerCapacityVerifier(ABC):
    """Interface for worker fleet capacity verification (3H.3.5)."""
    @abstractmethod
    def verify_worker_capacity(self) -> WorkerReadinessReport:
        pass


class IAIProviderReadinessVerifier(ABC):
    """Interface for AI provider readiness verification (3H.3.6)."""
    @abstractmethod
    def verify_ai_provider(self) -> AIProviderReadinessReport:
        pass


class IStartupReadinessVerifier(ABC):
    """Interface for startup readiness sequencing verification (3H.3.7)."""
    @abstractmethod
    def verify_startup_sequence(self) -> StartupReadinessReport:
        pass


class IReadinessFailureSimulator(ABC):
    """Interface for controlled readiness failure simulations (3H.3.8)."""
    @abstractmethod
    def run_failure_simulations(self) -> FailureSimulationReport:
        pass


class IOrchestratorIntegrationVerifier(ABC):
    """Interface for Kubernetes/Orchestrator integration verification (3H.3.9)."""
    @abstractmethod
    def verify_orchestration(self) -> OrchestrationReport:
        pass


class IReadinessObservabilityExporter(ABC):
    """Interface for Prometheus metrics & dashboards (3H.3.10)."""
    @abstractmethod
    def export_observability(self) -> ReadinessMetricsReport:
        pass


class IReadinessCertificationScorer(ABC):
    """Interface for 6-dimension weighted readiness scoring (3H.3.11)."""
    @abstractmethod
    def score_readiness(
        self,
        contract_rep: ReadinessContractReport,
        dep_rep: DependencyReadinessReport,
        db_rep: DatabaseReadinessReport,
        queue_rep: QueueReadinessReport,
        worker_rep: WorkerReadinessReport,
        ai_rep: AIProviderReadinessReport,
        startup_rep: StartupReadinessReport,
        sim_rep: FailureSimulationReport,
        orch_rep: OrchestrationReport,
        obs_rep: ReadinessMetricsReport,
    ) -> ReadinessCertificationScorecard:
        pass


class IReadinessEvidenceExporter(ABC):
    """Interface for exporting 11 JSON manifests into health_verification/ (3H.3.12)."""
    @abstractmethod
    def export_all(
        self,
        contract_rep: ReadinessContractReport,
        dep_rep: DependencyReadinessReport,
        db_rep: DatabaseReadinessReport,
        queue_rep: QueueReadinessReport,
        worker_rep: WorkerReadinessReport,
        ai_rep: AIProviderReadinessReport,
        startup_rep: StartupReadinessReport,
        sim_rep: FailureSimulationReport,
        orch_rep: OrchestrationReport,
        obs_rep: ReadinessMetricsReport,
        scorecard: ReadinessCertificationScorecard,
    ) -> Dict[str, str]:
        pass
