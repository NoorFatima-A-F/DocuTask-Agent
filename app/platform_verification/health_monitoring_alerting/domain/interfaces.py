"""Abstract interfaces for Phase 3H.4 Enterprise Health Monitoring & Alerting Framework."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    HealthSignalArchitectureReport,
    MetricsCollectionReport,
    PrometheusVerificationReport,
    DashboardValidationReport,
    AlertRuleReport,
    AlertAccuracyReport,
    IncidentSignalReport,
    AlertFatigueReport,
    MonitoringFailureTestReport,
    ObservabilitySecurityReport,
    HealthMonitoringScorecard,
)


class IHealthSignalArchitectureVerifier(ABC):
    """Interface for verifying health signals (3H.4.1)."""
    @abstractmethod
    def verify_signal_architecture(self) -> HealthSignalArchitectureReport:
        pass


class IOperationalMetricsVerifier(ABC):
    """Interface for verifying metrics collection (3H.4.2)."""
    @abstractmethod
    def verify_metrics_collection(self) -> MetricsCollectionReport:
        pass


class IPrometheusScrapingVerifier(ABC):
    """Interface for verifying Prometheus scraping (3H.4.3)."""
    @abstractmethod
    def verify_prometheus_scraping(self) -> PrometheusVerificationReport:
        pass


class IGrafanaDashboardVerifier(ABC):
    """Interface for verifying Grafana dashboards (3H.4.4)."""
    @abstractmethod
    def verify_dashboards(self) -> DashboardValidationReport:
        pass


class IAlertRuleVerifier(ABC):
    """Interface for verifying alert rules (3H.4.5)."""
    @abstractmethod
    def verify_alert_rules(self) -> AlertRuleReport:
        pass


class IAlertAccuracyVerifier(ABC):
    """Interface for verifying alert precision and recall (3H.4.6)."""
    @abstractmethod
    def verify_alert_accuracy(self) -> AlertAccuracyReport:
        pass


class IIncidentSignalVerifier(ABC):
    """Interface for verifying incident signal payloads (3H.4.7)."""
    @abstractmethod
    def verify_incident_signals(self) -> IncidentSignalReport:
        pass


class IAlertFatiguePreventionVerifier(ABC):
    """Interface for verifying deduplication and fatigue prevention (3H.4.8)."""
    @abstractmethod
    def verify_fatigue_prevention(self) -> AlertFatigueReport:
        pass


class IMonitoringFailureSimulator(ABC):
    """Interface for failure injection monitoring tests (3H.4.9)."""
    @abstractmethod
    def run_monitoring_failure_tests(self) -> MonitoringFailureTestReport:
        pass


class IObservabilitySecurityAuditor(ABC):
    """Interface for observability zero-leak security audit (3H.4.10)."""
    @abstractmethod
    def audit_security(self) -> ObservabilitySecurityReport:
        pass


class IHealthMonitoringScorer(ABC):
    """Interface for 6-dimension weighted scoring (3H.4.11)."""
    @abstractmethod
    def score_observability(
        self,
        signal_rep: HealthSignalArchitectureReport,
        metrics_rep: MetricsCollectionReport,
        prom_rep: PrometheusVerificationReport,
        dash_rep: DashboardValidationReport,
        alert_rep: AlertRuleReport,
        acc_rep: AlertAccuracyReport,
        inc_rep: IncidentSignalReport,
        fatigue_rep: AlertFatigueReport,
        sim_rep: MonitoringFailureTestReport,
        sec_rep: ObservabilitySecurityReport,
    ) -> HealthMonitoringScorecard:
        pass


class IHealthMonitoringEvidenceExporter(ABC):
    """Interface for exporting 10 JSON manifests to health_monitoring_verification/ (3H.4.12)."""
    @abstractmethod
    def export_all(
        self,
        signal_rep: HealthSignalArchitectureReport,
        metrics_rep: MetricsCollectionReport,
        prom_rep: PrometheusVerificationReport,
        dash_rep: DashboardValidationReport,
        alert_rep: AlertRuleReport,
        acc_rep: AlertAccuracyReport,
        inc_rep: IncidentSignalReport,
        fatigue_rep: AlertFatigueReport,
        sim_rep: MonitoringFailureTestReport,
        sec_rep: ObservabilitySecurityReport,
        scorecard: HealthMonitoringScorecard,
    ) -> Dict[str, str]:
        pass
