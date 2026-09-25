"""Phase 3J.7: Enterprise Performance Bottleneck Discovery — Domain Interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    AIProviderPerformanceReport,
    ApplicationBottleneckReport,
    CapacityBoundaryReport,
    DatabaseBottleneckReport,
    EnterpriseBottleneckCertificationReport,
    OptimizationRecommendationsReport,
    PerformanceArchitectureReport,
    PerformanceRegressionReport,
    QueueBottleneckReport,
    ResourceSaturationReport,
    WorkerCapacityReport,
)


class IPerformanceVerifier(ABC):
    """Base interface for all Phase 3J.7 bottleneck discovery verifiers."""

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


class IPerformanceArchitectureVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceArchitectureReport:
        pass


class IResourceSaturationVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ResourceSaturationReport:
        pass


class IApplicationBottleneckVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ApplicationBottleneckReport:
        pass


class IDatabaseBottleneckVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> DatabaseBottleneckReport:
        pass


class IQueueBottleneckVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> QueueBottleneckReport:
        pass


class IWorkerCapacityVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> WorkerCapacityReport:
        pass


class IAIProviderPerformanceVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> AIProviderPerformanceReport:
        pass


class IPerformanceRegressionVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> PerformanceRegressionReport:
        pass


class ICapacityBoundaryVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CapacityBoundaryReport:
        pass


class IOptimizationRecommendationsVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> OptimizationRecommendationsReport:
        pass


class IBottleneckDiscoveryScorer(ABC):
    @abstractmethod
    def score_reports(self, reports: Dict[str, Any]) -> EnterpriseBottleneckCertificationReport:
        pass


class IBottleneckDiscoveryExporter(ABC):
    @abstractmethod
    def export(
        self,
        reports: Dict[str, Any],
        certification: EnterpriseBottleneckCertificationReport,
        output_dir: str,
    ) -> List[str]:
        pass


class IBottleneckDiscoveryRuntime(ABC):
    @abstractmethod
    def run_full_verification(self, output_dir: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_latest_certification(self) -> Optional[EnterpriseBottleneckCertificationReport]:
        pass
