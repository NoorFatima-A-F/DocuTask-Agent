"""
Phase 3J.2: Performance Stress Verification — Domain Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    AIProviderStressReport,
    BaselineStressReport,
    CapacityBoundaryReport,
    CertificationReport,
    DatabasePerformanceReport,
    EnvironmentIsolationReport,
    MemoryStabilityReport,
    OverloadStressReport,
    ProgressiveLoadReport,
    RecoveryReport,
    RegressionReport,
)


class IPerformanceVerifier(ABC):
    """Base interface for all performance stress and capacity boundary verifiers."""

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
        """Executes the verification check and returns a structured report."""
        pass


class IPerformanceEnvironmentVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> EnvironmentIsolationReport:
        pass


class IBaselineStressVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> BaselineStressReport:
        pass


class IProgressiveLoadVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ProgressiveLoadReport:
        pass


class IOverloadStressVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> OverloadStressReport:
        pass


class ICapacityBoundaryVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CapacityBoundaryReport:
        pass


class IWorkerScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> WorkerScalingReport:
        pass


class IDatabaseStressVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> DatabasePerformanceReport:
        pass


class IAIProviderStressVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> AIProviderStressReport:
        pass


class IMemoryStabilityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> MemoryStabilityReport:
        pass


class IPerformanceRecoveryVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> RecoveryReport:
        pass


class IPerformanceRegressionGateVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> RegressionReport:
        pass


class IPerformanceScorer(ABC):
    """Calculates multi-dimensional performance scores and certification status."""

    @abstractmethod
    def score_reports(self, reports: Dict[str, Any]) -> CertificationReport:
        pass


class IPerformanceExporter(ABC):
    """Exports performance test results and metadata manifest."""

    @abstractmethod
    def export(
        self,
        reports: Dict[str, Any],
        certification: CertificationReport,
    ) -> List[str]:
        pass


class IPerformanceRuntime(ABC):
    """Master runtime orchestrator for performance verification."""

    @abstractmethod
    def run_full_verification(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_latest_certification(self) -> Optional[CertificationReport]:
        pass
