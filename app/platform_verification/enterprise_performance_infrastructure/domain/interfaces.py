"""Phase 3J.6: Enterprise Performance Infrastructure Verification Framework — Domain Interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    APILatencyReport,
    CapacityBoundaryReport,
    DatabasePerformanceReport,
    DegradationAnalysisReport,
    E2EWorkflowReport,
    EnterprisePerformanceCertificationReport,
    MemoryStabilityReport,
    MonitoringIntegrationReport,
    PerformanceTestArchitectureReport,
    QueueCapacityReport,
    ResourceUtilizationReport,
    ThroughputScalingReport,
    WorkerEfficiencyReport,
    WorkloadModelReport,
)


class IPerformanceVerifier(ABC):
    """Base interface for all Phase 3J.6 performance infrastructure verifiers."""

    @property
    @abstractmethod
    def verifier_id(self) -> str:
        pass

    @property
    def phase_id(self) -> str:
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


class IPerformanceTestArchitectureVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceTestArchitectureReport:
        pass


class IWorkloadModelingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> WorkloadModelReport:
        pass


class IAPIPerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> APILatencyReport:
        pass


class IE2EWorkflowVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> E2EWorkflowReport:
        pass


class IThroughputScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ThroughputScalingReport:
        pass


class IDatabasePerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> DatabasePerformanceReport:
        pass


class IQueueCapacityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> QueueCapacityReport:
        pass


class IWorkerEfficiencyVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> WorkerEfficiencyReport:
        pass


class IResourceUtilizationVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ResourceUtilizationReport:
        pass


class IMemoryStabilityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> MemoryStabilityReport:
        pass


class IDegradationAnalysisVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> DegradationAnalysisReport:
        pass


class ICapacityBoundaryVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CapacityBoundaryReport:
        pass


class IMonitoringIntegrationVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> MonitoringIntegrationReport:
        pass


class IPerformanceInfrastructureScorer(ABC):
    """Calculates 5-category weighted performance quality score and certification tier."""

    @abstractmethod
    def score_reports(self, reports: Dict[str, Any]) -> EnterprisePerformanceCertificationReport:
        pass


class IPerformanceInfrastructureExporter(ABC):
    """Exports structured reports, dashboards, and SHA-256 metadata manifest."""

    @abstractmethod
    def export(
        self,
        reports: Dict[str, Any],
        certification: EnterprisePerformanceCertificationReport,
        output_dir: str,
    ) -> List[str]:
        pass


class IPerformanceInfrastructureRuntime(ABC):
    """Master orchestrator for enterprise performance infrastructure verification."""

    @abstractmethod
    def run_full_verification(self, output_dir: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_latest_certification(self) -> Optional[EnterprisePerformanceCertificationReport]:
        pass


# Aliases
IEnterprisePerformanceVerifier = IPerformanceVerifier
IEnterprisePerformanceScorer = IPerformanceInfrastructureScorer
IEnterprisePerformanceExporter = IPerformanceInfrastructureExporter
IEnterprisePerformanceRuntime = IPerformanceInfrastructureRuntime
