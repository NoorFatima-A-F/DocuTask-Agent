"""
Part 3I: Enterprise Observability Infrastructure — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    LoggingArchitectureReport,
    StructuredLoggingReport,
    CorrelationReport,
    AIWorkflowLoggingReport,
    SecurityScanReport,
    RetentionReport,
    LogPerformanceReport,
    LoggingCertificationReport,
    MetricInventoryReport,
    GoldenSignalsReport,
    AppInfraMetricsReport,
    SLISLOReport,
    AlertingReport,
    DashboardReport,
    MetricsPerformanceReport,
    MetricsCertificationReport,
    UnifiedObservabilityCertification,
)


# ─── 3I.1 Logging Interfaces ──────────────────────────────────────────────

class ILoggingArchitectureVerifier(ABC):
    @abstractmethod
    def verify_logging_architecture(self) -> LoggingArchitectureReport:
        pass


class IStructuredLoggingVerifier(ABC):
    @abstractmethod
    def verify_structured_logging(self) -> StructuredLoggingReport:
        pass


class ICorrelationVerifier(ABC):
    @abstractmethod
    def verify_correlation(self) -> CorrelationReport:
        pass


class IAIWorkflowLoggingVerifier(ABC):
    @abstractmethod
    def verify_ai_workflow_logging(self) -> AIWorkflowLoggingReport:
        pass


class ISecurityScanVerifier(ABC):
    @abstractmethod
    def verify_security_scanning(self) -> SecurityScanReport:
        pass


class ILogRetentionVerifier(ABC):
    @abstractmethod
    def verify_retention(self) -> RetentionReport:
        pass


class ILogPerformanceVerifier(ABC):
    @abstractmethod
    def verify_log_performance(self) -> LogPerformanceReport:
        pass


class ILoggingScorer(ABC):
    @abstractmethod
    def calculate_logging_score(
        self,
        arch_report: LoggingArchitectureReport,
        struct_report: StructuredLoggingReport,
        corr_report: CorrelationReport,
        ai_report: AIWorkflowLoggingReport,
        sec_report: SecurityScanReport,
        ret_report: RetentionReport,
        perf_report: LogPerformanceReport,
    ) -> LoggingCertificationReport:
        pass


# ─── 3I.2 Metrics Interfaces ──────────────────────────────────────────────

class IMetricsArchitectureVerifier(ABC):
    @abstractmethod
    def verify_metrics_architecture(self) -> MetricInventoryReport:
        pass


class IGoldenSignalsVerifier(ABC):
    @abstractmethod
    def verify_golden_signals(self) -> GoldenSignalsReport:
        pass


class IAppInfraMetricsVerifier(ABC):
    @abstractmethod
    def verify_app_infra_metrics(self) -> AppInfraMetricsReport:
        pass


class ISLISLOVerifier(ABC):
    @abstractmethod
    def verify_sli_slo(self) -> SLISLOReport:
        pass


class IAlertingVerifier(ABC):
    @abstractmethod
    def verify_alerting(self) -> AlertingReport:
        pass


class IDashboardVerifier(ABC):
    @abstractmethod
    def verify_dashboards(self) -> DashboardReport:
        pass


class IMetricsPerformanceVerifier(ABC):
    @abstractmethod
    def verify_metrics_performance(self) -> MetricsPerformanceReport:
        pass


class IMetricsScorer(ABC):
    @abstractmethod
    def calculate_metrics_score(
        self,
        inventory_report: MetricInventoryReport,
        golden_report: GoldenSignalsReport,
        app_infra_report: AppInfraMetricsReport,
        sli_report: SLISLOReport,
        alert_report: AlertingReport,
        dash_report: DashboardReport,
        perf_report: MetricsPerformanceReport,
    ) -> MetricsCertificationReport:
        pass


# ─── Composite Exporter Interface ─────────────────────────────────────────

class IObservabilityExporter(ABC):
    @abstractmethod
    def export_all_observability_reports(
        self,
        base_dir: str,
        logging_reports: Dict[str, Any],
        logging_cert: LoggingCertificationReport,
        metrics_reports: Dict[str, Any],
        metrics_cert: MetricsCertificationReport,
        unified_cert: UnifiedObservabilityCertification,
    ) -> Dict[str, Any]:
        pass
