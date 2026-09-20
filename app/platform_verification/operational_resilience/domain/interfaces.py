"""
Phase 3H.7: Domain Interfaces for Operational Resilience Verification
"""
from abc import ABC, abstractmethod
from .models import (
    ResilienceArchitectureReport,
    CircuitBreakerReport,
    RetryStrategyReport,
    GracefulDegradationReport,
    BulkheadReport,
    LoadSheddingReport,
    SelfHealingReport,
    ChaosResilienceReport,
    BusinessContinuityReport,
    ResilienceMetricsReport,
    OperationalResilienceScorecard,
)


class IResilienceArchitectureVerifier(ABC):
    @abstractmethod
    def verify_resilience_architecture(self) -> ResilienceArchitectureReport:
        pass


class ICircuitBreakerVerifier(ABC):
    @abstractmethod
    def verify_circuit_breakers(self) -> CircuitBreakerReport:
        pass


class IRetryStrategyVerifier(ABC):
    @abstractmethod
    def verify_retry_strategies(self) -> RetryStrategyReport:
        pass


class IGracefulDegradationVerifier(ABC):
    @abstractmethod
    def verify_graceful_degradation(self) -> GracefulDegradationReport:
        pass


class IBulkheadIsolationVerifier(ABC):
    @abstractmethod
    def verify_bulkhead_isolation(self) -> BulkheadReport:
        pass


class ILoadSheddingVerifier(ABC):
    @abstractmethod
    def verify_load_shedding(self) -> LoadSheddingReport:
        pass


class ISelfHealingVerifier(ABC):
    @abstractmethod
    def verify_self_healing_capabilities(self) -> SelfHealingReport:
        pass


class IChaosResilienceVerifier(ABC):
    @abstractmethod
    def execute_chaos_validation(self) -> ChaosResilienceReport:
        pass


class IBusinessContinuityVerifier(ABC):
    @abstractmethod
    def verify_business_continuity(self) -> BusinessContinuityReport:
        pass


class IResilienceMetricsVerifier(ABC):
    @abstractmethod
    def collect_resilience_metrics(self) -> ResilienceMetricsReport:
        pass


class IOperationalResilienceScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        arch_report: ResilienceArchitectureReport,
        cb_report: CircuitBreakerReport,
        retry_report: RetryStrategyReport,
        degrade_report: GracefulDegradationReport,
        bulkhead_report: BulkheadReport,
        shed_report: LoadSheddingReport,
        self_healing_report: SelfHealingReport,
        chaos_report: ChaosResilienceReport,
        continuity_report: BusinessContinuityReport,
        metrics_report: ResilienceMetricsReport,
    ) -> OperationalResilienceScorecard:
        pass
