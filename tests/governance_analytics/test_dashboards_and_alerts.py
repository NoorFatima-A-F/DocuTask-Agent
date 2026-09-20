"""Tests for Multi-Role Dashboards (Executive, Admin, Developer) and Alert Detector."""

import pytest
from app.governance.analytics.warehouse.repositories import GovernanceDataWarehouseRepository
from app.governance.analytics.events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType
from app.governance.analytics.core.engine import GovernanceMetricsEngine
from app.governance.analytics.dashboards.services import DashboardService
from app.governance.analytics.alerts.detector import AlertDetector
from app.governance.analytics.alerts.rules import AlertRule, AlertSeverity


def test_multi_role_dashboards():
    repo = GovernanceDataWarehouseRepository()
    metrics = GovernanceMetricsEngine(repo)
    dash_service = DashboardService(metrics_engine=metrics)

    # Ingest event
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="tenant_dash",
            event_type=AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
            risk_score=0.1,
            is_success=True,
        )
    )

    # Executive Dashboard
    exec_dash = dash_service.get_executive_dashboard("tenant_dash")
    assert exec_dash.tenant_id == "tenant_dash"
    assert exec_dash.overall_governance_score >= 0.0

    # Administrator Dashboard
    admin_dash = dash_service.get_administrator_dashboard("tenant_dash")
    assert admin_dash.tenant_id == "tenant_dash"
    assert admin_dash.decisions.total_decisions == 1

    # Developer Dashboard
    dev_dash = dash_service.get_developer_dashboard("tenant_dash")
    assert dev_dash.tenant_id == "tenant_dash"


def test_alert_detector_trigger():
    repo = GovernanceDataWarehouseRepository()
    metrics = GovernanceMetricsEngine(repo)
    detector = AlertDetector(metrics_engine=metrics)

    # Add custom low threshold rule
    detector.add_rule(
        AlertRule(
            rule_id="test_rule",
            name="Test Low Risk Threshold",
            metric="overall_risk_score",
            operator=">=",
            threshold=0.0,
            severity=AlertSeverity.HIGH,
        )
    )

    alerts = detector.evaluate_alerts("tenant_dash")
    assert len(alerts) >= 1
    assert alerts[0].rule_id == "test_rule"
