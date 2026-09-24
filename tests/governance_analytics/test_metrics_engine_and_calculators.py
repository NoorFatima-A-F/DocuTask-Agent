"""Tests for Metrics Engine, Calculators, and Governance Health Score."""

from app.governance.analytics.warehouse.repositories import GovernanceDataWarehouseRepository
from app.governance.analytics.events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType
from app.governance.analytics.core.engine import GovernanceMetricsEngine
from app.governance.analytics.core.aggregators import TimeSeriesAggregator
from app.governance.analytics.core.metrics import MetricTrend


def test_metrics_engine_calculations():
    repo = GovernanceDataWarehouseRepository()
    engine = GovernanceMetricsEngine(repo)

    # Ingest decisions
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="tenant_1",
            event_type=AnalyticsEventType.GOVERNANCE_DECISION_CREATED,
            is_success=True,
            risk_score=0.1,
        )
    )
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="tenant_1",
            event_type=AnalyticsEventType.ACCESS_DENIED,
            is_success=False,
            risk_score=0.9,
        )
    )

    # Ingest model executions
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="tenant_1",
            event_type=AnalyticsEventType.MODEL_INVOCATION,
            model_id="gemini-1.5-pro",
            cost_usd=0.01,
            latency_ms=250.0,
            is_success=True,
            risk_score=0.1,
        )
    )

    dec_metrics = engine.get_decision_metrics("tenant_1")
    assert dec_metrics.total_decisions == 2
    assert dec_metrics.allowed_decisions == 1
    assert dec_metrics.denied_decisions == 1
    assert dec_metrics.allow_rate == 0.5

    model_metrics = engine.get_model_metrics("tenant_1")
    assert model_metrics.total_model_invocations == 1
    assert model_metrics.total_cost_usd == 0.01

    gov_score = engine.calculate_governance_score("tenant_1")
    assert 0.0 <= gov_score <= 100.0


def test_time_series_aggregator_period_comparison():
    change_pct, trend = TimeSeriesAggregator.compare_periods(
        current_val=15.0, previous_val=10.0, is_lower_better=True
    )
    assert change_pct == 50.0
    assert trend == MetricTrend.CRITICAL_SPIKE

    change_pct2, trend2 = TimeSeriesAggregator.compare_periods(
        current_val=95.0, previous_val=90.0, is_lower_better=False
    )
    assert change_pct2 > 0
    assert trend2 == MetricTrend.IMPROVING
