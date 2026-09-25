"""Phase 3J.9: Enterprise AI Performance Bottleneck Interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    AIModelPerformanceReport,
    CapacityPlanReport,
    DatabasePerformanceReport,
    EnterpriseAIPerformanceCertificationReport,
    LatencyBreakdownReport,
    PerformanceArchitectureReport,
    PerformanceFailureReport,
    PerformanceObservabilityReport,
    PerformanceRegressionReport,
    QueueCapacityReport,
    ResourceBottleneckReport,
    ThroughputCapacityReport,
    WorkerScalingReport,
)


class IPerformanceVerifier(ABC):
    @property
    @abstractmethod
    def verifier_id(self) -> str: pass

    @property
    def phase_id(self) -> str:
        parts = self.verifier_id.split("-")
        for part in parts:
            if part.startswith("3J.") or part.startswith("3j."):
                return part
        return self.verifier_id

    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def verify(self) -> Any: pass


class IPerformanceArchitectureVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceArchitectureReport: pass


class ILatencyBreakdownVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> LatencyBreakdownReport: pass


class IThroughputCapacityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ThroughputCapacityReport: pass


class IResourceBottleneckVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ResourceBottleneckReport: pass


class IDatabasePerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> DatabasePerformanceReport: pass


class IQueueCapacityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> QueueCapacityReport: pass


class IWorkerScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> WorkerScalingReport: pass


class IAIModelPerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> AIModelPerformanceReport: pass


class IPerformanceRegressionVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceRegressionReport: pass


class ICapacityPlanningVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CapacityPlanReport: pass


class IPerformanceFailureVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceFailureReport: pass


class IPerformanceObservabilityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceObservabilityReport: pass


class IAIPerformanceScorer(ABC):
    @abstractmethod
    def score_reports(self, reports: Dict[str, Any]) -> EnterpriseAIPerformanceCertificationReport: pass


class IAIPerformanceExporter(ABC):
    @abstractmethod
    def export(self, reports: Dict[str, Any], certification: EnterpriseAIPerformanceCertificationReport, output_dir: str) -> List[str]: pass


class IAIPerformanceRuntime(ABC):
    @abstractmethod
    def run_full_verification(self, output_dir: str) -> Dict[str, Any]: pass

    @abstractmethod
    def get_latest_certification(self) -> Optional[EnterpriseAIPerformanceCertificationReport]: pass
