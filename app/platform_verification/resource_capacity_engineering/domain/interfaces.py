"""
Phase 3J.4: Resource Utilization & Capacity Engineering Verification Framework — Domain Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    AIResourceProfileReport,
    AutoscalingReadinessReport,
    CPUCapacityReport,
    CapacityModelReport,
    ContainerResourcePolicyReport,
    DatabaseCapacityReport,
    MemoryLeakReport,
    QueueCapacityReport,
    ResourceAlertReport,
    ResourceCapacityCertificationReport,
    ResourceProfileReport,
    WorkerCapacityReport,
)


class IResourceCollector(ABC):
    """Base interface for all granular resource telemetry collectors."""

    @property
    @abstractmethod
    def collector_name(self) -> str:
        pass

    @abstractmethod
    def collect(self) -> Dict[str, Any]:
        pass


class IResourceVerifier(ABC):
    """Base interface for all resource and capacity engineering verifiers."""

    @property
    @abstractmethod
    def verifier_id(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def verify(self) -> Any:
        pass


class IResourceProfilingVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> ResourceProfileReport:
        pass


class IContainerResourcePolicyVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> ContainerResourcePolicyReport:
        pass


class ICPUCapacityVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> CPUCapacityReport:
        pass


class IMemoryLeakVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> MemoryLeakReport:
        pass


class IWorkerCapacityVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> WorkerCapacityReport:
        pass


class IQueueCapacityVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> QueueCapacityReport:
        pass


class IDatabaseCapacityVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> DatabaseCapacityReport:
        pass


class IAIResourceProfileVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> AIResourceProfileReport:
        pass


class ICapacityModelingVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> CapacityModelReport:
        pass


class IAutoscalingReadinessVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> AutoscalingReadinessReport:
        pass


class IResourceAlertingVerifier(IResourceVerifier):
    @abstractmethod
    def verify(self) -> ResourceAlertReport:
        pass


class IResourceScorer(ABC):
    """Calculates 6-category resource quality score and certification tier."""

    @abstractmethod
    def score_reports(self, reports: Dict[str, Any]) -> ResourceCapacityCertificationReport:
        pass


class IResourceExporter(ABC):
    """Exports structured reports and SHA-256 metadata manifest."""

    @abstractmethod
    def export(
        self,
        reports: Dict[str, Any],
        certification: ResourceCapacityCertificationReport,
    ) -> List[str]:
        pass


class IResourceRuntime(ABC):
    """Master orchestrator for resource utilization and capacity verification."""

    @abstractmethod
    def run_full_verification(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_latest_certification(self) -> Optional[ResourceCapacityCertificationReport]:
        pass
