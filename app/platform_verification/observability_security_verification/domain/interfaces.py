"""
Phase 3H.4.10: Enterprise Observability Security - Abstract Interfaces
"""
from abc import ABC, abstractmethod
from typing import List
from .models import (
    DataClassificationReport,
    LogSecurityReport,
    LogSanitizationReport,
    MetricSecurityReport,
    TraceSecurityReport,
    DashboardAccessReport,
    AlertSecurityReport,
    PipelineSecurityReport,
    AISecurityReport,
    SecurityFailureSimulationResult,
    ObservabilitySecurityScorecard,
)


class IDataClassificationVerifier(ABC):
    @abstractmethod
    def verify_data_classification(self) -> DataClassificationReport:
        pass


class ILogSecurityVerifier(ABC):
    @abstractmethod
    def scan_logs_for_sensitive_data(self) -> LogSecurityReport:
        pass


class ILogSanitizationVerifier(ABC):
    @abstractmethod
    def verify_sanitization_middleware(self) -> LogSanitizationReport:
        pass


class IMetricSecurityVerifier(ABC):
    @abstractmethod
    def audit_metrics_privacy(self) -> MetricSecurityReport:
        pass


class ITraceSecurityVerifier(ABC):
    @abstractmethod
    def audit_trace_security(self) -> TraceSecurityReport:
        pass


class IDashboardAccessVerifier(ABC):
    @abstractmethod
    def verify_dashboard_rbac(self) -> DashboardAccessReport:
        pass


class IAlertSecurityVerifier(ABC):
    @abstractmethod
    def audit_alert_payloads(self) -> AlertSecurityReport:
        pass


class IPipelineSecurityVerifier(ABC):
    @abstractmethod
    def verify_pipeline_and_storage_security(self) -> PipelineSecurityReport:
        pass


class IAISecurityVerifier(ABC):
    @abstractmethod
    def audit_ai_telemetry_security(self) -> AISecurityReport:
        pass


class ISecurityFailureSimulator(ABC):
    @abstractmethod
    def simulate_security_failure_injections(self) -> List[SecurityFailureSimulationResult]:
        pass


class IObservabilitySecurityScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        classification_report: DataClassificationReport,
        log_report: LogSecurityReport,
        metric_report: MetricSecurityReport,
        trace_report: TraceSecurityReport,
        access_report: DashboardAccessReport,
        pipeline_report: PipelineSecurityReport,
        ai_report: AISecurityReport,
    ) -> ObservabilitySecurityScorecard:
        pass


class IObservabilitySecurityExporter(ABC):
    @abstractmethod
    def export_evidence_manifests(
        self,
        output_dir: str,
        classification_report: DataClassificationReport,
        log_report: LogSecurityReport,
        sanitization_report: LogSanitizationReport,
        metric_report: MetricSecurityReport,
        trace_report: TraceSecurityReport,
        access_report: DashboardAccessReport,
        alert_report: AlertSecurityReport,
        pipeline_report: PipelineSecurityReport,
        ai_report: AISecurityReport,
        simulations: List[SecurityFailureSimulationResult],
        scorecard: ObservabilitySecurityScorecard,
    ) -> List[str]:
        pass
