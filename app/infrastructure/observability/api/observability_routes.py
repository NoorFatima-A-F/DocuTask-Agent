"""
FastAPI REST Routes for Enterprise Observability, Telemetry & SRE.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.infrastructure.observability.alerts.models import AlertRule, AlertSeverity, RuleType
from app.infrastructure.observability.logs.models import LogLevel
from app.infrastructure.observability.metrics.types import MetricType
from app.infrastructure.observability.sdk.observability import ObservabilitySDK
from app.infrastructure.observability.slo.objectives import SLIType, SLOObjective

router = APIRouter(prefix="/api/v1/infrastructure/observability", tags=["Platform Observability & SRE"])

observability_sdk = ObservabilitySDK()


class MetricRecordRequest(BaseModel):
    name: str
    value: float
    metric_type: MetricType = MetricType.GAUGE
    labels: Dict[str, str] = Field(default_factory=dict)


class LogEmitRequest(BaseModel):
    level: LogLevel = LogLevel.INFO
    message: str
    attributes: Dict[str, Any] = Field(default_factory=dict)


# --- Metrics ---

@router.get("/metrics", response_model=List[Dict[str, Any]])
def get_metrics(prefix: Optional[str] = None) -> List[Dict[str, Any]]:
    series = observability_sdk.get_metrics(prefix=prefix)
    return [s.model_dump(mode="json") for s in series]


@router.post("/metrics/record", status_code=status.HTTP_201_CREATED)
def record_metric(req: MetricRecordRequest) -> Dict[str, Any]:
    observability_sdk.record_metric(
        name=req.name,
        value=req.value,
        metric_type=req.metric_type,
        labels=req.labels,
    )
    return {"status": "RECORDED", "metric": req.name, "value": req.value}


# --- Logs ---

@router.get("/logs", response_model=List[Dict[str, Any]])
def search_logs(
    tenant_id: Optional[str] = None,
    service_name: Optional[str] = None,
    trace_id: Optional[str] = None,
    level: Optional[LogLevel] = None,
    keyword: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    logs = observability_sdk.search_logs(
        tenant_id=tenant_id,
        service_name=service_name,
        trace_id=trace_id,
        level=level,
        keyword=keyword,
        limit=limit,
    )
    return [l.model_dump(mode="json") for l in logs]


@router.post("/logs", status_code=status.HTTP_201_CREATED)
def emit_log(req: LogEmitRequest) -> Dict[str, Any]:
    record = observability_sdk.log(level=req.level, message=req.message, **req.attributes)
    return record.model_dump(mode="json")


# --- Traces ---

@router.get("/traces/{trace_id}", response_model=Dict[str, Any])
def get_trace_analysis(trace_id: str) -> Dict[str, Any]:
    report = observability_sdk.analyze_trace(trace_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Trace '{trace_id}' not found.")
    return report.model_dump(mode="json")


# --- Alerts ---

@router.get("/alerts", response_model=List[Dict[str, Any]])
def list_alerts() -> List[Dict[str, Any]]:
    alerts = observability_sdk.alert_evaluator.list_active_alerts()
    return [a.model_dump(mode="json") for a in alerts]


@router.post("/alerts/rules", status_code=status.HTTP_201_CREATED)
def create_alert_rule(rule: AlertRule) -> Dict[str, Any]:
    observability_sdk.alert_evaluator.register_rule(rule)
    return rule.model_dump(mode="json")


# --- SLOs ---

@router.get("/slo", response_model=List[Dict[str, Any]])
def list_slos() -> List[Dict[str, Any]]:
    statuses = observability_sdk.error_budget_tracker.list_all_statuses()
    return [s.model_dump(mode="json") for s in statuses]


# --- Service Dependencies ---

@router.get("/dependencies", response_model=List[Dict[str, Any]])
def get_dependencies() -> List[Dict[str, Any]]:
    edges = observability_sdk.get_service_dependencies()
    return [e.model_dump(mode="json") for e in edges]


# --- Diagnostics & RCA ---

@router.get("/diagnostics/rca", response_model=Dict[str, Any])
def run_rca(trace_id: Optional[str] = None) -> Dict[str, Any]:
    report = observability_sdk.run_root_cause_analysis(trace_id=trace_id)
    return report.model_dump(mode="json")
