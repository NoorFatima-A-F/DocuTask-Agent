"""FastAPI Router for Phase 7: Enterprise AI Customer Experience & Simulation Platform."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..domain.models import (
    ApprovalItem,
    AutomationTemplate,
    CustomerAnalyticsReport,
    DemoRunResult,
    EnterpriseConnector,
    EnterpriseTenant,
    ExceptionItem,
    OnboardingJourney,
    PortfolioPresentationArtifacts,
    TrustCenterReport,
    WorkflowDefinition,
    WorkflowExecutionResult,
)
from ..runtime.customer_experience_runtime import CustomerExperienceRuntime


router = APIRouter(prefix="/api/v1/customer-experience", tags=["Enterprise Customer Experience & Demo"])
_runtime = CustomerExperienceRuntime()


class OnboardStartRequest(BaseModel):
    company_name: str
    industry: str


class ApprovalDecisionRequest(BaseModel):
    decision: str
    notes: Optional[str] = None


@router.get("/health")
def get_customer_experience_health() -> Dict[str, Any]:
    """Return operational status of the Enterprise Customer Experience platform."""
    return {
        "status": "healthy",
        "phase": "Phase 7 - Enterprise AI Automation Experience & Customer Simulation Platform",
        "tenants_count": len(_runtime.tenant_engine.list_tenants()),
        "templates_count": len(_runtime.template_marketplace.list_templates()),
        "connectors_count": len(_runtime.connector_manager.list_connectors()),
    }


@router.get("/tenants", response_model=List[EnterpriseTenant])
def list_tenants() -> List[EnterpriseTenant]:
    """List all simulated enterprise customer organizations."""
    return _runtime.tenant_engine.list_tenants()


@router.get("/tenants/{tenant_id}", response_model=EnterpriseTenant)
def get_tenant(tenant_id: str) -> EnterpriseTenant:
    """Get single tenant details."""
    t = _runtime.tenant_engine.get_tenant(tenant_id)
    if not t:
        raise HTTPException(status_code=404, detail=f"Tenant '{tenant_id}' not found")
    return t


@router.post("/onboarding/start", response_model=OnboardingJourney)
def start_onboarding(req: OnboardStartRequest) -> OnboardingJourney:
    """Initialize 7-step customer onboarding wizard."""
    return _runtime.onboarding_engine.start_onboarding(req.company_name, req.industry)


@router.get("/templates", response_model=List[AutomationTemplate])
def list_templates(industry: Optional[str] = None) -> List[AutomationTemplate]:
    """List pre-configured AI automation templates."""
    return _runtime.template_marketplace.list_templates(industry_filter=industry)


@router.get("/workflows", response_model=List[WorkflowDefinition])
def list_workflows(tenant_id: Optional[str] = None) -> List[WorkflowDefinition]:
    """List visual workflow definitions."""
    return _runtime.workflow_builder.list_workflows(tenant_id=tenant_id)


@router.post("/workflows/{workflow_id}/execute", response_model=WorkflowExecutionResult)
def execute_workflow(workflow_id: str, payload: Optional[Dict[str, Any]] = None) -> WorkflowExecutionResult:
    """Execute a visual DAG workflow."""
    return _runtime.workflow_builder.execute_workflow(workflow_id, payload or {})


@router.get("/connectors", response_model=List[EnterpriseConnector])
def list_connectors(category: Optional[str] = None) -> List[EnterpriseConnector]:
    """List enterprise connectors."""
    return _runtime.connector_manager.list_connectors(category=category)


@router.post("/connectors/{connector_id}/test")
def test_connector(connector_id: str) -> Dict[str, Any]:
    """Simulate connector authentication and diagnostic ping."""
    return _runtime.connector_manager.test_connection(connector_id)


@router.get("/approvals", response_model=List[ApprovalItem])
def list_pending_approvals(tenant_id: Optional[str] = None) -> List[ApprovalItem]:
    """Get pending human approval queue."""
    return _runtime.approval_engine.get_pending_approvals(tenant_id=tenant_id)


@router.post("/approvals/{approval_id}/decision", response_model=ApprovalItem)
def submit_approval_decision(approval_id: str, req: ApprovalDecisionRequest) -> ApprovalItem:
    """Submit human supervisor sign-off or exception handling."""
    try:
        return _runtime.approval_engine.submit_decision(approval_id, req.decision, req.notes)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/exceptions", response_model=List[ExceptionItem])
def list_exceptions(tenant_id: Optional[str] = None) -> List[ExceptionItem]:
    """List exception and remediation queue."""
    return _runtime.approval_engine.list_exceptions(tenant_id=tenant_id)


@router.get("/analytics", response_model=CustomerAnalyticsReport)
def get_customer_analytics(tenant_id: str = "TENANT-FIN-01") -> CustomerAnalyticsReport:
    """Get customer business outcomes, liberated hours, and financial ROI."""
    return _runtime.analytics_engine.generate_analytics_report(tenant_id)


@router.get("/trust-center", response_model=TrustCenterReport)
def get_trust_center() -> TrustCenterReport:
    """Get enterprise AI trust, security boundaries, and model governance."""
    return _runtime.trust_center.get_trust_report()


@router.post("/demo/run", response_model=DemoRunResult)
def run_interactive_demo(scenario: str = Query(default="invoice_automation")) -> DemoRunResult:
    """Trigger 1-Click Interactive Enterprise Demonstration."""
    return _runtime.demo_engine.run_demo_scenario(scenario)


@router.get("/portfolio/presentation", response_model=PortfolioPresentationArtifacts)
def get_portfolio_presentation() -> PortfolioPresentationArtifacts:
    """Retrieve generated case studies, architecture diagrams, and audience demo scripts."""
    return _runtime.portfolio_generator.generate_portfolio_artifacts()


@router.post("/simulation/run-all")
def run_full_simulation() -> Dict[str, Any]:
    """Execute complete end-to-end customer simulation and export all evidence."""
    return _runtime.run_full_simulation()
