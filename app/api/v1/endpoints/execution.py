"""
Phase 13.15: Execution Platform REST Endpoints (ARWE-UTOCOP).
Provides full management, orchestration, simulation, execution, verification, and audit APIs.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.runtime.execution.events import (
    ConnectorCategory,
    CredentialType,
    RiskLevel,
    ToolType,
)
from app.runtime.execution.runtime.execution_runtime import execution_runtime
from app.runtime.execution.tool_registry.tool_registry_engine import ToolDefinition, ToolParameter
from app.runtime.execution.connectors.connector_engine import ConnectorConfig

router = APIRouter()


# Request Models
class GoalExecutionRequest(BaseModel):
    goal: str = Field(..., description="High-level natural language mission directive")
    dry_run: bool = Field(False, description="Whether to simulate only without external mutations")
    initiated_by: str = Field("autonomous_executive", description="Agent/User identity requesting execution")


class ToolRegistrationRequest(BaseModel):
    tool_id: str
    name: str
    version: str = "1.0.0"
    description: str
    tool_type: str = "saas"
    category: str = "custom_api"
    risk_level: str = "low"
    rate_limit_per_min: int = 60
    timeout_seconds: int = 30
    is_idempotent: bool = True
    supports_compensation: bool = True
    compensation_tool_id: Optional[str] = None
    parameters: List[Dict[str, Any]] = []
    output_schema: Dict[str, Any] = {}
    tags: List[str] = []


class ConnectorCreateRequest(BaseModel):
    connector_id: str
    name: str
    category: str
    protocol: str
    endpoint_url: str
    credential_id: Optional[str] = None
    metadata: Dict[str, Any] = {}


class BrowserActionRequest(BaseModel):
    action_type: str
    selector: Optional[str] = None
    value: Optional[str] = None


class PlanMissionRequest(BaseModel):
    mission_goal: str
    target_tools: Optional[List[str]] = None


class CredentialCreateRequest(BaseModel):
    name: str
    cred_type: str
    target_system: str
    raw_secret: str
    scopes: List[str] = []


class ApprovalResolveRequest(BaseModel):
    approved: bool
    approver: str = "executive_lead"


class SimulateWorkflowRequest(BaseModel):
    workflow_id: str


# Endpoints
@router.get("/overview")
def get_platform_overview() -> Dict[str, Any]:
    """Retrieve top-level operational and health summary of the execution platform."""
    return execution_runtime.get_executive_overview()


# Tool Registry
@router.get("/tools")
def list_tools(
    category: Optional[str] = None,
    tool_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    search: Optional[str] = None,
) -> Dict[str, Any]:
    tools = execution_runtime.tool_registry.list_tools(
        category=category, tool_type=tool_type, risk_level=risk_level, search=search
    )
    return {"tools": [t.to_dict() for t in tools], "total": len(tools)}


@router.post("/tools")
def register_tool(req: ToolRegistrationRequest) -> Dict[str, Any]:
    try:
        t_type = ToolType(req.tool_type)
    except ValueError:
        t_type = ToolType.CUSTOM

    try:
        r_level = RiskLevel(req.risk_level)
    except ValueError:
        r_level = RiskLevel.LOW

    params = [
        ToolParameter(
            name=p.get("name", "param"),
            param_type=p.get("param_type", "string"),
            description=p.get("description", ""),
            required=p.get("required", True),
            default=p.get("default"),
            enum_values=p.get("enum_values"),
        )
        for p in req.parameters
    ]

    t_def = ToolDefinition(
        tool_id=req.tool_id,
        name=req.name,
        version=req.version,
        description=req.description,
        tool_type=t_type,
        category=req.category,
        risk_level=r_level,
        rate_limit_per_min=req.rate_limit_per_min,
        timeout_seconds=req.timeout_seconds,
        is_idempotent=req.is_idempotent,
        supports_compensation=req.supports_compensation,
        compensation_tool_id=req.compensation_tool_id,
        parameters=params,
        output_schema=req.output_schema,
        tags=req.tags,
    )
    registered = execution_runtime.tool_registry.register_tool(t_def)
    return {"success": True, "tool": registered.to_dict()}


@router.get("/tools/{tool_id}")
def get_tool_details(tool_id: str) -> Dict[str, Any]:
    t = execution_runtime.tool_registry.get_tool(tool_id)
    if not t:
        raise HTTPException(status_code=404, detail=f"Tool {tool_id} not found")
    return {"tool": t.to_dict()}


# Connectors
@router.get("/connectors")
def list_connectors(category: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
    connectors = execution_runtime.connectors.list_connectors(category=category, status=status)
    return {"connectors": [c.to_dict() for c in connectors], "total": len(connectors)}


@router.post("/connectors")
def create_connector(req: ConnectorCreateRequest) -> Dict[str, Any]:
    try:
        cat = ConnectorCategory(req.category)
    except ValueError:
        cat = ConnectorCategory.CUSTOM_API

    config = ConnectorConfig(
        connector_id=req.connector_id,
        name=req.name,
        category=cat,
        protocol=req.protocol,
        endpoint_url=req.endpoint_url,
        credential_id=req.credential_id,
        metadata=req.metadata,
    )
    res = execution_runtime.connectors.create_connector(config)
    return {"success": True, "connector": res.to_dict()}


@router.post("/connectors/{connector_id}/test")
def test_connector(connector_id: str) -> Dict[str, Any]:
    res = execution_runtime.connectors.test_connection(connector_id)
    if not res.get("success"):
        raise HTTPException(status_code=404, detail=res.get("error", "Connection test failed"))
    return res


# Browser Automation
@router.get("/browser/sessions")
def list_browser_sessions() -> Dict[str, Any]:
    sessions = execution_runtime.browser.list_sessions()
    return {"sessions": [s.to_dict() for s in sessions], "total": len(sessions)}


@router.post("/browser/sessions")
def create_browser_session() -> Dict[str, Any]:
    s = execution_runtime.browser.create_session()
    return {"session": s.to_dict()}


@router.post("/browser/sessions/{session_id}/actions")
def execute_browser_action(session_id: str, req: BrowserActionRequest) -> Dict[str, Any]:
    res = execution_runtime.browser.execute_action(
        session_id=session_id,
        action_type=req.action_type,
        selector=req.selector,
        value=req.value,
    )
    return res


# Workflows
@router.get("/workflows")
def list_workflows() -> Dict[str, Any]:
    workflows = execution_runtime.workflow.list_workflows()
    return {"workflows": [w.to_dict() for w in workflows], "total": len(workflows)}


@router.get("/workflows/{workflow_id}")
def get_workflow_details(workflow_id: str) -> Dict[str, Any]:
    w = execution_runtime.workflow.get_workflow(workflow_id)
    if not w:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
    return {"workflow": w.to_dict(), "tiers": w.get_execution_order()}


# Planner
@router.post("/planner/plan")
def plan_mission_goal(req: PlanMissionRequest) -> Dict[str, Any]:
    wf, plan = execution_runtime.planner.plan_mission(req.mission_goal, req.target_tools)
    execution_runtime.workflow.register_workflow(wf)
    return {"workflow": wf.to_dict(), "plan": plan.to_dict()}


@router.get("/planner/plans")
def list_execution_plans() -> Dict[str, Any]:
    plans = execution_runtime.planner.list_plans()
    return {"plans": [p.to_dict() for p in plans], "total": len(plans)}


# Credentials
@router.get("/credentials")
def list_credentials() -> Dict[str, Any]:
    creds = execution_runtime.credentials.list_credentials()
    return {"credentials": [c.to_dict() for c in creds], "total": len(creds)}


@router.post("/credentials")
def add_credential(req: CredentialCreateRequest) -> Dict[str, Any]:
    try:
        ctype = CredentialType(req.cred_type)
    except ValueError:
        ctype = CredentialType.API_KEY

    rec = execution_runtime.credentials.add_credential(
        name=req.name,
        cred_type=ctype,
        target_system=req.target_system,
        raw_secret=req.raw_secret,
        scopes=req.scopes,
    )
    return {"success": True, "credential": rec.to_dict()}


# Policy & Governance
@router.get("/policies/rules")
def list_policy_rules() -> Dict[str, Any]:
    rules = execution_runtime.policy.list_rules()
    return {"rules": [r.to_dict() for r in rules], "total": len(rules)}


@router.get("/policies/approvals")
def list_policy_approvals(status: Optional[str] = None) -> Dict[str, Any]:
    approvals = execution_runtime.policy.list_approvals(status=status)
    return {"approvals": [a.to_dict() for a in approvals], "total": len(approvals)}


@router.post("/policies/approvals/{approval_id}/resolve")
def resolve_policy_approval(approval_id: str, req: ApprovalResolveRequest) -> Dict[str, Any]:
    res = execution_runtime.policy.resolve_approval(approval_id, approved=req.approved, approver=req.approver)
    if not res:
        raise HTTPException(status_code=404, detail=f"Approval request {approval_id} not found")
    return {"success": True, "approval": res.to_dict()}


# Simulation
@router.post("/simulation/simulate")
def simulate_workflow_execution(req: SimulateWorkflowRequest) -> Dict[str, Any]:
    wf = execution_runtime.workflow.get_workflow(req.workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail=f"Workflow {req.workflow_id} not found")
    report = execution_runtime.simulation.simulate_workflow(wf)
    return {"simulation": report.to_dict()}


# Missions & Execution
@router.post("/missions/execute-goal")
def execute_natural_language_goal(req: GoalExecutionRequest) -> Dict[str, Any]:
    """Autonomous one-shot Goal -> CPM Plan -> Simulation -> Invariant Check -> Execution."""
    res = execution_runtime.execute_goal_end_to_end(
        goal=req.goal,
        dry_run=req.dry_run,
        initiated_by=req.initiated_by,
    )
    return res


@router.get("/missions")
def list_missions(status: Optional[str] = None) -> Dict[str, Any]:
    missions = execution_runtime.execution.list_missions(status=status)
    return {"missions": [m.to_dict() for m in missions], "total": len(missions)}


@router.get("/missions/{mission_id}")
def get_mission_details(mission_id: str) -> Dict[str, Any]:
    m = execution_runtime.execution.get_mission(mission_id)
    if not m:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} not found")
    return {"mission": m.to_dict()}


@router.post("/missions/{mission_id}/run")
def run_existing_mission(mission_id: str, dry_run: bool = False) -> Dict[str, Any]:
    try:
        res = execution_runtime.execution.execute_mission(mission_id, dry_run=dry_run)
        return {"mission": res.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Verification & Rollback
@router.get("/verifications")
def list_verifications(mission_id: Optional[str] = None) -> Dict[str, Any]:
    certs = execution_runtime.verification_engine.list_certificates(mission_id) if hasattr(execution_runtime, 'verification_engine') and execution_runtime.verification_engine else []
    if not certs:
        from app.runtime.execution.verification.verification_engine import verification_engine
        certs = verification_engine.list_certificates(mission_id)
    return {"certificates": [c.to_dict() for c in certs], "total": len(certs)}


@router.get("/rollbacks")
def list_rollbacks(mission_id: Optional[str] = None) -> Dict[str, Any]:
    rollbacks = execution_runtime.rollback.list_rollbacks(mission_id=mission_id)
    return {"rollbacks": [r.to_dict() for r in rollbacks], "total": len(rollbacks)}


# Monitoring & Audit
@router.get("/monitoring/telemetry")
def get_system_telemetry() -> Dict[str, Any]:
    snap = execution_runtime.monitoring.get_telemetry_snapshot()
    return {"telemetry": snap.to_dict()}


@router.get("/monitoring/alerts")
def list_monitoring_alerts(resolved: Optional[bool] = None) -> Dict[str, Any]:
    alerts = execution_runtime.monitoring.list_alerts(resolved=resolved)
    return {"alerts": [a.to_dict() for a in alerts], "total": len(alerts)}


@router.post("/monitoring/alerts/{alert_id}/resolve")
def resolve_monitoring_alert(alert_id: str) -> Dict[str, Any]:
    success = execution_runtime.monitoring.resolve_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    return {"success": True, "alert_id": alert_id}


@router.get("/audit/entries")
def list_audit_entries(mission_id: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
    entries = execution_runtime.audit.list_entries(mission_id=mission_id, limit=limit)
    return {"entries": [e.to_dict() for e in entries], "total": len(entries)}


@router.get("/audit/verify")
def verify_audit_ledger() -> Dict[str, Any]:
    valid, err = execution_runtime.audit.verify_ledger_integrity()
    return {"ledger_valid": valid, "error": err}
