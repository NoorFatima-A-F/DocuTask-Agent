"""
FastAPI Routes for Enterprise Reliability, Health, Failover, and Incidents.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.infrastructure.failover.planner import FailoverScope, FailoverType
from app.infrastructure.health.probes import ProbeType
from app.infrastructure.incidents.models import IncidentStatus
from app.infrastructure.recovery.workflows import RecoveryWorkflow
from app.infrastructure.reliability.models import SeverityLevel
from app.infrastructure.sdk.reliability import ReliabilitySDK

router = APIRouter(prefix="/api/v1/infrastructure/reliability", tags=["Platform Reliability & DR"])

reliability_sdk = ReliabilitySDK()


class ProbeRegisterRequest(BaseModel):
    probe_id: str
    component_id: str
    probe_type: ProbeType = ProbeType.LIVENESS
    interval_seconds: float = 10.0
    timeout_seconds: float = 3.0


class FailoverPlanRequest(BaseModel):
    plan_id: str
    source_region: str
    target_region: str
    failover_type: FailoverType = FailoverType.AUTOMATIC
    scope: FailoverScope = FailoverScope.REGION
    affected_services: Optional[List[str]] = None
    reason: str = "Operator requested or threshold breach"


class FailoverExecuteRequest(BaseModel):
    plan_id: str


class IncidentCreateRequest(BaseModel):
    incident_id: str
    title: str
    severity: SeverityLevel = SeverityLevel.WARNING
    impacted_components: Optional[List[str]] = None
    lead_responder: Optional[str] = None


class IncidentTransitionRequest(BaseModel):
    target_status: IncidentStatus
    actor: str = "operator"
    message: str = ""


# --- Health & Probing Endpoints ---

@router.get("/health", response_model=Dict[str, Any])
def get_system_health() -> Dict[str, Any]:
    matrix = reliability_sdk.get_system_health()
    return matrix.model_dump(mode="json")


@router.get("/health/{component_id}", response_model=Dict[str, Any])
def get_component_health(component_id: str) -> Dict[str, Any]:
    score = reliability_sdk.get_component_health(component_id)
    return score.model_dump(mode="json")


@router.post("/probes/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def register_probe(req: ProbeRegisterRequest) -> Dict[str, Any]:
    probe = reliability_sdk.register_probe(
        probe_id=req.probe_id,
        component_id=req.component_id,
        probe_type=req.probe_type,
        interval_seconds=req.interval_seconds,
        timeout_seconds=req.timeout_seconds,
    )
    return {"status": "REGISTERED", "probe": probe.model_dump(mode="json")}


@router.post("/probes/{probe_id}/execute", response_model=Dict[str, Any])
def execute_probe(probe_id: str) -> Dict[str, Any]:
    try:
        result = reliability_sdk.execute_probe(probe_id)
        return result.model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Probe '{probe_id}' not found.")


# --- Failover Endpoints ---

@router.post("/failover/plan", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def plan_failover(req: FailoverPlanRequest) -> Dict[str, Any]:
    plan = reliability_sdk.plan_failover(
        plan_id=req.plan_id,
        source_region=req.source_region,
        target_region=req.target_region,
        failover_type=req.failover_type,
        scope=req.scope,
        affected_services=req.affected_services,
        reason=req.reason,
    )
    return plan.model_dump(mode="json")


@router.post("/failover/execute", response_model=Dict[str, Any])
def execute_failover(req: FailoverExecuteRequest) -> Dict[str, Any]:
    try:
        res = reliability_sdk.execute_failover(req.plan_id)
        return res.model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plan '{req.plan_id}' not found.")


@router.get("/failover/status/{plan_id}", response_model=Dict[str, Any])
def get_failover_status(plan_id: str) -> Dict[str, Any]:
    plan = reliability_sdk.failover_orchestrator.planner.get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Plan '{plan_id}' not found.")
    exec_result = reliability_sdk.failover_orchestrator.get_execution_result(plan_id)
    return {
        "plan": plan.model_dump(mode="json"),
        "execution": exec_result.model_dump(mode="json") if exec_result else None,
    }


# --- Recovery Endpoints ---

@router.post("/recovery/execute", response_model=Dict[str, Any])
def execute_recovery(workflow: RecoveryWorkflow) -> Dict[str, Any]:
    report = reliability_sdk.execute_recovery_workflow(workflow)
    return report.model_dump(mode="json")


# --- Incident Endpoints ---

@router.get("/incidents", response_model=List[Dict[str, Any]])
def list_incidents() -> List[Dict[str, Any]]:
    incidents = reliability_sdk.incident_manager.list_all_incidents()
    return [i.model_dump(mode="json") for i in incidents]


@router.post("/incidents", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def create_incident(req: IncidentCreateRequest) -> Dict[str, Any]:
    incident = reliability_sdk.create_incident(
        incident_id=req.incident_id,
        title=req.title,
        severity=req.severity,
        impacted_components=req.impacted_components,
        lead_responder=req.lead_responder,
    )
    return incident.model_dump(mode="json")


@router.post("/incidents/{incident_id}/transition", response_model=Dict[str, Any])
def transition_incident(incident_id: str, req: IncidentTransitionRequest) -> Dict[str, Any]:
    try:
        entry = reliability_sdk.incident_manager.transition_incident(
            incident_id=incident_id,
            target_status=req.target_status,
            actor=req.actor,
            message=req.message,
        )
        return entry.model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incident '{incident_id}' not found.")


# --- Replication Endpoints ---

@router.get("/replication/lag", response_model=List[Dict[str, Any]])
def get_replication_lag() -> List[Dict[str, Any]]:
    metrics = reliability_sdk.replication_manager.get_all_lag_metrics()
    return [m.model_dump(mode="json") for m in metrics]
