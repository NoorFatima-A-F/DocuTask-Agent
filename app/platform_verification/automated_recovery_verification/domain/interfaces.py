"""
Phase 3H.12: Enterprise Automated Recovery & Self-Healing — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    RecoveryArchitectureReport,
    RecoveryPolicyReport,
    ServiceRestartReport,
    DatabaseRecoveryReport,
    QueueRecoveryReport,
    WorkerRecoveryReport,
    AIRecoveryReport,
    CircuitBreakerReport,
    RecoveryValidationReport,
    ReliabilityMetricsReport,
    RecoverySafetyReport,
    RecoveryAuditReport,
    RecoveryCertificationReport,
)


class IRecoveryArchitectureVerifier(ABC):
    @abstractmethod
    def verify_recovery_architecture(self) -> RecoveryArchitectureReport:
        pass


class IRecoveryPolicyVerifier(ABC):
    @abstractmethod
    def verify_recovery_policies(self) -> RecoveryPolicyReport:
        pass


class IServiceRestartVerifier(ABC):
    @abstractmethod
    def verify_service_restart(self) -> ServiceRestartReport:
        pass


class IDatabaseRecoveryVerifier(ABC):
    @abstractmethod
    def verify_database_recovery(self) -> DatabaseRecoveryReport:
        pass


class IQueueRecoveryVerifier(ABC):
    @abstractmethod
    def verify_queue_recovery(self) -> QueueRecoveryReport:
        pass


class IWorkerSelfHealingVerifier(ABC):
    @abstractmethod
    def verify_worker_self_healing(self) -> WorkerRecoveryReport:
        pass


class IAIRecoveryVerifier(ABC):
    @abstractmethod
    def verify_ai_recovery(self) -> AIRecoveryReport:
        pass


class ICircuitBreakerVerifier(ABC):
    @abstractmethod
    def verify_circuit_breaker(self) -> CircuitBreakerReport:
        pass


class IRecoveryValidationEngineVerifier(ABC):
    @abstractmethod
    def verify_validation_engine(self) -> RecoveryValidationReport:
        pass


class IReliabilityMetricsVerifier(ABC):
    @abstractmethod
    def verify_reliability_metrics(self) -> ReliabilityMetricsReport:
        pass


class IRecoverySafetyVerifier(ABC):
    @abstractmethod
    def verify_recovery_safety(self) -> RecoverySafetyReport:
        pass


class IRecoveryAuditVerifier(ABC):
    @abstractmethod
    def verify_recovery_audit(self) -> RecoveryAuditReport:
        pass


class IAutomatedRecoveryScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        arch_report: RecoveryArchitectureReport,
        policy_report: RecoveryPolicyReport,
        restart_report: ServiceRestartReport,
        db_report: DatabaseRecoveryReport,
        queue_report: QueueRecoveryReport,
        worker_report: WorkerRecoveryReport,
        ai_report: AIRecoveryReport,
        circuit_report: CircuitBreakerReport,
        validation_report: RecoveryValidationReport,
        metrics_report: ReliabilityMetricsReport,
        safety_report: RecoverySafetyReport,
        audit_report: RecoveryAuditReport,
    ) -> RecoveryCertificationReport:
        pass


class IAutomatedRecoveryExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: RecoveryArchitectureReport,
        policy_report: RecoveryPolicyReport,
        restart_report: ServiceRestartReport,
        db_report: DatabaseRecoveryReport,
        queue_report: QueueRecoveryReport,
        worker_report: WorkerRecoveryReport,
        ai_report: AIRecoveryReport,
        circuit_report: CircuitBreakerReport,
        validation_report: RecoveryValidationReport,
        metrics_report: ReliabilityMetricsReport,
        safety_report: RecoverySafetyReport,
        audit_report: RecoveryAuditReport,
        certification_report: RecoveryCertificationReport,
    ) -> Dict[str, Any]:
        pass
