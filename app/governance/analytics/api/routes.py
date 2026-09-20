"""FastAPI REST API Routes for Enterprise Governance Analytics & Reporting."""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Query

from ..sdk.client import GovernanceAnalyticsSDK
from ..reporting.templates import ReportType, ReportFormat
from ..dashboards.schemas import ExecutiveDashboardDTO, AdministratorDashboardDTO, DeveloperDashboardDTO
from ..risk.analyzer import RiskAnalysisSummary
from ..policies.analytics import PolicyIntelligenceReport
from ..ai_systems.agents import AgentSystemAnalytics
from ..ai_systems.models import ModelSystemAnalytics
from ..ai_systems.workflows import WorkflowSystemAnalytics
from ..alerts.detector import AlertEvent
from .schemas import (
    IngestEventRequest,
    IngestBatchRequest,
    OverviewResponse,
    GenerateReportRequest,
    GenerateReportResponse,
)

router = APIRouter(prefix="/api/v1/governance/analytics", tags=["Governance Analytics & Intelligence"])

_sdk: Optional[GovernanceAnalyticsSDK] = None


def get_sdk() -> GovernanceAnalyticsSDK:
    global _sdk
    if _sdk is None:
        _sdk = GovernanceAnalyticsSDK()
    return _sdk


@router.post("/events", status_code=status.HTTP_201_CREATED)
def ingest_event(
    payload: IngestEventRequest,
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Ingests a normalized governance event into the analytics pipeline."""
    return sdk.ingest_event(payload.event)


@router.post("/events/batch", status_code=status.HTTP_201_CREATED)
def ingest_batch_events(
    payload: IngestBatchRequest,
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Ingests a batch of normalized governance events."""
    return [sdk.ingest_event(e) for e in payload.events]


@router.get("/overview", response_model=OverviewResponse)
def get_overview(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
) -> OverviewResponse:
    """Returns high-level governance health score and intelligence summary."""
    data = sdk.get_overview(tenant_id=tenant_id)
    return OverviewResponse(**data)


@router.get("/risk", response_model=RiskAnalysisSummary)
def get_risk_analytics(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Returns multi-category risk posture, scores, and detected anomalies."""
    return sdk.get_risk_posture(tenant_id=tenant_id)


@router.get("/policies", response_model=PolicyIntelligenceReport)
def get_policy_analytics(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Returns policy usage, violations, and friction metrics."""
    return sdk.get_policy_intelligence(tenant_id=tenant_id)


@router.get("/systems/agents", response_model=AgentSystemAnalytics)
def get_agent_analytics(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Returns agent workforce execution, reliability, and risk telemetry."""
    return sdk.agent_analytics.analyze_agents(tenant_id=tenant_id)


@router.get("/systems/models", response_model=ModelSystemAnalytics)
def get_model_analytics(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Returns foundation model usage, latency, cost, and drift signals."""
    return sdk.model_analytics.analyze_models(tenant_id=tenant_id)


@router.get("/systems/workflows", response_model=WorkflowSystemAnalytics)
def get_workflow_analytics(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Returns workflow execution and governance delay analytics."""
    return sdk.workflow_analytics.analyze_workflows(tenant_id=tenant_id)


@router.get("/dashboards/executive", response_model=ExecutiveDashboardDTO)
def get_executive_dashboard(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Returns the Executive Governance & Strategic Risk Dashboard."""
    return sdk.get_executive_dashboard(tenant_id=tenant_id)


@router.get("/dashboards/admin", response_model=AdministratorDashboardDTO)
def get_administrator_dashboard(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Returns the Security & Compliance Administrator Dashboard."""
    return sdk.get_admin_dashboard(tenant_id=tenant_id)


@router.get("/dashboards/developer", response_model=DeveloperDashboardDTO)
def get_developer_dashboard(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Returns the AI Engineer & Developer Performance Dashboard."""
    return sdk.get_developer_dashboard(tenant_id=tenant_id)


@router.post("/reports/generate", response_model=GenerateReportResponse)
def generate_report(
    payload: GenerateReportRequest,
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Generates and exports an automated governance report."""
    rep = sdk.reports.generate_report(
        report_type=payload.report_type,
        tenant_id=payload.tenant_id,
        title=payload.title,
    )
    from ..reporting.exporters import ReportExporter
    content = ReportExporter.export(rep, format=payload.export_format)
    return GenerateReportResponse(
        report_id=rep.report_id,
        export_format=payload.export_format,
        content=content,
    )


@router.get("/alerts", response_model=List[AlertEvent])
def evaluate_alerts(
    tenant_id: str = Query("*"),
    sdk: GovernanceAnalyticsSDK = Depends(get_sdk),
):
    """Evaluates real-time governance alert rules."""
    return sdk.evaluate_alerts(tenant_id=tenant_id)
