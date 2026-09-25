"""Domain Interfaces for Phase 4: Enterprise Cross-System Integration & End-to-End Platform Validation Framework."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from .models import (
    APIChainReport,
    AgentCollaborationReport,
    CognitiveIntegrationReport,
    CrossSystemIntegrationQualityReport,
    CrossSystemIntegrationQualityScore,
    CrossSystemPerformanceReport,
    DataIntegrityReport,
    DependencyMappingReport,
    DeploymentIntegrationReport,
    EnterpriseWorkflowsReport,
    EventBusReport,
    EvidenceGenerationReport,
    FailurePropagationReport,
    IntegrationRegressionReport,
    InterfaceContractReport,
    KnowledgeFlowReport,
    LifecycleIntegrationReport,
    MarketplaceValidationReport,
    MemoryInteractionReport,
    ObservabilityIntegrationReport,
    PlanningPipelineReport,
    SchedulerReport,
    SecurityBoundaryReport,
    StatePropagationReport,
)


class IBaseCrossSystemVerifier(ABC):
    @property
    @abstractmethod
    def verifier_id(self) -> str:
        """Unique verifier identifier."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable verifier name."""
        ...

    @abstractmethod
    def verify(self) -> Any:
        """Execute verification logic and return typed report."""
        ...


class IDependencyMappingVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> DependencyMappingReport: ...


class IInterfaceContractVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> InterfaceContractReport: ...


class IAPIChainVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> APIChainReport: ...


class IStatePropagationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> StatePropagationReport: ...


class IKnowledgeFlowVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> KnowledgeFlowReport: ...


class IMemoryInteractionVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> MemoryInteractionReport: ...


class IPlanningPipelineVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> PlanningPipelineReport: ...


class IAgentCollaborationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> AgentCollaborationReport: ...


class ICognitiveIntegrationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> CognitiveIntegrationReport: ...


class ISecurityBoundaryVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> SecurityBoundaryReport: ...


class ILifecycleIntegrationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> LifecycleIntegrationReport: ...


class IDeploymentIntegrationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> DeploymentIntegrationReport: ...


class IMarketplaceValidationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> MarketplaceValidationReport: ...


class IEventBusVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> EventBusReport: ...


class ISchedulerVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> SchedulerReport: ...


class IObservabilityIntegrationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> ObservabilityIntegrationReport: ...


class IDataIntegrityVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> DataIntegrityReport: ...


class IFailurePropagationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> FailurePropagationReport: ...


class ICrossSystemPerformanceVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> CrossSystemPerformanceReport: ...


class IEnterpriseWorkflowsVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> EnterpriseWorkflowsReport: ...


class IIntegrationRegressionVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> IntegrationRegressionReport: ...


class IEvidenceGenerationVerifier(IBaseCrossSystemVerifier):
    @abstractmethod
    def verify(self) -> EvidenceGenerationReport: ...


class ICrossSystemIntegrationQualityScorer(ABC):
    @abstractmethod
    def calculate_score(self, reports: Dict[str, Any]) -> CrossSystemIntegrationQualityScore:
        """Compute the weighted multi-pillar certification score."""
        ...


class ICrossSystemIntegrationQualityExporter(ABC):
    @abstractmethod
    def export(
        self,
        report: CrossSystemIntegrationQualityReport,
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """Export artifacts to disk and return file paths with SHA-256 signatures."""
        ...


class ICrossSystemIntegrationVerificationRuntime(ABC):
    @abstractmethod
    def execute_all(self, output_dir: Optional[str] = None) -> CrossSystemIntegrationQualityReport:
        """Execute all 22 verifiers, score results, export artifacts, and return overall report."""
        ...
