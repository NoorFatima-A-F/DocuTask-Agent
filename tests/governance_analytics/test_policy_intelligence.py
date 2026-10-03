"""Tests for Policy Intelligence, Coverage, and Effectiveness Engine."""

from app.governance.analytics.warehouse.repositories import GovernanceDataWarehouseRepository
from app.governance.analytics.events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType
from app.governance.analytics.policies.analytics import PolicyAnalyticsEngine
from app.governance.analytics.policies.effectiveness import PolicyEffectivenessEngine


def test_policy_intelligence_and_effectiveness():
    repo = GovernanceDataWarehouseRepository()
    analytics_engine = PolicyAnalyticsEngine(repo)
    eff_engine = PolicyEffectivenessEngine(repo)

    # Ingest decisions with policies
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="tenant_p",
            event_type=AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
            policy_id="pol_auth_gate",
            risk_score=0.1,
            is_success=True,
        )
    )
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="tenant_p",
            event_type=AnalyticsEventType.POLICY_VIOLATION,
            policy_id="pol_auth_gate",
            severity="HIGH",
        )
    )

    report = analytics_engine.generate_policy_intelligence("tenant_p")
    assert report.total_evaluations == 1
    assert report.total_violations == 1
    assert len(report.policy_usage_stats) >= 1

    eff_summary = eff_engine.evaluate_effectiveness("tenant_p")
    assert 0.0 <= eff_summary.overall_effectiveness_score <= 1.0
