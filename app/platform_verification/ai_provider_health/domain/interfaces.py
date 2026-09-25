"""Domain interfaces for AI Provider Health Verification."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.platform_verification.ai_provider_health.domain.models import (
    AIAuthReport,
    AIConnectivityReport,
    AIDegradedModeReport,
    AIFailureClassificationReport,
    AIFailureSimulationReport,
    AIFailoverReport,
    AILatencyReport,
    AIMonitoringReport,
    AIProviderHealthReport,
    AIQuotaReport,
    AIResponseIntegrityReport,
    AISecurityReport,
    AITimeoutReport,
    AIHealthQualityScorecard,
)


class IAIProviderHealthContractVerifier(ABC):
    @abstractmethod
    def verify_provider_health(self) -> AIProviderHealthReport:
        pass


class IAIAuthVerifier(ABC):
    @abstractmethod
    def verify_authentication(self) -> AIAuthReport:
        pass


class IAIConnectivityVerifier(ABC):
    @abstractmethod
    def verify_connectivity(self) -> AIConnectivityReport:
        pass


class IAILatencyVerifier(ABC):
    @abstractmethod
    def verify_latency(self) -> AILatencyReport:
        pass


class IAIQuotaVerifier(ABC):
    @abstractmethod
    def verify_quota(self) -> AIQuotaReport:
        pass


class IAIResponseIntegrityVerifier(ABC):
    @abstractmethod
    def verify_response_integrity(self) -> AIResponseIntegrityReport:
        pass


class IAITimeoutVerifier(ABC):
    @abstractmethod
    def verify_timeouts(self) -> AITimeoutReport:
        pass


class IAIFailureClassifier(ABC):
    @abstractmethod
    def classify_failures(self) -> AIFailureClassificationReport:
        pass


class IAIDegradedModeVerifier(ABC):
    @abstractmethod
    def verify_degraded_mode(self) -> AIDegradedModeReport:
        pass


class IAIFailoverVerifier(ABC):
    @abstractmethod
    def verify_failover(self) -> AIFailoverReport:
        pass


class IAIMonitoringBridge(ABC):
    @abstractmethod
    def verify_monitoring_integration(self) -> AIMonitoringReport:
        pass


class IAISecurityAuditor(ABC):
    @abstractmethod
    def audit_security(self) -> AISecurityReport:
        pass


class IAIFailureSimulator(ABC):
    @abstractmethod
    def run_simulations(self) -> AIFailureSimulationReport:
        pass


class IAIHealthScorer(ABC):
    @abstractmethod
    def compute_scorecard(
        self,
        health_report: AIProviderHealthReport,
        auth_report: AIAuthReport,
        connectivity_report: AIConnectivityReport,
        latency_report: AILatencyReport,
        quota_report: AIQuotaReport,
        integrity_report: AIResponseIntegrityReport,
        timeout_report: AITimeoutReport,
        failure_report: AIFailureClassificationReport,
        degraded_report: AIDegradedModeReport,
        failover_report: AIFailoverReport,
        monitoring_report: AIMonitoringReport,
        security_report: AISecurityReport,
        simulation_report: AIFailureSimulationReport,
    ) -> AIHealthQualityScorecard:
        pass
