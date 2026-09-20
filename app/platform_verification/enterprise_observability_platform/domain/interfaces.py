"""
Phase 3I.11: Enterprise Observability Intelligence Platform Integration — Domain Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from app.platform_verification.enterprise_observability_platform.domain.models import (
    ControlPlaneArchitectureReport,
    TelemetryFederationReport,
    ObservabilityStandardizationReport,
    EnvironmentDriftReport,
    GlobalReliabilityReport,
    CrossEnvironmentIncidentReport,
    ProductionReadinessGateReport,
    MultiRegionReliabilityReport,
    CloudObservabilityIntegrationReport,
    DashboardFederationReport,
    GlobalAutomationControlReport,
    GlobalOperationsCertificationReport,
)


class IControlPlaneVerifier(ABC):
    @abstractmethod
    def verify(self) -> ControlPlaneArchitectureReport:
        """Verify centralized control plane architecture and environment separation."""
        pass


class ITelemetryFederationVerifier(ABC):
    @abstractmethod
    def verify(self) -> TelemetryFederationReport:
        """Verify telemetry aggregation across Dev, Test, Staging, Prod, and DR."""
        pass


class IObservabilityStandardizationVerifier(ABC):
    @abstractmethod
    def verify(self) -> ObservabilityStandardizationReport:
        """Verify standardization of metrics, logs, and distributed tracing across environments."""
        pass


class IDriftDetectionVerifier(ABC):
    @abstractmethod
    def verify(self) -> EnvironmentDriftReport:
        """Verify detection of infrastructure, configuration, and observability drift."""
        pass


class IGlobalReliabilityVerifier(ABC):
    @abstractmethod
    def verify(self) -> GlobalReliabilityReport:
        """Calculate global platform reliability score, risk level, and health trends."""
        pass


class ICrossEnvironmentIncidentVerifier(ABC):
    @abstractmethod
    def verify(self) -> CrossEnvironmentIncidentReport:
        """Verify cross-environment incident learning and preventative deployment blocking."""
        pass


class IProductionReadinessVerifier(ABC):
    @abstractmethod
    def verify(self) -> ProductionReadinessGateReport:
        """Verify multi-stage pre-production release readiness approval gates."""
        pass


class IMultiRegionVerifier(ABC):
    @abstractmethod
    def verify(self) -> MultiRegionReliabilityReport:
        """Verify multi-region health, latency comparison, and automated failover."""
        pass


class ICloudIntegrationVerifier(ABC):
    @abstractmethod
    def verify(self) -> CloudObservabilityIntegrationReport:
        """Verify unified observability integration across AWS, GCP, Azure, and Kubernetes."""
        pass


class IDashboardFederationVerifier(ABC):
    @abstractmethod
    def verify(self) -> DashboardFederationReport:
        """Verify federated Executive, SRE, AI Ops, and Infrastructure dashboard views."""
        pass


class IAutomationControlVerifier(ABC):
    @abstractmethod
    def verify(self) -> GlobalAutomationControlReport:
        """Verify controlled global actions including scaling, deployment protection, and recovery."""
        pass


class IGlobalOperationsScorer(ABC):
    @abstractmethod
    def compute_certification(self, verification_results: Dict[str, Any]) -> GlobalOperationsCertificationReport:
        """Compute the 7-category weighted score and generate the certification report."""
        pass


class IEnterpriseObservabilityExporter(ABC):
    @abstractmethod
    def export(self, verification_results: Dict[str, Any], certification_report: GlobalOperationsCertificationReport) -> Dict[str, str]:
        """Export all verification manifests and signed metadata.json."""
        pass
