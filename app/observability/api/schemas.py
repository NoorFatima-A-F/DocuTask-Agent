"""Pydantic Request & Response Schemas for Observability & SRE APIs."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class LogQueryRequest(BaseModel):
    tenant_id: Optional[str] = None
    service: Optional[str] = None
    level: Optional[str] = None
    trace_id: Optional[str] = None
    query: Optional[str] = None
    limit: int = 100


class LogEntrySchema(BaseModel):
    timestamp: float
    service: str
    level: str
    message: str
    trace_id: str
    tenant_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AlertCreateRequest(BaseModel):
    rule_id: str
    name: str
    severity: str = "WARNING"
    metric_name: str
    operator: str = ">"
    threshold_value: float
    description: str = ""


class AlertResponseSchema(BaseModel):
    alert_id: str
    rule_id: str
    name: str
    severity: str
    state: str
    current_value: float
    threshold_value: float
    description: str
    acknowledged: bool


class AlertAcknowledgeRequest(BaseModel):
    acknowledged_by: str


class IncidentCreateRequest(BaseModel):
    title: str
    description: str
    severity: str = "SEV2_MAJOR"
    affected_services: List[str] = Field(default_factory=list)
    commander: Optional[str] = None


class IncidentResponseSchema(BaseModel):
    incident_id: str
    title: str
    severity: str
    status: str
    affected_services: List[str]
    commander: Optional[str] = None


class RCARequest(BaseModel):
    service_name: str
    metrics_snapshot: Dict[str, float] = Field(default_factory=dict)
    error_logs: List[str] = Field(default_factory=list)


class RCAResponse(BaseModel):
    analysis_id: str
    issue_summary: str
    primary_root_cause: str
    confidence_score: float
    mitigation_recommendation: str
