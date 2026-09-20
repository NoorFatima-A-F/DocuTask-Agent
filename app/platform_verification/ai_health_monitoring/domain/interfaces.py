"""Domain interfaces for AI Health Monitoring Integration."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.platform_verification.ai_health_monitoring.domain.models import (
    AIAlertingReport,
    AIAutomatedResponseReport,
    AIDashboardReport,
    AIIncidentTestReport,
    AILoggingReport,
    AIMetricsReport,
    AIMonitoringSecurityReport,
    AIObservabilityArchitectureReport,
    AIObservabilityScorecard,
    AISLOReport,
    AITracingReport,
)


class IAIObservabilityArchitectureVerifier(ABC):
    @abstractmethod
    def verify_architecture(self) -> AIObservabilityArchitectureReport:
        pass


class IAIMetricsCollectorVerifier(ABC):
    @abstractmethod
    def verify_metrics_collection(self) -> AIMetricsReport:
        pass


class IAIDashboardVerifier(ABC):
    @abstractmethod
    def verify_dashboards(self) -> AIDashboardReport:
        pass


class IAILoggingVerifier(ABC):
    @abstractmethod
    def verify_logging(self) -> AILoggingReport:
        pass


class IAITracingVerifier(ABC):
    @abstractmethod
    def verify_tracing(self) -> AITracingReport:
        pass


class IAIAlertingVerifier(ABC):
    @abstractmethod
    def verify_alerting(self) -> AIAlertingReport:
        pass


class IAISLOMonitoringVerifier(ABC):
    @abstractmethod
    def verify_slos(self) -> AISLOReport:
        pass


class IAIIncidentDetectorVerifier(ABC):
    @abstractmethod
    def verify_incident_detection(self) -> AIIncidentTestReport:
        pass


class IAIAutomatedResponseVerifier(ABC):
    @abstractmethod
    def verify_automated_response(self) -> AIAutomatedResponseReport:
        pass


class IAIMonitoringSecurityVerifier(ABC):
    @abstractmethod
    def verify_security(self) -> AIMonitoringSecurityReport:
        pass


class IAIObservabilityQualityScorer(ABC):
    @abstractmethod
    def compute_scorecard(
        self,
        arch_report: AIObservabilityArchitectureReport,
        metrics_report: AIMetricsReport,
        dashboard_report: AIDashboardReport,
        logging_report: AILoggingReport,
        tracing_report: AITracingReport,
        alerting_report: AIAlertingReport,
        slo_report: AISLOReport,
        incident_report: AIIncidentTestReport,
        automation_report: AIAutomatedResponseReport,
        security_report: AIMonitoringSecurityReport,
    ) -> AIObservabilityScorecard:
        pass
