"""FastAPI Request and Response Schemas for Governance Analytics."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from ..events.normalizers import GovernanceAnalyticsEvent
from ..reporting.templates import ReportType, ReportFormat


class IngestEventRequest(BaseModel):
    event: GovernanceAnalyticsEvent


class IngestBatchRequest(BaseModel):
    events: List[GovernanceAnalyticsEvent]


class OverviewResponse(BaseModel):
    tenant_id: str
    governance_score: float
    decisions: Dict[str, Any]
    risk_summary: Dict[str, Any]
    compliance_status: str


class GenerateReportRequest(BaseModel):
    tenant_id: str = "*"
    report_type: ReportType = ReportType.MONTHLY_EXECUTIVE
    title: Optional[str] = None
    export_format: ReportFormat = ReportFormat.JSON


class GenerateReportResponse(BaseModel):
    report_id: str
    export_format: ReportFormat
    content: str
