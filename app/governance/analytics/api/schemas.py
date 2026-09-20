"""FastAPI Request and Response Schemas for Governance Analytics."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType
from ..reporting.templates import ReportType, ReportFormat, GovernanceReport
from ..dashboards.schemas import ExecutiveDashboardDTO, AdministratorDashboardDTO, DeveloperDashboardDTO
from ..risk.analyzer import RiskAnalysisSummary
from ..policies.analytics import PolicyIntelligenceReport
from ..ai_systems.agents import AgentSystemAnalytics
from ..ai_systems.models import ModelSystemAnalytics
from ..ai_systems.workflows import WorkflowSystemAnalytics
from ..alerts.detector import AlertEvent


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
