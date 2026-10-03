"""Tests for Governance Data Warehouse Models, Fact Tables, and Repositories."""

from app.governance.analytics.warehouse.repositories import GovernanceDataWarehouseRepository
from app.governance.analytics.warehouse.schemas import WarehouseQueryFilter
from app.governance.analytics.events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType


def test_warehouse_event_routing():
    repo = GovernanceDataWarehouseRepository()

    # 1. Decision event
    ev_dec = GovernanceAnalyticsEvent(
        tenant_id="tenant_x",
        event_type=AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
        user_id="usr_alice",
        policy_id="pol_auth",
        risk_score=0.2,
        is_success=True,
    )
    repo.insert_event(ev_dec)
    assert len(repo.fact_decisions) == 1
    assert "tenant_x" in repo.dim_tenants
    assert "usr_alice" in repo.dim_users

    # 2. Policy violation event
    ev_pol = GovernanceAnalyticsEvent(
        tenant_id="tenant_x",
        event_type=AnalyticsEventType.POLICY_VIOLATION,
        policy_id="pol_pii",
        severity="HIGH",
    )
    repo.insert_event(ev_pol)
    assert len(repo.fact_policies) == 1

    # 3. Model execution event
    ev_model = GovernanceAnalyticsEvent(
        tenant_id="tenant_x",
        event_type=AnalyticsEventType.MODEL_INVOCATION,
        model_id="gemini-1.5-flash",
        cost_usd=0.001,
        latency_ms=350.0,
    )
    repo.insert_event(ev_model)
    assert len(repo.fact_ai_executions) == 1
    assert "gemini-1.5-flash" in repo.dim_models

    # 4. Risk event
    ev_risk = GovernanceAnalyticsEvent(
        tenant_id="tenant_x",
        event_type=AnalyticsEventType.RISK_DETECTED,
        risk_score=0.88,
        metadata={"risk_category": "Security Risk"},
    )
    repo.insert_event(ev_risk)
    assert len(repo.fact_risk_events) == 1


def test_warehouse_queries_and_filters():
    repo = GovernanceDataWarehouseRepository()
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="t1",
            event_type=AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
            risk_score=0.1,
        )
    )
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="t2",
            event_type=AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
            risk_score=0.2,
        )
    )

    q1 = WarehouseQueryFilter(tenant_id="t1")
    res1 = repo.query_decisions(q1)
    assert len(res1) == 1
    assert res1[0].tenant_id == "t1"

    q_all = WarehouseQueryFilter(tenant_id="*")
    res_all = repo.query_decisions(q_all)
    assert len(res_all) == 2
