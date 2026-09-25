"""
Phase 3M: Enterprise Cloud Readiness Verification — Domain Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any

from .models import (
    AutoScalingReport,
    CloudArchitectureAssessmentReport,
    CloudComputeResourceReport,
    CloudMigrationSimulationReport,
    CloudNetworkingReport,
    CloudObservabilityReport,
    CloudQueueWorkerReport,
    CloudSecretReport,
    CloudSecurityReport,
    CloudStorageReport,
    ContainerCloudCompatibilityReport,
    IaCVerificationReport,
    KubernetesReadinessReport,
    ManagedDatabaseReport,
    MultiCloudPortabilityReport,
)


class ICloudReadinessVerifier(ABC):
    @property
    @abstractmethod
    def verifier_id(self) -> str: pass

    @property
    def phase_id(self) -> str:
        parts = self.verifier_id.split("-")
        for part in parts:
            if part.startswith("3M.") or part.startswith("3m."):
                return part
        return self.verifier_id

    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def verify(self) -> Any: pass


class ICloudArchitectureAssessmentVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudArchitectureAssessmentReport: pass


class IContainerCloudCompatibilityVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> ContainerCloudCompatibilityReport: pass


class ICloudComputeResourceVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudComputeResourceReport: pass


class ICloudNetworkingVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudNetworkingReport: pass


class ICloudStorageCompatibilityVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudStorageReport: pass


class IManagedDatabaseReadinessVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> ManagedDatabaseReport: pass


class ICloudQueueWorkerScalabilityVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudQueueWorkerReport: pass


class IAutoScalingReadinessVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> AutoScalingReport: pass


class ICloudSecretManagementVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudSecretReport: pass


class ICloudObservabilityCompatibilityVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudObservabilityReport: pass


class IInfrastructureAsCodeVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> IaCVerificationReport: pass


class IKubernetesReadinessVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> KubernetesReadinessReport: pass


class ICloudSecurityVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudSecurityReport: pass


class IMultiCloudPortabilityVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> MultiCloudPortabilityReport: pass


class ICloudMigrationSimulationVerifier(ICloudReadinessVerifier):
    @abstractmethod
    def verify(self) -> CloudMigrationSimulationReport: pass
