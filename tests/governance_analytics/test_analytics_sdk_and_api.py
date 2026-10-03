"""Tests for Governance Analytics Developer SDK and FastAPI REST Routes."""

from app.governance.analytics.sdk.client import GovernanceAnalyticsSDK
from app.governance.analytics.events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType
from app.governance.analytics.reporting.templates import ReportType, ReportFormat
from app.governance.analytics.api.routes import (
    ingest_event,
    get_overview,
    get_risk_analytics,
    get_policy_analytics,
    get_agent_analytics,
    get_model_analytics,
    get_workflow_analytics,
    get_executive_dashboard,
    get_administrator_dashboard,
    get_developer_dashboard,
    generate_report,
    evaluate_alerts,
)
from app.governance.analytics.api.schemas import (
    IngestEventRequest,
    GenerateReportRequest,
)


def test_governance_analytics_sdk_end_to_end():
    sdk = GovernanceAnalyticsSDK()

    # 1. Ingest Events
    sdk.ingest_event({
        "event_type": "GovernanceDecisionCreated",
        "tenant_id": "tenant_sdk_test",
        "risk_score": 0.25,
        "is_success": True,
    })
    sdk.ingest_event({
        "event_type": "PolicyViolation",
        "tenant_id": "tenant_sdk_test",
        "policy_id": "pol_safety_1",
        "severity": "HIGH",
    })
    sdk.ingest_event({
        "event_type": "ModelInvocation",
        "tenant_id": "tenant_sdk_test",
        "model_id": "gemini-1.5-pro",
        "cost_usd": 0.004,
        "latency_ms": 320.0,
    })

    # 2. Get Overview
    overview = sdk.get_overview("tenant_sdk_test")
    assert overview["tenant_id"] == "tenant_sdk_test"
    assert "governance_score" in overview

    # 3. Get Dashboards
    exec_dash = sdk.get_executive_dashboard("tenant_sdk_test")
    assert exec_dash.overall_governance_score >= 0.0

    admin_dash = sdk.get_admin_dashboard("tenant_sdk_test")
    assert admin_dash.total_policy_violations == 1

    dev_dash = sdk.get_developer_dashboard("tenant_sdk_test")
    assert dev_dash.models.total_model_invocations == 1

    # 4. Generate Report
    rep_content = sdk.generate_report(
        report_type=ReportType.MONTHLY_EXECUTIVE,
        tenant_id="tenant_sdk_test",
        export_format=ReportFormat.JSON,
    )
    assert "report_id" in rep_content

    # 5. Evaluate Alerts
    alerts = sdk.evaluate_alerts("tenant_sdk_test")
    assert isinstance(alerts, list)


def test_fastapi_rest_endpoints():
    sdk = GovernanceAnalyticsSDK()

    # Ingest event endpoint
    ev = GovernanceAnalyticsEvent(
        tenant_id="tenant_api_test",
        event_type=AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
        risk_score=0.1,
    )
    res_in = ingest_event(IngestEventRequest(event=ev), sdk=sdk)
    assert res_in.tenant_id == "tenant_api_test"

    # Overview endpoint
    res_overview = get_overview(tenant_id="tenant_api_test", sdk=sdk)
    assert res_overview.tenant_id == "tenant_api_test"

    # Risk endpoint
    res_risk = get_risk_analytics(tenant_id="tenant_api_test", sdk=sdk)
    assert res_risk.tenant_id == "tenant_api_test"

    # Policies endpoint
    res_pol = get_policy_analytics(tenant_id="tenant_api_test", sdk=sdk)
    assert res_pol.tenant_id == "tenant_api_test"

    # System endpoints
    res_agents = get_agent_analytics(tenant_id="tenant_api_test", sdk=sdk)
    assert res_agents.tenant_id == "tenant_api_test"

    res_models = get_model_analytics(tenant_id="tenant_api_test", sdk=sdk)
    assert res_models.tenant_id == "tenant_api_test"

    res_wfs = get_workflow_analytics(tenant_id="tenant_api_test", sdk=sdk)
    assert res_wfs.tenant_id == "tenant_api_test"

    # Dashboard endpoints
    res_exec = get_executive_dashboard(tenant_id="tenant_api_test", sdk=sdk)
    assert res_exec.tenant_id == "tenant_api_test"

    res_admin = get_administrator_dashboard(tenant_id="tenant_api_test", sdk=sdk)
    assert res_admin.tenant_id == "tenant_api_test"

    res_dev = get_developer_dashboard(tenant_id="tenant_api_test", sdk=sdk)
    assert res_dev.tenant_id == "tenant_api_test"

    # Report generation endpoint
    rep_req = GenerateReportRequest(
        tenant_id="tenant_api_test",
        report_type=ReportType.DAILY_OPERATIONAL,
        export_format=ReportFormat.JSON,
    )
    res_rep = generate_report(rep_req, sdk=sdk)
    assert res_rep.report_id.startswith("rep_")
    assert "report_id" in res_rep.content

    # Alerts endpoint
    res_alerts = evaluate_alerts(tenant_id="tenant_api_test", sdk=sdk)
    assert isinstance(res_alerts, list)
