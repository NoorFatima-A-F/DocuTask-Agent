"""Domain Interfaces for Phase 5: Enterprise Autonomous Workflow & Business Process Validation Framework."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .models import (
    AuditTrailValidationReport,
    AutonomousRecoveryReport,
    AutonomousWorkflowQualityReport,
    AutonomousWorkflowQualityScore,
    BusinessKPIReport,
    BusinessRuleEnforcementReport,
    BusinessValueReport,
    CompleteWorkflowExecutionReport,
    ComplianceValidationReport,
    CostValidationReport,
    DecisionQualityReport,
    EnterpriseDatasetReport,
    ExceptionWorkflowReport,
    ExecutiveReadinessReport,
    ExplainabilityValidationReport,
    HumanInTheLoopReport,
    LongRunningWorkflowReport,
    MultiAgentBusinessCollaborationReport,
    OrganizationalWorkflowReport,
    ScenarioLibraryReport,
    WorkflowOptimizationReport,
    WorkflowScalabilityReport,
)


class IBaseWorkflowVerifier(ABC):
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


class IScenarioLibraryVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> ScenarioLibraryReport: ...


class ICompleteWorkflowExecutionVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> CompleteWorkflowExecutionReport: ...


class IHumanInTheLoopVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> HumanInTheLoopReport: ...


class IMultiAgentBusinessCollaborationVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> MultiAgentBusinessCollaborationReport: ...


class IDecisionQualityVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> DecisionQualityReport: ...


class IBusinessRuleEnforcementVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> BusinessRuleEnforcementReport: ...


class IExceptionWorkflowVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> ExceptionWorkflowReport: ...


class IBusinessKPIVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> BusinessKPIReport: ...


class IAutonomousRecoveryVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> AutonomousRecoveryReport: ...


class IOrganizationalWorkflowVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> OrganizationalWorkflowReport: ...


class ILongRunningWorkflowVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> LongRunningWorkflowReport: ...


class IExplainabilityValidationVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> ExplainabilityValidationReport: ...


class IAuditTrailValidationVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> AuditTrailValidationReport: ...


class IComplianceValidationVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> ComplianceValidationReport: ...


class ICostValidationVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> CostValidationReport: ...


class IWorkflowOptimizationVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> WorkflowOptimizationReport: ...


class IBusinessValueVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> BusinessValueReport: ...


class IEnterpriseDatasetVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> EnterpriseDatasetReport: ...


class IWorkflowScalabilityVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> WorkflowScalabilityReport: ...


class IExecutiveReadinessVerifier(IBaseWorkflowVerifier):
    @abstractmethod
    def verify(self) -> ExecutiveReadinessReport: ...


class IAutonomousWorkflowQualityScorer(ABC):
    @abstractmethod
    def calculate_score(self, reports: Dict[str, Any]) -> AutonomousWorkflowQualityScore:
        """Compute the 7-pillar weighted business certification score."""
        ...


class IAutonomousWorkflowQualityExporter(ABC):
    @abstractmethod
    def export(
        self,
        report: AutonomousWorkflowQualityReport,
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """Export evidence artifacts and return path mappings with SHA-256 signatures."""
        ...


class IAutonomousWorkflowVerificationRuntime(ABC):
    @abstractmethod
    def execute_all(self, output_dir: Optional[str] = None) -> AutonomousWorkflowQualityReport:
        """Execute all 20 verifiers, score results, export evidence, and return report."""
        ...
