"""Tests for Model Analytics, Cost Tracking, and Deprecation Management (Phase 8C)."""

import time
from app.model_governance.analytics.usage import ModelUsageTracker, UsageEvent
from app.model_governance.analytics.cost import ModelCostCalculator
from app.model_governance.analytics.performance import ModelPerformanceAnalyzer, PerformanceMetricSample
from app.model_governance.registry.models import Model, ModelCategory, ModelLifecycleState, ModelProvider
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.lifecycle.manager import ModelLifecycleManager
from app.model_governance.lifecycle.deprecation import ModelDeprecationManager, DeprecationPlan


def test_usage_and_cost_analytics():
    usage_tracker = ModelUsageTracker()
    cost_calc = ModelCostCalculator()

    model = Model(
        model_id="gpt-4o",
        model_name="GPT-4o",
        organization_id="org_test",
        family_id="gpt-4o",
        version="2024-08-06",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.OPENAI,
        input_token_cost_per_1k=0.005,
        output_token_cost_per_1k=0.015,
    )
    cost_calc.register_model_pricing(model)

    e1 = UsageEvent(
        event_id="evt-1",
        organization_id="org_test",
        model_id="gpt-4o",
        prompt_tokens=1000,
        completion_tokens=500,
    )
    e2 = UsageEvent(
        event_id="evt-2",
        organization_id="org_test",
        model_id="gpt-4o",
        prompt_tokens=2000,
        completion_tokens=1000,
    )

    usage_tracker.record_usage(e1)
    usage_tracker.record_usage(e2)

    summary = usage_tracker.get_summary("org_test", "gpt-4o")
    assert summary.total_requests == 2
    assert summary.total_prompt_tokens == 3000
    assert summary.total_completion_tokens == 1500
    assert summary.total_tokens == 4500

    cost_attr = cost_calc.calculate_total_spend([e1, e2], "org_test")
    # Prompt: 3k * 0.005 = 0.015; Completion: 1.5k * 0.015 = 0.0225; Total = 0.0375
    assert cost_attr.total_cost == 0.0375


def test_performance_percentiles_calculation():
    analyzer = ModelPerformanceAnalyzer()

    for lat in [10.0, 20.0, 30.0, 40.0, 50.0, 100.0, 200.0, 300.0, 500.0, 1000.0]:
        analyzer.record_sample(
            PerformanceMetricSample(
                model_id="claude-3-5-sonnet",
                organization_id="org_test",
                latency_ms=lat,
            )
        )

    report = analyzer.analyze("claude-3-5-sonnet")
    assert report.sample_count == 10
    assert report.p50_latency_ms > 0
    assert report.p95_latency_ms > report.p50_latency_ms
    assert report.p99_latency_ms >= report.p95_latency_ms


def test_model_deprecation_workflow():
    repo = ModelRegistryRepository()
    lifecycle = ModelLifecycleManager(repo)
    deprecation_mgr = ModelDeprecationManager(repo, lifecycle)

    model = Model(
        model_id="gpt-3.5-turbo-legacy",
        model_name="GPT 3.5 Turbo Legacy",
        organization_id="org_test",
        family_id="gpt-3.5",
        version="0613",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.OPENAI,
        lifecycle_state=ModelLifecycleState.ACTIVE,
    )
    repo.save_model(model)

    # Schedule deprecation
    plan = DeprecationPlan(
        model_id="gpt-3.5-turbo-legacy",
        organization_id="org_test",
        replacement_model_id="gpt-4o-mini",
        sunset_date=time.time() + 86400 * 30,
        reason="Model sunsetted by upstream vendor",
    )

    deprecation_mgr.schedule_deprecation(plan, actor="admin@test.com")

    updated = repo.get_model("gpt-3.5-turbo-legacy", "org_test")
    assert updated.lifecycle_state == ModelLifecycleState.DEPRECATED
    assert updated.replacement_model_id == "gpt-4o-mini"

    # Sunset model
    deprecation_mgr.execute_sunset("gpt-3.5-turbo-legacy", "org_test", actor="admin@test.com")
    retired = repo.get_model("gpt-3.5-turbo-legacy", "org_test")
    assert retired.lifecycle_state == ModelLifecycleState.RETIRED
