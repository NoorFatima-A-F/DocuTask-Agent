"""
Phase 3H.5.10: Domain Interfaces for Health Security Verification Framework
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    EndpointSecurityReport,
    HealthAuthorizationReport,
    MetricsPrivacyReport,
    LogSecurityReport,
    AlertSecurityReport,
    TraceSecurityReport,
    SecretScanReport,
    DashboardSecurityReport,
    SecurityFailureInjectionReport,
    ComplianceSecurityReport,
    HealthSecurityScorecard,
)


class IEndpointSecurityVerifier(ABC):
    @abstractmethod
    def verify_endpoint_security(self) -> EndpointSecurityReport:
        pass


class IHealthAuthorizationVerifier(ABC):
    @abstractmethod
    def verify_health_authorization(self) -> HealthAuthorizationReport:
        pass


class IMetricsPrivacyVerifier(ABC):
    @abstractmethod
    def verify_metrics_privacy(self) -> MetricsPrivacyReport:
        pass


class ILogSecurityVerifier(ABC):
    @abstractmethod
    def verify_log_security(self) -> LogSecurityReport:
        pass


class IAlertSecurityVerifier(ABC):
    @abstractmethod
    def verify_alert_security(self) -> AlertSecurityReport:
        pass


class ITraceSecurityVerifier(ABC):
    @abstractmethod
    def verify_trace_security(self) -> TraceSecurityReport:
        pass


class ISecretScanVerifier(ABC):
    @abstractmethod
    def scan_secrets_across_observability(self) -> SecretScanReport:
        pass


class IDashboardSecurityVerifier(ABC):
    @abstractmethod
    def verify_dashboard_security(self) -> DashboardSecurityReport:
        pass


class ISecurityFailureInjectionVerifier(ABC):
    @abstractmethod
    def execute_security_failure_injection(self) -> SecurityFailureInjectionReport:
        pass


class IComplianceSecurityVerifier(ABC):
    @abstractmethod
    def verify_compliance_and_standards(self) -> ComplianceSecurityReport:
        pass


class IHealthSecurityScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        endpoint_report: EndpointSecurityReport,
        auth_report: HealthAuthorizationReport,
        metrics_report: MetricsPrivacyReport,
        log_report: LogSecurityReport,
        alert_report: AlertSecurityReport,
        trace_report: TraceSecurityReport,
        secret_report: SecretScanReport,
        dashboard_report: DashboardSecurityReport,
        injection_report: SecurityFailureInjectionReport,
        compliance_report: ComplianceSecurityReport,
    ) -> HealthSecurityScorecard:
        pass
