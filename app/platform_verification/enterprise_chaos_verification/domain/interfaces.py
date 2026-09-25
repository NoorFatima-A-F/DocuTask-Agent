"""
Phase 3K: Enterprise Chaos Engineering Verification — Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any

from .models import (
    AIProviderFailureReport,
    CascadingFailureReport,
    ChaosObservabilityReport,
    ChaosPipelineReport,
    ChaosReadinessReport,
    ChaosReportGenerationReport,
    ContainerFailureReport,
    DatabaseFailureReport,
    NetworkFailureReport,
    QueueFailureReport,
    ResourceExhaustionReport,
    WorkerAgentFailureReport,
)


class IChaosVerifier(ABC):
    @property
    @abstractmethod
    def verifier_id(self) -> str: pass

    @property
    def phase_id(self) -> str:
        parts = self.verifier_id.split("-")
        for part in parts:
            if part.startswith("3K.") or part.startswith("3k."):
                return part
        return self.verifier_id

    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def verify(self) -> Any: pass


class IChaosReadinessVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> ChaosReadinessReport: pass


class IContainerFailureVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> ContainerFailureReport: pass


class IDatabaseFailureVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> DatabaseFailureReport: pass


class IQueueFailureVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> QueueFailureReport: pass


class INetworkFailureVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> NetworkFailureReport: pass


class IAIProviderFailureVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> AIProviderFailureReport: pass


class IResourceExhaustionVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> ResourceExhaustionReport: pass


class IWorkerAgentFailureVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> WorkerAgentFailureReport: pass


class ICascadingFailureVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> CascadingFailureReport: pass


class IChaosAutomationPipelineVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> ChaosPipelineReport: pass


class IChaosObservabilityVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> ChaosObservabilityReport: pass


class IChaosReportGenerationVerifier(IChaosVerifier):
    @abstractmethod
    def verify(self) -> ChaosReportGenerationReport: pass
