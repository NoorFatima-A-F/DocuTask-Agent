"""Domain Interfaces for Phase 7: Enterprise AI Automation Experience & Customer Simulation Platform."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .models import (
    ApprovalItem,
    AutomationTemplate,
    CaseStudyDocument,
    CustomerAnalyticsReport,
    DemoRunResult,
    DemoScript,
    EnterpriseConnector,
    EnterpriseTenant,
    ExceptionItem,
    OnboardingJourney,
    PortfolioPresentationArtifacts,
    TrustCenterReport,
    WorkflowDefinition,
    WorkflowExecutionResult,
)


class ITenantSimulationEngine(ABC):
    @abstractmethod
    def list_tenants(self) -> List[EnterpriseTenant]:
        """List all simulated enterprise organizations."""
        ...

    @abstractmethod
    def get_tenant(self, tenant_id: str) -> Optional[EnterpriseTenant]:
        """Retrieve tenant profile by ID."""
        ...

    @abstractmethod
    def verify_tenant_isolation(self, tenant_a_id: str, tenant_b_id: str) -> bool:
        """Validate data separation and permission boundaries between tenants."""
        ...


class IOnboardingEngine(ABC):
    @abstractmethod
    def start_onboarding(self, company_name: str, industry: str) -> OnboardingJourney:
        """Initialize 7-step customer onboarding journey."""
        ...

    @abstractmethod
    def advance_step(self, journey_id: str, step_data: Dict[str, Any]) -> OnboardingJourney:
        """Advance customer onboarding journey to next step."""
        ...

    @abstractmethod
    def get_journey(self, journey_id: str) -> Optional[OnboardingJourney]:
        """Get current onboarding status and progress."""
        ...


class ITemplateMarketplace(ABC):
    @abstractmethod
    def list_templates(self, industry_filter: Optional[str] = None) -> List[AutomationTemplate]:
        """List available AI automation templates."""
        ...

    @abstractmethod
    def get_template(self, template_id: str) -> Optional[AutomationTemplate]:
        """Get template specifications."""
        ...


class IWorkflowBuilderEngine(ABC):
    @abstractmethod
    def validate_workflow(self, workflow: WorkflowDefinition) -> Dict[str, Any]:
        """Validate DAG integrity, cycle absence, and node connectivity."""
        ...

    @abstractmethod
    def execute_workflow(self, workflow_id: str, input_payload: Dict[str, Any]) -> WorkflowExecutionResult:
        """Execute visual AI workflow synchronously."""
        ...


class IConnectorManager(ABC):
    @abstractmethod
    def list_connectors(self, category: Optional[str] = None) -> List[EnterpriseConnector]:
        """List enterprise connectors."""
        ...

    @abstractmethod
    def test_connection(self, connector_id: str) -> Dict[str, Any]:
        """Simulate ping, authentication verification, and data mapping."""
        ...


class IApprovalCenterEngine(ABC):
    @abstractmethod
    def get_pending_approvals(self, tenant_id: Optional[str] = None) -> List[ApprovalItem]:
        """Get items requiring human supervisor sign-off."""
        ...

    @abstractmethod
    def submit_decision(self, approval_id: str, decision: str, notes: Optional[str] = None) -> ApprovalItem:
        """Approve, reject, or request changes with feedback loop."""
        ...

    @abstractmethod
    def list_exceptions(self, tenant_id: Optional[str] = None) -> List[ExceptionItem]:
        """Get system exceptions and remediation suggestions."""
        ...


class ICustomerAnalyticsEngine(ABC):
    @abstractmethod
    def generate_analytics_report(self, tenant_id: str) -> CustomerAnalyticsReport:
        """Generate executive KPI and financial ROI metrics."""
        ...


class ITrustCenterEngine(ABC):
    @abstractmethod
    def get_trust_report(self) -> TrustCenterReport:
        """Get security posture, compliance standards, and AI governance state."""
        ...


class IDemoEngine(ABC):
    @abstractmethod
    def run_demo_scenario(self, scenario_key: str) -> DemoRunResult:
        """Execute 1-click interactive enterprise simulation run."""
        ...


class IPortfolioPresentationGenerator(ABC):
    @abstractmethod
    def generate_portfolio_artifacts(self, output_dir: Optional[str] = None) -> PortfolioPresentationArtifacts:
        """Generate case studies, architecture diagrams, and audience demo scripts."""
        ...


class ICustomerExperienceRuntime(ABC):
    @abstractmethod
    def run_full_simulation(self, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """Master orchestrator executing complete customer adoption journey."""
        ...
