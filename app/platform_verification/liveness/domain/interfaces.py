"""
Abstract Interfaces for Enterprise Liveness Verification Framework (Part 3H.2).
"""
from abc import ABC, abstractmethod
from app.platform_verification.liveness.domain.models import (
    LivenessContractReport,
    ResponsivenessReport,
    ProcessStateReport,
    EventLoopHealthReport,
    DeadlockReport,
    WorkerLivenessReport,
    SchedulerLivenessReport,
    ResourceHealthReport,
    FailureSimulationReport,
    RecoveryReport,
    SecurityReport,
    LivenessScorecard,
)


class ILivenessContractManager(ABC):
    @abstractmethod
    def verify_liveness_contracts(self) -> LivenessContractReport:
        pass


class IProcessVerifier(ABC):
    @abstractmethod
    def verify_processes(self) -> ProcessStateReport:
        pass


class IResponsivenessVerifier(ABC):
    @abstractmethod
    def verify_responsiveness(self) -> ResponsivenessReport:
        pass


class IEventLoopMonitor(ABC):
    @abstractmethod
    def monitor_event_loop(self) -> EventLoopHealthReport:
        pass


class IWorkerHeartbeatManager(ABC):
    @abstractmethod
    def evaluate_worker_heartbeats(self) -> WorkerLivenessReport:
        pass


class ISchedulerLivenessMonitor(ABC):
    @abstractmethod
    def check_scheduler_liveness(self) -> SchedulerLivenessReport:
        pass


class IResourceMonitor(ABC):
    @abstractmethod
    def check_resource_health(self) -> ResourceHealthReport:
        pass


class IDeadlockDetector(ABC):
    @abstractmethod
    def detect_deadlocks(self) -> DeadlockReport:
        pass


class ILivenessFailureInjector(ABC):
    @abstractmethod
    def execute_failure_simulations(self) -> FailureSimulationReport:
        pass


class IAutomatedRecoveryVerifier(ABC):
    @abstractmethod
    def verify_recovery(self) -> RecoveryReport:
        pass


class ILivenessSecurityVerifier(ABC):
    @abstractmethod
    def verify_security(self) -> SecurityReport:
        pass


class ILivenessScoreEngine(ABC):
    @abstractmethod
    def compute_scorecard(
        self,
        contract_report: LivenessContractReport,
        process_report: ProcessStateReport,
        loop_report: EventLoopHealthReport,
        deadlock_report: DeadlockReport,
        worker_report: WorkerLivenessReport,
        scheduler_report: SchedulerLivenessReport,
        resource_report: ResourceHealthReport,
        failure_report: FailureSimulationReport,
        recovery_report: RecoveryReport,
        security_report: SecurityReport,
    ) -> LivenessScorecard:
        pass
