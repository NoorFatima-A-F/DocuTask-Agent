"""
Phase 3L: Enterprise Backup, Disaster Recovery & Business Continuity — Domain Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any

from .models import (
    BackupSecurityReport,
    BusinessImpactAnalysisReport,
    CompleteSystemRestoreReport,
    ConfigurationRecoveryReport,
    DatabaseRecoveryReport,
    DisasterRecoveryArchitectureReport,
    DRAutomationReport,
    DRFailureSimulationReport,
    PITRReport,
    RecoveryObjectivesReport,
    RecoveryObservabilityReport,
    SecretRecoveryReport,
    StorageRecoveryReport,
)


class IDisasterRecoveryVerifier(ABC):
    @property
    @abstractmethod
    def verifier_id(self) -> str: pass

    @property
    def phase_id(self) -> str:
        parts = self.verifier_id.split("-")
        for part in parts:
            if part.startswith("3L.") or part.startswith("3l."):
                return part
        return self.verifier_id

    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def verify(self) -> Any: pass


class IDisasterRecoveryArchitectureVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> DisasterRecoveryArchitectureReport: pass


class IBusinessImpactAnalysisVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> BusinessImpactAnalysisReport: pass


class IRecoveryObjectivesVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> RecoveryObjectivesReport: pass


class IDatabaseRecoveryVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> DatabaseRecoveryReport: pass


class IStorageRecoveryVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> StorageRecoveryReport: pass


class IConfigurationRecoveryVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> ConfigurationRecoveryReport: pass


class ISecretRecoveryVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> SecretRecoveryReport: pass


class ICompleteSystemRestoreVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> CompleteSystemRestoreReport: pass


class IPITRRecoveryVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> PITRReport: pass


class IBackupSecurityVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> BackupSecurityReport: pass


class IDRAutomationPipelineVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> DRAutomationReport: pass


class IDRFailureSimulationVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> DRFailureSimulationReport: pass


class IRecoveryObservabilityVerifier(IDisasterRecoveryVerifier):
    @abstractmethod
    def verify(self) -> RecoveryObservabilityReport: pass
