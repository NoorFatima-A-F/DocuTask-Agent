"""Abstract interfaces for Grafana Dashboard Verification sub-engines."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    ConfigurationReport,
    ProvisioningReport,
    DashboardValidationReport,
    UsabilityAuditReport,
    PerformanceBenchmarkReport,
    SecurityAuditReport,
    OperationalDashboardScorecard,
)


class IGrafanaConfigurationVerifier(ABC):
    """Interface for verifying Grafana configuration and deployment (3H.4.4.1)."""

    @abstractmethod
    def verify_configuration(self) -> ConfigurationReport:
        pass


class IDashboardProvisioningVerifier(ABC):
    """Interface for verifying IaC dashboard provisioning (3H.4.4.2)."""

    @abstractmethod
    def verify_provisioning(self) -> ProvisioningReport:
        pass


class IDashboardSpecVerifier(ABC):
    """Interface for validating specific operational dashboards (3H.4.4.3 - 3H.4.4.7)."""

    @abstractmethod
    def verify_dashboard(self) -> DashboardValidationReport:
        pass


class IDashboardUsabilityVerifier(ABC):
    """Interface for benchmarking dashboard usability scenarios (3H.4.4.8)."""

    @abstractmethod
    def verify_usability(self) -> UsabilityAuditReport:
        pass


class IDashboardPerformanceVerifier(ABC):
    """Interface for testing load times and query latency (3H.4.4.9)."""

    @abstractmethod
    def verify_performance(self) -> PerformanceBenchmarkReport:
        pass


class IDashboardSecurityAuditor(ABC):
    """Interface for auditing dashboard authentication, RBAC, and zero leaks (3H.4.4.10)."""

    @abstractmethod
    def audit_security(self) -> SecurityAuditReport:
        pass


class IOperationalDashboardScorer(ABC):
    """Interface for 7-category weighted quality scoring (3H.4.4.11)."""

    @abstractmethod
    def score_dashboards(
        self,
        config_rep: ConfigurationReport,
        prov_rep: ProvisioningReport,
        system_rep: DashboardValidationReport,
        ai_rep: DashboardValidationReport,
        agent_rep: DashboardValidationReport,
        infra_rep: DashboardValidationReport,
        incident_rep: DashboardValidationReport,
        usability_rep: UsabilityAuditReport,
        perf_rep: PerformanceBenchmarkReport,
        sec_rep: SecurityAuditReport,
    ) -> OperationalDashboardScorecard:
        pass


class IGrafanaEvidenceExporter(ABC):
    """Interface for exporting structured audit manifests (3H.4.4.12)."""

    @abstractmethod
    def export_all(
        self,
        config_rep: ConfigurationReport,
        prov_rep: ProvisioningReport,
        system_rep: DashboardValidationReport,
        ai_rep: DashboardValidationReport,
        agent_rep: DashboardValidationReport,
        infra_rep: DashboardValidationReport,
        incident_rep: DashboardValidationReport,
        usability_rep: UsabilityAuditReport,
        perf_rep: PerformanceBenchmarkReport,
        sec_rep: SecurityAuditReport,
        scorecard: OperationalDashboardScorecard,
    ) -> Dict[str, str]:
        pass
