"""Comprehensive Unit and Integration Tests for Phase 7: Enterprise AI Customer Experience & Simulation Platform."""

import json
import os
import shutil
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.customer_experience.api.customer_experience_api import router
from app.customer_experience.tenant_demo.tenant_simulation_engine import TenantSimulationEngine
from app.customer_experience.onboarding.customer_onboarding_engine import CustomerOnboardingEngine
from app.customer_experience.templates.template_marketplace import TemplateMarketplace
from app.customer_experience.workflow_builder.workflow_builder_engine import WorkflowBuilderEngine
from app.customer_experience.connectors.connector_manager import ConnectorManager
from app.customer_experience.approvals.approval_center_engine import ApprovalCenterEngine
from app.customer_experience.analytics.customer_analytics_engine import CustomerAnalyticsEngine
from app.customer_experience.trust_center.trust_center_engine import TrustCenterEngine
from app.customer_experience.demo_engine.interactive_demo_engine import InteractiveDemoEngine
from app.customer_experience.portfolio_generator.portfolio_presentation_generator import PortfolioPresentationGenerator
from app.customer_experience.runtime.customer_experience_runtime import CustomerExperienceRuntime
from app.customer_experience.domain.models import (
    ApprovalStatus,
    ConnectorCategory,
    ConnectorStatus,
    IndustrySector,
    OnboardingStepStatus,
    SimulationRunStatus,
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowNode,
    WorkflowNodeType,
)


@pytest.fixture
def temp_evidence_dir():
    temp_dir = tempfile.mkdtemp(prefix="cust_exp_test_evidence_")
    yield temp_dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# 1. Tenant Simulation & Isolation Tests (Part A)
def test_tenant_simulation_engine_listing():
    engine = TenantSimulationEngine()
    tenants = engine.list_tenants()
    assert len(tenants) == 4
    tenant_ids = [t.tenant_id for t in tenants]
    assert "TENANT-FIN-01" in tenant_ids
    assert "TENANT-HLT-02" in tenant_ids
    assert "TENANT-HR-03" in tenant_ids
    assert "TENANT-LEG-04" in tenant_ids


def test_tenant_isolation_verification():
    engine = TenantSimulationEngine()
    # Different tenants should be isolated
    assert engine.verify_tenant_isolation("TENANT-FIN-01", "TENANT-HLT-02") is True
    assert engine.verify_tenant_isolation("TENANT-HR-03", "TENANT-LEG-04") is True
    # Same tenant comparison or invalid tenant should return False
    assert engine.verify_tenant_isolation("TENANT-FIN-01", "TENANT-FIN-01") is False
    assert engine.verify_tenant_isolation("TENANT-FIN-01", "INVALID_ID") is False


# 2. Customer Onboarding Journey Tests (Part B)
def test_customer_onboarding_lifecycle():
    engine = CustomerOnboardingEngine()
    journey = engine.start_onboarding("Vanguard Logistics Corp", "Finance & Banking")
    assert journey.journey_id.startswith("ONBOARD-")
    assert journey.current_step == 1
    assert journey.total_steps == 7
    assert journey.is_completed is False
    assert len(journey.steps) == 7

    # Advance through all 7 steps
    for step_num in range(1, 8):
        journey = engine.advance_step(journey.journey_id, {"step": step_num, "status": "OK"})
        if step_num < 7:
            assert journey.current_step == step_num + 1
            assert journey.is_completed is False

    assert journey.is_completed is True
    assert journey.current_step == 7
    assert journey.completed_at is not None


# 3. AI Automation Template Marketplace Tests (Part C)
def test_template_marketplace_listing_and_filtering():
    marketplace = TemplateMarketplace()
    templates = marketplace.list_templates()
    assert len(templates) >= 5

    finance_templates = marketplace.list_templates(industry_filter="Finance & Banking")
    assert len(finance_templates) >= 1
    assert finance_templates[0].industry == IndustrySector.FINANCE
    assert finance_templates[0].rating >= 4.8

    hr_template = marketplace.get_template("TMPL-HR-02")
    assert hr_template is not None
    assert hr_template.industry == IndustrySector.HR_RECRUITING
    assert len(hr_template.kpis) >= 1


# 4. Visual Workflow Builder & DAG Validation Tests (Part D)
def test_workflow_builder_dag_valid():
    engine = WorkflowBuilderEngine()
    workflow = engine.get_workflow("WF-DEFAULT-INVOICE")
    assert workflow is not None

    validation = engine.validate_workflow(workflow)
    assert validation["is_valid"] is True
    assert len(validation["errors"]) == 0
    assert validation["total_nodes"] == 6


def test_workflow_builder_cycle_detection():
    engine = WorkflowBuilderEngine()
    # Construct a cyclical workflow
    nodes = [
        WorkflowNode(node_id="n1", label="Trigger", node_type=WorkflowNodeType.TRIGGER),
        WorkflowNode(node_id="n2", label="Agent A", node_type=WorkflowNodeType.AGENT),
        WorkflowNode(node_id="n3", label="Agent B", node_type=WorkflowNodeType.AGENT),
    ]
    edges = [
        WorkflowEdge(edge_id="e1", source_node_id="n1", target_node_id="n2"),
        WorkflowEdge(edge_id="e2", source_node_id="n2", target_node_id="n3"),
        WorkflowEdge(edge_id="e3", source_node_id="n3", target_node_id="n2"),  # Cycle: n2 -> n3 -> n2
    ]
    cyclic_wf = WorkflowDefinition(
        workflow_id="WF-CYCLIC",
        tenant_id="TENANT-FIN-01",
        name="Cyclic Workflow",
        nodes=nodes,
        edges=edges,
    )
    validation = engine.validate_workflow(cyclic_wf)
    assert validation["is_valid"] is False
    assert any("Cycle detected" in err for err in validation["errors"])


def test_workflow_execution():
    engine = WorkflowBuilderEngine()
    result = engine.execute_workflow("WF-DEFAULT-INVOICE", {"tenant_id": "TENANT-FIN-01"})
    assert result.status == "SUCCESS"
    assert result.nodes_executed == 6
    assert result.duration_ms > 0
    assert len(result.errors) == 0


# 5. Enterprise Connector Simulation Tests (Part E)
def test_connector_manager_listing_and_ping():
    manager = ConnectorManager()
    connectors = manager.list_connectors()
    assert len(connectors) >= 10

    comm_connectors = manager.list_connectors(category="COMMUNICATION")
    assert len(comm_connectors) >= 4

    ping_result = manager.test_connection("CONN-GMAIL")
    assert ping_result["success"] is True
    assert ping_result["status"] == "HEALTHY"
    assert ping_result["auth_verified"] is True


# 6. Human-in-the-Loop Collaboration Tests (Part F)
def test_approval_center_workflow():
    engine = ApprovalCenterEngine()
    approvals = engine.get_pending_approvals()
    assert len(approvals) >= 2

    # Submit decision
    item = engine.submit_decision("APP-2026-001", "APPROVE", "Supervisor signoff verified")
    assert item.status == ApprovalStatus.APPROVED
    assert item.decided_at is not None

    # Verify pending queue decreased
    pending_after = engine.get_pending_approvals()
    assert len(pending_after) == len(approvals) - 1


def test_exception_center_listing():
    engine = ApprovalCenterEngine()
    exceptions = engine.list_exceptions()
    assert len(exceptions) >= 2
    for exc in exceptions:
        assert exc.suggested_remediation
        assert exc.severity is not None


# 7. Customer Value Analytics & Financial ROI Tests (Part G)
def test_customer_analytics_engine():
    engine = CustomerAnalyticsEngine()
    report = engine.generate_analytics_report("TENANT-FIN-01")
    assert report.tenant_id == "TENANT-FIN-01"
    assert report.automation_rate_pct >= 90.0
    assert report.straight_through_processing_pct >= 90.0
    assert report.financial_roi.net_annual_savings >= 2000000.0
    assert report.financial_roi.cost_reduction_pct >= 90.0
    assert report.financial_roi.roi_multiple >= 4.0
    assert len(report.metrics) >= 6


# 8. AI Trust Center & Model Governance Tests (Part H)
def test_trust_center_engine():
    engine = TrustCenterEngine()
    report = engine.get_trust_report()
    assert report.overall_trust_score == 100.0
    assert "SOC2 Type II" in report.compliance_standards
    assert "HIPAA Security Rule" in report.compliance_standards
    assert len(report.security_boundaries) >= 3
    assert len(report.model_governance) >= 2
    for gov in report.model_governance:
        assert gov.prompt_hash.startswith("sha256:")
        assert gov.temperature == 0.0


# 9. 1-Click Interactive Demo Engine Tests (Part I)
def test_interactive_demo_engine():
    engine = InteractiveDemoEngine()
    result = engine.run_demo_scenario("invoice_automation")
    assert result.status == SimulationRunStatus.COMPLETED
    assert result.confidence_score >= 0.98
    assert len(result.steps) == 6
    assert result.total_duration_ms > 0
    assert result.audit_trace_id.startswith("TRACE-")
    assert "vendor" in result.extracted_fields


# 10. Portfolio Presentation & Case Study Generator Tests (Part J-M)
def test_portfolio_presentation_generator(temp_evidence_dir):
    generator = PortfolioPresentationGenerator()
    artifacts = generator.generate_portfolio_artifacts(output_dir=temp_evidence_dir)

    assert "graph TD" in artifacts.architecture_diagram_mermaid
    assert len(artifacts.case_studies) >= 2
    assert len(artifacts.demo_scripts) == 3

    # Verify generated files
    files = os.listdir(temp_evidence_dir)
    assert any(f.startswith("case_study_") for f in files)
    assert any(f.startswith("demo_script_") for f in files)
    assert "platform_architecture.mermaid" in files


# 11. Master Runtime Full Simulation
def test_customer_experience_runtime(temp_evidence_dir):
    runtime = CustomerExperienceRuntime()
    result = runtime.run_full_simulation(output_dir=temp_evidence_dir)

    assert result["status"] == "ENTERPRISE_DEMO_READY"
    assert result["tenant_simulation"]["total_tenants"] == 4
    assert result["tenant_simulation"]["isolation_verified"] is True
    assert result["onboarding_simulation"]["is_completed"] is True
    assert result["connectors"]["total_connectors"] >= 10
    assert result["customer_analytics"]["financial_roi"]["net_annual_savings"] > 2000000.0

    manifest_path = os.path.join(temp_evidence_dir, "manifest.json")
    assert os.path.exists(manifest_path)
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert len(manifest) >= 5


# 12. FastAPI Router Endpoints Tests
def test_api_health(api_client):
    response = api_client.get("/api/v1/customer-experience/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["tenants_count"] == 4


def test_api_tenants(api_client):
    response = api_client.get("/api/v1/customer-experience/tenants")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4

    single_response = api_client.get("/api/v1/customer-experience/tenants/TENANT-FIN-01")
    assert single_response.status_code == 200
    assert single_response.json()["name"] == "Apex Global Financial Services"


def test_api_onboarding_flow(api_client):
    response = api_client.post(
        "/api/v1/customer-experience/onboarding/start",
        json={"company_name": "Nexus Global Corp", "industry": "Finance & Banking"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Nexus Global Corp"
    assert data["current_step"] == 1


def test_api_templates(api_client):
    response = api_client.get("/api/v1/customer-experience/templates")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5


def test_api_workflows(api_client):
    response = api_client.get("/api/v1/customer-experience/workflows")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

    exec_response = api_client.post(
        "/api/v1/customer-experience/workflows/WF-DEFAULT-INVOICE/execute",
        json={"tenant_id": "TENANT-FIN-01"},
    )
    assert exec_response.status_code == 200
    assert exec_response.json()["status"] == "SUCCESS"


def test_api_connectors(api_client):
    response = api_client.get("/api/v1/customer-experience/connectors")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10

    test_ping = api_client.post("/api/v1/customer-experience/connectors/CONN-GMAIL/test")
    assert test_ping.status_code == 200
    assert test_ping.json()["success"] is True


def test_api_approvals_and_decisions(api_client):
    response = api_client.get("/api/v1/customer-experience/approvals")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

    decision_resp = api_client.post(
        "/api/v1/customer-experience/approvals/APP-2026-001/decision",
        json={"decision": "APPROVE", "notes": "Approved via API"},
    )
    assert decision_resp.status_code == 200
    assert decision_resp.json()["status"] == "APPROVED"


def test_api_analytics_and_trust_center(api_client):
    analytics_resp = api_client.get("/api/v1/customer-experience/analytics")
    assert analytics_resp.status_code == 200
    assert analytics_resp.json()["automation_rate_pct"] >= 90.0

    trust_resp = api_client.get("/api/v1/customer-experience/trust-center")
    assert trust_resp.status_code == 200
    assert trust_resp.json()["overall_trust_score"] == 100.0


def test_api_demo_run(api_client):
    demo_resp = api_client.post("/api/v1/customer-experience/demo/run?scenario=invoice_automation")
    assert demo_resp.status_code == 200
    data = demo_resp.json()
    assert data["status"] == "COMPLETED"
    assert len(data["steps"]) == 6
