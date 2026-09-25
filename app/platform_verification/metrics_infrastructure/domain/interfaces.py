"""
Phase 3I.3: Enterprise Metrics Infrastructure Verification — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    MetricsArchitectureReport,
    MetricsStandardReport,
    ApplicationMetricsReport,
    AIMetricsReport,
    InfrastructureMetricsReport,
    BusinessSLAMetricsReport,
    DashboardReport,
    AlertValidationReport,
    MetricsAccuracyReport,
    MetricsSecurityReport,
    MetricsPerformanceReport,
    ChaosMetricReport,
    MetricsCertificationReport,
)


class IMetricsArchitectureVerifier(ABC):
    @abstractmethod
    def verify_metrics_architecture(self) -> MetricsArchitectureReport:
        pass


class IMetricsStandardVerifier(ABC):
    @abstractmethod
    def verify_metrics_standard(self) -> MetricsStandardReport:
        pass


class IApplicationMetricsVerifier(ABC):
    @abstractmethod
    def verify_application_metrics(self) -> ApplicationMetricsReport:
        pass


class IAIMetricsVerifier(ABC):
    @abstractmethod
    def verify_ai_metrics(self) -> AIMetricsReport:
        pass


class IInfrastructureMetricsVerifier(ABC):
    @abstractmethod
    def verify_infrastructure_metrics(self) -> InfrastructureMetricsReport:
        pass


class IBusinessSLAMetricsVerifier(ABC):
    @abstractmethod
    def verify_business_sla_metrics(self) -> BusinessSLAMetricsReport:
        pass


class IMetricsDashboardVerifier(ABC):
    @abstractmethod
    def verify_dashboards(self) -> DashboardReport:
        pass


class IAlertMetricVerifier(ABC):
    @abstractmethod
    def verify_alert_metrics(self) -> AlertValidationReport:
        pass


class IMetricsAccuracyVerifier(ABC):
    @abstractmethod
    def verify_metrics_accuracy(self) -> MetricsAccuracyReport:
        pass


class IMetricsSecurityVerifier(ABC):
    @abstractmethod
    def verify_metrics_security(self) -> MetricsSecurityReport:
        pass


class IMetricsPerformanceVerifier(ABC):
    @abstractmethod
    def verify_metrics_performance(self) -> MetricsPerformanceReport:
        pass


class IFailureSimulationMetricsVerifier(ABC):
    @abstractmethod
    def verify_failure_simulation_metrics(self) -> ChaosMetricReport:
        pass


class IMetricsQualityScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        arch_report: MetricsArchitectureReport,
        std_report: MetricsStandardReport,
        app_report: ApplicationMetricsReport,
        ai_report: AIMetricsReport,
        infra_report: InfrastructureMetricsReport,
        biz_report: BusinessSLAMetricsReport,
        dash_report: DashboardReport,
        alert_report: AlertValidationReport,
        acc_report: MetricsAccuracyReport,
        sec_report: MetricsSecurityReport,
        perf_report: MetricsPerformanceReport,
        chaos_report: ChaosMetricReport,
    ) -> MetricsCertificationReport:
        pass


class IMetricsEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: MetricsArchitectureReport,
        std_report: MetricsStandardReport,
        app_report: ApplicationMetricsReport,
        ai_report: AIMetricsReport,
        infra_report: InfrastructureMetricsReport,
        biz_report: BusinessSLAMetricsReport,
        dash_report: DashboardReport,
        alert_report: AlertValidationReport,
        acc_report: MetricsAccuracyReport,
        sec_report: MetricsSecurityReport,
        perf_report: MetricsPerformanceReport,
        chaos_report: ChaosMetricReport,
        certification_report: MetricsCertificationReport,
    ) -> Dict[str, Any]:
        pass
