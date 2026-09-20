"""
Phase 3J.5: Enterprise Performance Baseline & Capacity Verification Framework — Domain Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    AIWorkloadReport,
    BottleneckAnalysisReport,
    CapacityPlanReport,
    ControlledLoadTestReport,
    DatabasePerformanceReport,
    EnduranceTestReport,
    EnterprisePerformanceCertificationReport,
    LatencyBreakdownReport,
    PerformanceBaselineReport,
    PerformanceRegressionReport,
    QueuePerformanceReport,
    ResourceUtilizationReport,
    SpikeTestReport,
    StoragePerformanceReport,
    StressTestReport,
    ThroughputCapacityReport,
)


class IPerformanceVerifier(ABC):
    """Base interface for all Phase 3J.5 performance and capacity verifiers."""

    @property
    @abstractmethod
    def verifier_id(self) -> str:
        pass

    @property
    def phase_id(self) -> str:
        # Extract phase ID e.g. "3J.5.1" from "VERIFY-3J.5.1-PERF-BASELINE"
        parts = self.verifier_id.split("-")
        for part in parts:
            if part.startswith("3J.") or part.startswith("3j."):
                return part
        return self.verifier_id

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def verify(self) -> Any:
        pass



class IPerformanceBaselineVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceBaselineReport:
        pass


class ILatencyBreakdownVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> LatencyBreakdownReport:
        pass


class IThroughputCapacityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ThroughputCapacityReport:
        pass


class ILoadTestingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ControlledLoadTestReport:
        pass


class IStressTestingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> StressTestReport:
        pass


class ISpikeTestingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> SpikeTestReport:
        pass


class IEnduranceTestingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> EnduranceTestReport:
        pass


class IAIWorkloadVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> AIWorkloadReport:
        pass


class IQueuePerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> QueuePerformanceReport:
        pass


class IDatabasePerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> DatabasePerformanceReport:
        pass


class IStoragePerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> StoragePerformanceReport:
        pass


class IResourceUtilizationVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ResourceUtilizationReport:
        pass


class IBottleneckAnalysisVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> BottleneckAnalysisReport:
        pass


class ICapacityPlanningVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CapacityPlanReport:
        pass


class IPerformanceRegressionVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceRegressionReport:
        pass


class IPerformanceScorer(ABC):
    """Calculates 6-category weighted performance quality score and certification tier."""

    @abstractmethod
    def score_reports(self, reports: Dict[str, Any]) -> EnterprisePerformanceCertificationReport:
        pass


class IPerformanceExporter(ABC):
    """Exports structured reports and SHA-256 metadata manifest."""

    @abstractmethod
    def export(
        self,
        reports: Dict[str, Any],
        certification: EnterprisePerformanceCertificationReport,
    ) -> List[str]:
        pass


class IPerformanceRuntime(ABC):
    """Master orchestrator for enterprise performance verification."""

    @abstractmethod
    def run_full_verification(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_latest_certification(self) -> Optional[EnterprisePerformanceCertificationReport]:
        pass


# Backward & enterprise naming aliases
IEnterprisePerformanceVerifier = IPerformanceVerifier
IEnterprisePerformanceScorer = IPerformanceScorer
IEnterprisePerformanceExporter = IPerformanceExporter
IEnterprisePerformanceRuntime = IPerformanceRuntime

