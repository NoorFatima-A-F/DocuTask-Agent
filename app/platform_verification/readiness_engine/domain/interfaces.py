"""
Abstract interfaces and protocols for Part 3H.3.2.
"""
from typing import Dict, Any, Protocol
from app.platform_verification.readiness_engine.domain.models import (
    DatabaseReadinessReport,
    QueueReadinessReport,
    StorageReadinessReport,
    AIProviderReadinessReport,
    WorkerReadinessReport,
    DependencyMatrixReport,
    ReadinessEvaluationResult,
    FailureSimulationReport,
    KubernetesCompatibilityReport,
    ReadinessSecurityReport,
    ReadinessScorecard,
)


class IDatabaseReadinessChecker(Protocol):
    def check_readiness(self) -> DatabaseReadinessReport: ...


class IQueueReadinessChecker(Protocol):
    def check_readiness(self) -> QueueReadinessReport: ...


class IStorageReadinessChecker(Protocol):
    def check_readiness(self) -> StorageReadinessReport: ...


class IAIProviderReadinessChecker(Protocol):
    def check_readiness(self) -> AIProviderReadinessReport: ...


class IWorkerReadinessChecker(Protocol):
    def check_readiness(self) -> WorkerReadinessReport: ...


class IDependencyPolicyEngine(Protocol):
    def evaluate_dependencies(self) -> DependencyMatrixReport: ...


class IReadinessEvaluator(Protocol):
    def evaluate_readiness(self) -> ReadinessEvaluationResult: ...


class IFailureSimulationRunner(Protocol):
    def run_all_simulations(self) -> FailureSimulationReport: ...


class IKubernetesReadinessVerifier(Protocol):
    def verify_kubernetes_compatibility(self) -> KubernetesCompatibilityReport: ...


class IReadinessSecurityAuditor(Protocol):
    def audit_security(self, payload: Dict[str, Any]) -> ReadinessSecurityReport: ...


class IReadinessQualityScorer(Protocol):
    def compute_scorecard(
        self,
        db_report: DatabaseReadinessReport,
        queue_report: QueueReadinessReport,
        storage_report: StorageReadinessReport,
        ai_report: AIProviderReadinessReport,
        worker_report: WorkerReadinessReport,
        matrix_report: DependencyMatrixReport,
        eval_result: ReadinessEvaluationResult,
        sim_report: FailureSimulationReport,
        k8s_report: KubernetesCompatibilityReport,
        sec_report: ReadinessSecurityReport,
        observability_valid: bool,
    ) -> ReadinessScorecard: ...
