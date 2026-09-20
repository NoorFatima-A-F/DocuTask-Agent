"""
Phase 3N: Enterprise Infrastructure Security Verification — Domain Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any

from .models import (
    AISecurityReport,
    APISecurityReport,
    BaseVerificationReport,
    CICDSecurityReport,
    ContainerSecurityReport,
    DatabaseSecurityReport,
    IAMSecurityReport,
    ImageSupplyChainReport,
    NetworkSecurityReport,
    SecretSecurityReport,
    SecurityArchitectureReport,
    SecurityAttackSimulationReport,
    SecurityMonitoringReport,
    ServiceSecurityReport,
    StorageSecurityReport,
    ThreatModelReport,
    VulnerabilityReport,
)


class IInfrastructureSecurityVerifier(ABC):
    @property
    @abstractmethod
    def verifier_id(self) -> str: pass

    @property
    def phase_id(self) -> str:
        parts = self.verifier_id.split("-")
        for part in parts:
            if part.startswith("3N.") or part.startswith("3n."):
                return part
        return self.verifier_id

    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def verify(self) -> Any: pass


class ISecurityArchitectureVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> SecurityArchitectureReport: pass


class IThreatModelingVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> ThreatModelReport: pass


class IContainerSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> ContainerSecurityReport: pass


class IImageSupplyChainSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> ImageSupplyChainReport: pass


class IVulnerabilityManagementVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> VulnerabilityReport: pass


class ISecretSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> SecretSecurityReport: pass


class IIAMSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> IAMSecurityReport: pass


class INetworkSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> NetworkSecurityReport: pass


class IServiceToServiceSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> ServiceSecurityReport: pass


class IAPIInfrastructureSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> APISecurityReport: pass


class IDatabaseSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> DatabaseSecurityReport: pass


class IStorageSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> StorageSecurityReport: pass


class IAIInfrastructureSecurityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> AISecurityReport: pass


class ICICDSecurityGateVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> CICDSecurityReport: pass


class ISecurityFailureSimulationVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> SecurityAttackSimulationReport: pass


class ISecurityObservabilityVerifier(IInfrastructureSecurityVerifier):
    @abstractmethod
    def verify(self) -> SecurityMonitoringReport: pass
