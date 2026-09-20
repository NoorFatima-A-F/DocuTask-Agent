"""FastAPI REST API Routes for Observability, SRE & Operational Intelligence."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from .schemas import (
    AlertAcknowledgeRequest,
    AlertCreateRequest,
    AlertResponseSchema,
    IncidentCreateRequest,
    IncidentResponseSchema,
    LogEntrySchema,
    LogQueryRequest,
    RCARequest,
    RCAResponse,
)
from ..alerts.rules import AlertRule, AlertSeverity, RuleConditionType
from ..incidents.manager import IncidentSeverity, IncidentStatus
from ..sdk.client import ObservabilitySDK

router = APIRouter(prefix="/observability", tags=["Observability & SRE Platform"])
observability_router = router

_global_sdk: Optional[ObservabilitySDK] = None


def get_observability_sdk() -> ObservabilitySDK:
    global _global_sdk
    if _global_sdk is None:
        _global_sdk = ObservabilitySDK(service_name="api-gateway")
    return _global_sdk


@router.get("/metrics")
def get_metrics_snapshot(sdk: ObservabilitySDK = Depends(get_observability_sdk)):
    return sdk.metric_registry.dump_snapshot()


@router.post("/logs/search", response_model=List[LogEntrySchema])
def search_logs(
    req: LogQueryRequest,
    sdk: ObservabilitySDK = Depends(get_observability_sdk),
):
    entries = sdk.log_storage.search(
        tenant_id=req.tenant_id,
        service=req.service,
        level=req.level,
        trace_id=req.trace_id,
        query=req.query,
        limit=req.limit,
    )
    return [
        LogEntrySchema(
            timestamp=e.timestamp,
            service=e.service,
            level=e.level,
            message=e.message,
            trace_id=e.trace_id,
            tenant_id=e.tenant_id,
            metadata=e.record_dict.get("metadata", {}),
        )
        for e in entries
    ]


@router.get("/traces/{trace_id}")
def get_trace_by_id(
    trace_id: str,
    sdk: ObservabilitySDK = Depends(get_observability_sdk),
):
    spans = sdk.tracer.get_trace(trace_id)
    if not spans:
        raise HTTPException(status_code=404, detail=f"Trace {trace_id} not found")
    return [
        {
            "span_id": s.context.span_id,
            "trace_id": s.context.trace_id,
            "name": s.name,
            "parent_span_id": s.parent_span_id,
            "kind": s.kind.value,
            "duration_ms": s.duration_ms,
            "status": s.status.value,
            "attributes": s.attributes,
        }
        for s in spans
    ]


@router.get("/alerts", response_model=List[AlertResponseSchema])
def list_alerts(sdk: ObservabilitySDK = Depends(get_observability_sdk)):
    alerts = sdk.alert_engine.list_active_alerts()
    return [
        AlertResponseSchema(
            alert_id=a.alert_id,
            rule_id=a.rule_id,
            name=a.name,
            severity=a.severity.value,
            state=a.state.value,
            current_value=a.current_value,
            threshold_value=a.threshold_value,
            description=a.description,
            acknowledged=a.acknowledged,
        )
        for a in alerts
    ]


@router.post("/alerts/rules")
def create_alert_rule(
    req: AlertCreateRequest,
    sdk: ObservabilitySDK = Depends(get_observability_sdk),
):
    rule = AlertRule(
        rule_id=req.rule_id,
        name=req.name,
        severity=AlertSeverity(req.severity.upper()),
        condition_type=RuleConditionType.METRIC_THRESHOLD,
        metric_name=req.metric_name,
        operator=req.operator,
        threshold_value=req.threshold_value,
        description=req.description,
    )
    sdk.alert_engine.add_rule(rule)
    return {"rule_id": rule.rule_id, "status": "created"}


@router.post("/alerts/{alert_id}/acknowledge")
def acknowledge_alert(
    alert_id: str,
    req: AlertAcknowledgeRequest,
    sdk: ObservabilitySDK = Depends(get_observability_sdk),
):
    ok = sdk.alert_engine.acknowledge_alert(alert_id, req.acknowledged_by)
    if not ok:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "acknowledged", "alert_id": alert_id}


@router.get("/incidents", response_model=List[IncidentResponseSchema])
def list_incidents(sdk: ObservabilitySDK = Depends(get_observability_sdk)):
    incidents = sdk.incident_manager.list_incidents()
    return [
        IncidentResponseSchema(
            incident_id=i.incident_id,
            title=i.title,
            severity=i.severity.value,
            status=i.status.value,
            affected_services=i.affected_services,
            commander=i.commander,
        )
        for i in incidents
    ]


@router.post("/incidents", response_model=IncidentResponseSchema)
def create_incident(
    req: IncidentCreateRequest,
    sdk: ObservabilitySDK = Depends(get_observability_sdk),
):
    inc = sdk.incident_manager.create_incident(
        title=req.title,
        description=req.description,
        severity=IncidentSeverity(req.severity.upper()),
        affected_services=req.affected_services,
    )
    if req.commander:
        sdk.incident_manager.assign_commander(inc.incident_id, req.commander, "API")

    return IncidentResponseSchema(
        incident_id=inc.incident_id,
        title=inc.title,
        severity=inc.severity.value,
        status=inc.status.value,
        affected_services=inc.affected_services,
        commander=inc.commander,
    )


@router.get("/dashboards/{dashboard_id}")
def get_dashboard_data(
    dashboard_id: str,
    sdk: ObservabilitySDK = Depends(get_observability_sdk),
):
    data = sdk.dashboard_engine.render_dashboard_data(dashboard_id)
    if not data:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return data


@router.post("/rca", response_model=RCAResponse)
def perform_rca(
    req: RCARequest,
    sdk: ObservabilitySDK = Depends(get_observability_sdk),
):
    result = sdk.rca_engine.analyze_incident(
        service_name=req.service_name,
        metrics_snapshot=req.metrics_snapshot,
        error_logs=req.error_logs,
    )
    return RCAResponse(
        analysis_id=result.analysis_id,
        issue_summary=result.issue_summary,
        primary_root_cause=result.primary_root_cause,
        confidence_score=result.confidence_score,
        mitigation_recommendation=result.mitigation_recommendation,
    )
