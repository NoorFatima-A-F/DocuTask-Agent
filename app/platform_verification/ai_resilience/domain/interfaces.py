"""Abstract interfaces for Phase 3H.3.10 - AI Failure Simulation & Resilience Verification Framework."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    FailureInjectionScenario,
    OutageSimulationReport,
    LatencyChaosReport,
    MalformedResponseReport,
    AuthFailureReport,
    QuotaExhaustionReport,
    NetworkFailureReport,
    QualityDegradationReport,
    FallbackVerificationReport,
    TaskPreservationReport,
    CircuitBreakerReport,
    ChaosExperimentResult,
    RecoveryMetricsReport,
    AIResilienceScorecard,
)


class IAIFailureSimulator(ABC):
    """Interface for central AI Chaos Simulation & Fault Injection."""
    @abstractmethod
    def list_scenarios(self) -> List[FailureInjectionScenario]:
        pass

    @abstractmethod
    def inject_fault(self, scenario: FailureInjectionScenario, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        pass


class IProviderOutageVerifier(ABC):
    """Interface for verifying AI Provider Outage handling (3H.3.10.2)."""
    @abstractmethod
    def verify_outage_handling(self, request_count: int = 100) -> OutageSimulationReport:
        pass


class ILatencyChaosVerifier(ABC):
    """Interface for verifying AI Latency Chaos & Timeouts (3H.3.10.3)."""
    @abstractmethod
    def verify_latency_chaos(self, test_count: int = 50) -> LatencyChaosReport:
        pass


class IMalformedResponseVerifier(ABC):
    """Interface for verifying Malformed Response & Schema Integrity (3H.3.10.4)."""
    @abstractmethod
    def verify_malformed_responses(self, test_count: int = 50) -> MalformedResponseReport:
        pass


class IAuthFailureVerifier(ABC):
    """Interface for verifying AI Authentication Failure handling (3H.3.10.5)."""
    @abstractmethod
    def verify_auth_failures(self) -> AuthFailureReport:
        pass


class IQuotaExhaustionVerifier(ABC):
    """Interface for verifying AI Quota & 429 Exhaustion handling (3H.3.10.6)."""
    @abstractmethod
    def verify_quota_exhaustion(self, rate_limited_count: int = 60) -> QuotaExhaustionReport:
        pass


class INetworkFailureVerifier(ABC):
    """Interface for verifying AI Network & Connection failure handling (3H.3.10.7)."""
    @abstractmethod
    def verify_network_failures(self, fault_count: int = 45) -> NetworkFailureReport:
        pass


class IQualityDegradationVerifier(ABC):
    """Interface for verifying AI Quality & Hallucination detection (3H.3.10.8)."""
    @abstractmethod
    def verify_quality_degradation(self, degraded_count: int = 60) -> QualityDegradationReport:
        pass


class IFallbackVerifier(ABC):
    """Interface for verifying Multi-Provider Fallback & Failover (3H.3.10.9)."""
    @abstractmethod
    def verify_fallback_switching(self, failover_tests: int = 30) -> FallbackVerificationReport:
        pass


class ITaskPreservationVerifier(ABC):
    """Interface for verifying Task State & Document Preservation (3H.3.10.10)."""
    @abstractmethod
    def verify_task_preservation(self, document_count: int = 100) -> TaskPreservationReport:
        pass


class ICircuitBreakerVerifier(ABC):
    """Interface for verifying AI Circuit Breaker lifecycle (3H.3.10.11)."""
    @abstractmethod
    def verify_circuit_breaker(self, failure_threshold: int = 5) -> CircuitBreakerReport:
        pass


class IChaosExperimentRunner(ABC):
    """Interface for automated chaos experiment coordinator (3H.3.10.12)."""
    @abstractmethod
    def run_all_experiments(self, documents_per_experiment: int = 50) -> List[ChaosExperimentResult]:
        pass


class IRecoveryMetricsCollector(ABC):
    """Interface for collecting resilience & recovery metrics (3H.3.10.13)."""
    @abstractmethod
    def collect_recovery_metrics(self, experiment_results: List[ChaosExperimentResult]) -> RecoveryMetricsReport:
        pass


class IEvidenceExporter(ABC):
    """Interface for exporting structured resilience verification manifests (3H.3.10.14)."""
    @abstractmethod
    def export_all(
        self,
        outage_report: OutageSimulationReport,
        latency_report: LatencyChaosReport,
        malformed_report: MalformedResponseReport,
        auth_report: AuthFailureReport,
        quota_report: QuotaExhaustionReport,
        network_report: NetworkFailureReport,
        quality_report: QualityDegradationReport,
        fallback_report: FallbackVerificationReport,
        preservation_report: TaskPreservationReport,
        circuit_breaker_report: CircuitBreakerReport,
        recovery_metrics: RecoveryMetricsReport,
        scorecard: AIResilienceScorecard,
    ) -> Dict[str, str]:
        pass


class IAIResilienceScorer(ABC):
    """Interface for 6-dimension weighted AI Resilience Quality Scoring (3H.3.10.15)."""
    @abstractmethod
    def calculate_scorecard(
        self,
        outage_report: OutageSimulationReport,
        latency_report: LatencyChaosReport,
        malformed_report: MalformedResponseReport,
        auth_report: AuthFailureReport,
        quota_report: QuotaExhaustionReport,
        network_report: NetworkFailureReport,
        quality_report: QualityDegradationReport,
        fallback_report: FallbackVerificationReport,
        preservation_report: TaskPreservationReport,
        circuit_breaker_report: CircuitBreakerReport,
        recovery_metrics: RecoveryMetricsReport,
    ) -> AIResilienceScorecard:
        pass
