"""Domain Interfaces for Health Monitoring Integration."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from app.platform_verification.health_monitoring_integration.domain.models import (
    AlertConfigurationReport,
    AlertQualityReport,
    FailureSimulationReport,
    GrafanaDashboardReport,
    HealthMetricsInventoryReport,
    IncidentVisibilityReport,
    MonitoringQualityScorecard,
    MonitoringSecurityReport,
    ObservabilityArchitectureReport,
    PrometheusVerificationReport,
    TracingVerificationReport,
)


class IObservabilityArchVerifier(ABC):
    @abstractmethod
    def verify_architecture(self) -> ObservabilityArchitectureReport:
        pass


class IHealthMetricsCollector(ABC):
    @abstractmethod
    def collect_inventory(self) -> HealthMetricsInventoryReport:
        pass


class IPrometheusVerifier(ABC):
    @abstractmethod
    def verify_prometheus(self) -> PrometheusVerificationReport:
        pass


class IGrafanaDashboardBuilder(ABC):
    @abstractmethod
    def verify_dashboards(self) -> GrafanaDashboardReport:
        pass


class IAlertRuleManager(ABC):
    @abstractmethod
    def get_alert_configuration(self) -> AlertConfigurationReport:
        pass


class IAlertQualityEvaluator(ABC):
    @abstractmethod
    def evaluate_quality(self) -> AlertQualityReport:
        pass


class IIncidentVisibilityEngine(ABC):
    @abstractmethod
    def verify_incident_visibility(self, document_id: str) -> IncidentVisibilityReport:
        pass


class IMonitoringSimulationRunner(ABC):
    @abstractmethod
    def run_simulations(self) -> FailureSimulationReport:
        pass


class IDistributedTraceVerifier(ABC):
    @abstractmethod
    def verify_tracing(self) -> TracingVerificationReport:
        pass


class IMonitoringSecurityAuditor(ABC):
    @abstractmethod
    def audit_security(self) -> MonitoringSecurityReport:
        pass


class IMonitoringQualityScorer(ABC):
    @abstractmethod
    def compute_scorecard(
        self,
        arch_report: ObservabilityArchitectureReport,
        metrics_report: HealthMetricsInventoryReport,
        prom_report: PrometheusVerificationReport,
        grafana_report: GrafanaDashboardReport,
        alert_config_report: AlertConfigurationReport,
        alert_quality_report: AlertQualityReport,
        incident_report: IncidentVisibilityReport,
        simulation_report: FailureSimulationReport,
        tracing_report: TracingVerificationReport,
        security_report: MonitoringSecurityReport,
    ) -> MonitoringQualityScorecard:
        pass
