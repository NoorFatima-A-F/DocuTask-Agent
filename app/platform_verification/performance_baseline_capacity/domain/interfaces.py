"""
Phase 3J.3: Enterprise Performance Baseline & Capacity Verification Framework — Domain Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    AIPipelinePerformanceReport,
    BaselinePerformanceReport,
    CapacityModelReport,
    ConcurrentLoadReport,
    DatabasePerformanceReport,
    LatencyDistributionReport,
    PerformanceArchitectureReport,
    PerformanceFailureReport,
    PerformanceQualityCertificationReport,
    PerformanceRegressionReport,
    QueueCapacityReport,
    ResourceUtilizationReport,
    WorkerScalingReport,
)


class IPerformanceVerifier(ABC):
    """Base interface for all performance baseline and capacity verifiers."""

    @property
    @abstractmethod
    def verifier_id(self) -> str:
        """Unique identifier for the verifier."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the verifier."""
        pass

    @abstractmethod
    def verify(self) -> Any:
        """Executes verification check and returns a structured report."""
        pass


class IPerformanceArchitectureVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceArchitectureReport:
        pass


class IBaselinePerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> BaselinePerformanceReport:
        pass


class IAIPipelinePerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> AIPipelinePerformanceReport:
        pass


class IConcurrentLoadVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ConcurrentLoadReport:
        pass


class ICapacityModelVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CapacityModelReport:
        pass


class ILatencyDistributionVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> LatencyDistributionReport:
        pass


class IResourceUtilizationVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ResourceUtilizationReport:
        pass


class IDatabasePerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> DatabasePerformanceReport:
        pass


class IQueueCapacityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> QueueCapacityReport:
        pass


class IWorkerScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> WorkerScalingReport:
        pass


class IPerformanceFailureVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceFailureReport:
        pass


class IPerformanceRegressionVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceRegressionReport:
        pass


class IPerformanceScorer(ABC):
    """Calculates 6-category weighted performance quality score and certification tier."""

    @abstractmethod
    def score_reports(self, reports: Dict[str, Any]) -> PerformanceQualityCertificationReport:
        pass


class IPerformanceExporter(ABC):
    """Exports structured performance reports and metadata manifest."""

    @abstractmethod
    def export(
        self,
        reports: Dict[str, Any],
        certification: PerformanceQualityCertificationReport,
    ) -> List[str]:
        pass


class IPerformanceRuntime(ABC):
    """Master orchestrator for the performance baseline and capacity verification subsystem."""

    @abstractmethod
    def run_full_verification(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_latest_certification(self) -> Optional[PerformanceQualityCertificationReport]:
        pass
