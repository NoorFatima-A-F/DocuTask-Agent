"""Phase 3J.8: Enterprise Autoscaling & Elastic Capacity — Domain Interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    AIScalingReport,
    APIScalingReport,
    AutoscalingArchitectureReport,
    CloudScalingReport,
    CostScalingReport,
    DatabaseScalingImpactReport,
    EnterpriseAutoscalingCertificationReport,
    K8sScalingReadinessReport,
    QueueAutoscalingReport,
    ScaleDownSafetyReport,
    ScaleUpValidationReport,
    ScalingFailureReport,
    ScalingMetricsReport,
    ScalingPolicyReport,
    WorkerScalingReport,
)


class IPerformanceVerifier(ABC):
    """Base interface for all Phase 3J.8 autoscaling verifiers."""

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


class IAutoscalingArchitectureVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> AutoscalingArchitectureReport: pass


class IScalingMetricsVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ScalingMetricsReport: pass


class IWorkerScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> WorkerScalingReport: pass


class IQueueAutoscalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> QueueAutoscalingReport: pass


class IAPIScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> APIScalingReport: pass


class IScalingPolicyVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ScalingPolicyReport: pass


class IScaleUpVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ScaleUpValidationReport: pass


class IScaleDownSafetyVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ScaleDownSafetyReport: pass


class IDatabaseScalingImpactVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> DatabaseScalingImpactReport: pass


class IAIProviderScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> AIScalingReport: pass


class IK8sScalingReadinessVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> K8sScalingReadinessReport: pass


class ICloudScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CloudScalingReport: pass


class ICostScalingVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> CostScalingReport: pass


class IScalingFailureVerifier(IPerformanceVerifier):
    @abstractmethod
    def verify(self) -> ScalingFailureReport: pass


class IAutoscalingScorer(ABC):
    @abstractmethod
    def score_reports(self, reports: Dict[str, Any]) -> EnterpriseAutoscalingCertificationReport: pass


class IAutoscalingExporter(ABC):
    @abstractmethod
    def export(self, reports: Dict[str, Any], certification: EnterpriseAutoscalingCertificationReport, output_dir: str) -> List[str]: pass


class IAutoscalingRuntime(ABC):
    @abstractmethod
    def run_full_verification(self, output_dir: str) -> Dict[str, Any]: pass

    @abstractmethod
    def get_latest_certification(self) -> Optional[EnterpriseAutoscalingCertificationReport]: pass
