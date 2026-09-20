"""
Phase 13.20: Autonomous AI Application Lifecycle Platform (AAILP) API Endpoints.
Mounted under /api/v1/ai-lifecycle.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Query, Body
from app.platform_ai_lifecycle.runtime.lifecycle_master_orchestrator import LifecycleMasterOrchestrator
from app.platform_ai_lifecycle.models.schemas import (
    AgentApplication,
    AgentCategory,
    AgentLifecycleState,
    AgentVersion,
    AgentTestResult,
    AgentSecurityScan,
    AgentApproval,
    ApprovalStage,
    ApprovalDecision,
    AgentDeployment,
    DeploymentEnvironment,
    DeploymentStrategy,
    AgentDependency,
    AgentTemplate,
    AgentMarketplaceListing,
    AgentAnalytics,
    AgentRetirementPlan,
    LifecycleOverview,
)

router = APIRouter()
orchestrator = LifecycleMasterOrchestrator()


# 1. Executive Control Plane & Overview
@router.get("/overview", response_model=LifecycleOverview, tags=["AI Lifecycle Executive Control"])
async def get_lifecycle_overview():
    """Returns platform-wide AI application lifecycle statistics & ROI."""
    return orchestrator.get_overview()


@router.post("/full-release", tags=["AI Lifecycle Executive Control"])
async def full_lifecycle_release(payload: Dict[str, Any] = Body(...)):
    """Runs end-to-end automated DevSecOps release pipeline for an AI application."""
    required = ["tenant_id", "organization_id", "workspace_id", "name", "slug", "owner_id", "owner_email", "system_prompt"]
    if not all(k in payload for k in required):
        raise HTTPException(status_code=400, detail="Missing required release fields")

    cat_str = payload.get("category", "AUTOMATION")
    category = AgentCategory(cat_str) if cat_str in AgentCategory.__members__ else AgentCategory.AUTOMATION

    return orchestrator.full_lifecycle_release(
        tenant_id=payload["tenant_id"],
        organization_id=payload["organization_id"],
        workspace_id=payload["workspace_id"],
        name=payload["name"],
        slug=payload["slug"],
        category=category,
        owner_id=payload["owner_id"],
        owner_email=payload["owner_email"],
        system_prompt=payload["system_prompt"],
        tools=payload.get("tools", []),
        connectors=payload.get("connectors", []),
    )


# 2. Agent Inventory & Registry
@router.get("/agents", response_model=List[AgentApplication], tags=["Agent Registry"])
async def list_agents(
    tenant_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    category: Optional[AgentCategory] = None,
    state: Optional[AgentLifecycleState] = None,
):
    return orchestrator.registry.list_agents(tenant_id, workspace_id, category, state)


@router.post("/agents", response_model=AgentApplication, tags=["Agent Registry"])
async def register_agent(payload: Dict[str, Any] = Body(...)):
    cat_str = payload.get("category", "AUTOMATION")
    category = AgentCategory(cat_str) if cat_str in AgentCategory.__members__ else AgentCategory.AUTOMATION
    return orchestrator.registry.register_agent(
        tenant_id=payload["tenant_id"],
        organization_id=payload["organization_id"],
        workspace_id=payload["workspace_id"],
        name=payload["name"],
        slug=payload["slug"],
        category=category,
        owner_id=payload["owner_id"],
        owner_email=payload["owner_email"],
        description=payload.get("description", ""),
        tags=payload.get("tags", []),
    )


@router.get("/agents/{agent_id}", response_model=AgentApplication, tags=["Agent Registry"])
async def get_agent(agent_id: str):
    agent = orchestrator.registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/agents/{agent_id}/state", response_model=AgentApplication, tags=["Agent Registry"])
async def update_agent_lifecycle_state(agent_id: str, state: AgentLifecycleState = Query(...)):
    try:
        return orchestrator.registry.update_lifecycle_state(agent_id, state)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 3. Version Control (AVCS)
@router.get("/agents/{agent_id}/versions", response_model=List[AgentVersion], tags=["Agent Version Control"])
async def list_versions(agent_id: str):
    return orchestrator.versioning.list_versions(agent_id)


@router.post("/agents/{agent_id}/versions", response_model=AgentVersion, tags=["Agent Version Control"])
async def create_version(agent_id: str, payload: Dict[str, Any] = Body(...)):
    return orchestrator.versioning.create_version(
        agent_id=agent_id,
        version_tag=payload["version_tag"],
        system_prompt=payload["system_prompt"],
        tools=payload.get("tools", []),
        connectors=payload.get("connectors", []),
        model_family=payload.get("model_family", "gemini-pro"),
        changelog=payload.get("changelog", ""),
        accuracy_score=payload.get("accuracy_score", 0.95),
        cost_per_execution_usd=payload.get("cost_per_execution_usd", 0.004),
        parameters=payload.get("parameters", {}),
    )


@router.post("/agents/{agent_id}/rollback", response_model=AgentVersion, tags=["Agent Version Control"])
async def rollback_version(agent_id: str, target_version_tag: str = Query(...)):
    try:
        ver = orchestrator.versioning.rollback_to_version(agent_id, target_version_tag)
        orchestrator.registry.update_lifecycle_state(agent_id, AgentLifecycleState.DEPLOYED)
        return ver
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 4. Automated Testing
@router.post("/agents/{agent_id}/test", response_model=AgentTestResult, tags=["AI Quality & Security Testing"])
async def run_agent_tests(agent_id: str, version_tag: str = Query("1.0.0")):
    return orchestrator.testing.run_comprehensive_test_suite(agent_id, version_tag)


@router.get("/agents/{agent_id}/test-results", response_model=List[AgentTestResult], tags=["AI Quality & Security Testing"])
async def list_test_results(agent_id: str):
    return orchestrator.testing.list_test_results(agent_id)


# 5. Security Scanner
@router.post("/agents/{agent_id}/security-scan", response_model=AgentSecurityScan, tags=["Security Scanner"])
async def scan_agent_security(agent_id: str, payload: Dict[str, Any] = Body(...)):
    return orchestrator.security.scan_agent_version(
        agent_id=agent_id,
        version_tag=payload.get("version_tag", "1.0.0"),
        system_prompt=payload["system_prompt"],
        tools=payload.get("tools", []),
    )


@router.get("/agents/{agent_id}/security-scans", response_model=List[AgentSecurityScan], tags=["Security Scanner"])
async def list_security_scans(agent_id: str):
    return orchestrator.security.list_scans(agent_id)


# 6. Approval Workflow
@router.post("/agents/{agent_id}/approvals/submit", response_model=AgentApproval, tags=["Approval Workflow"])
async def submit_for_approval(agent_id: str, payload: Dict[str, Any] = Body(...)):
    return orchestrator.approvals.submit_for_approval(
        agent_id=agent_id,
        version_tag=payload.get("version_tag", "1.0.0"),
        submitter_id=payload["submitter_id"],
        submitter_email=payload["submitter_email"],
    )


@router.post("/agents/{agent_id}/approvals/review", response_model=AgentApproval, tags=["Approval Workflow"])
async def review_approval(agent_id: str, payload: Dict[str, Any] = Body(...)):
    stage_str = payload.get("stage", "FINAL_RELEASE")
    stage = ApprovalStage(stage_str) if stage_str in ApprovalStage.__members__ else ApprovalStage.FINAL_RELEASE
    dec_str = payload.get("decision", "APPROVED")
    decision = ApprovalDecision(dec_str) if dec_str in ApprovalDecision.__members__ else ApprovalDecision.APPROVED

    return orchestrator.approvals.review_and_decide(
        approval_id=payload["approval_id"],
        stage=stage,
        decision=decision,
        approver_id=payload["approver_id"],
        approver_email=payload["approver_email"],
        comments=payload.get("comments", ""),
    )


@router.get("/agents/{agent_id}/approvals", response_model=List[AgentApproval], tags=["Approval Workflow"])
async def list_approvals(agent_id: str):
    return orchestrator.approvals.list_approvals(agent_id)


# 7. Deployment Engine
@router.post("/agents/{agent_id}/deploy", response_model=AgentDeployment, tags=["Distributed Deployment"])
async def deploy_agent(agent_id: str, payload: Dict[str, Any] = Body(...)):
    env_str = payload.get("environment", "PRODUCTION")
    environment = DeploymentEnvironment(env_str) if env_str in DeploymentEnvironment.__members__ else DeploymentEnvironment.PRODUCTION
    strat_str = payload.get("strategy", "CANARY")
    strategy = DeploymentStrategy(strat_str) if strat_str in DeploymentStrategy.__members__ else DeploymentStrategy.CANARY

    dep = orchestrator.deployment.deploy_agent_version(
        agent_id=agent_id,
        version_tag=payload.get("version_tag", "1.0.0"),
        environment=environment,
        strategy=strategy,
        traffic_weight_pct=payload.get("traffic_weight_pct", 100),
        cluster_id=payload.get("cluster_id", "cluster_us_east_primary"),
    )
    orchestrator.registry.update_lifecycle_state(agent_id, AgentLifecycleState.DEPLOYED)
    return dep


@router.get("/agents/{agent_id}/deployments", response_model=List[AgentDeployment], tags=["Distributed Deployment"])
async def list_deployments(agent_id: str):
    return orchestrator.deployment.list_deployments(agent_id)


# 8. Dependency Graph
@router.get("/agents/{agent_id}/dependencies", response_model=List[AgentDependency], tags=["Dependency Graph"])
async def list_dependencies(agent_id: str):
    return orchestrator.dependencies.list_dependencies(agent_id)


@router.get("/agents/{agent_id}/dependencies/validate", tags=["Dependency Graph"])
async def validate_dependencies(agent_id: str):
    return orchestrator.dependencies.validate_dependency_graph(agent_id)


# 9. Starter Templates
@router.get("/templates", response_model=List[AgentTemplate], tags=["Starter Templates"])
async def list_templates(category: Optional[AgentCategory] = None):
    return orchestrator.templates.list_templates(category)


# 10. Marketplace
@router.get("/marketplace/listings", response_model=List[AgentMarketplaceListing], tags=["AI Marketplace"])
async def list_marketplace_listings(category: Optional[AgentCategory] = None):
    return orchestrator.marketplace.list_listings(category)


@router.post("/marketplace/publish", response_model=AgentMarketplaceListing, tags=["AI Marketplace"])
async def publish_to_marketplace(payload: Dict[str, Any] = Body(...)):
    cat_str = payload.get("category", "AUTOMATION")
    category = AgentCategory(cat_str) if cat_str in AgentCategory.__members__ else AgentCategory.AUTOMATION
    return orchestrator.marketplace.publish_agent(
        agent_id=payload["agent_id"],
        title=payload["title"],
        publisher_name=payload["publisher_name"],
        category=category,
        description=payload["description"],
        version=payload.get("version", "1.0.0"),
        price_monthly_usd=payload.get("price_monthly_usd", 0.0),
        tags=payload.get("tags", []),
    )


# 11. Analytics & ROI
@router.get("/analytics/{agent_id}", response_model=AgentAnalytics, tags=["Lifecycle Analytics"])
async def get_agent_analytics(agent_id: str):
    return orchestrator.analytics.get_agent_analytics(agent_id)


# 12. Retirement & Sunsetting
@router.post("/agents/{agent_id}/retire", response_model=AgentRetirementPlan, tags=["Retirement & Deprecation"])
async def schedule_agent_retirement(agent_id: str, payload: Dict[str, Any] = Body(...)):
    plan = orchestrator.retirement.schedule_retirement(
        agent_id=agent_id,
        deprecation_notice=payload.get("deprecation_notice", "Scheduled for retirement"),
        sunset_days=payload.get("sunset_days", 60),
        target_migration_agent_id=payload.get("target_migration_agent_id"),
    )
    orchestrator.registry.update_lifecycle_state(agent_id, AgentLifecycleState.DEPRECATED)
    return plan
