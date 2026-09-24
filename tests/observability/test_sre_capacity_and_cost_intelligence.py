"""Tests for Capacity Planning, Saturation Forecasting, and Cost Optimization."""

from app.observability.capacity.planner import CapacityPlanner
from app.observability.cost.analyzer import CostAnalyzer
from app.observability.cost.optimization import CostOptimizationEngine, RecommendationType


def test_capacity_planner_saturation_forecast():
    planner = CapacityPlanner(critical_days_threshold=7.0)

    # 1. Critical growth: 80GB used of 100GB, growing 5GB/day -> 4 days to saturation -> CRITICAL
    f_crit = planner.calculate_saturation(
        resource_name="disk_storage_gb",
        current_value=80.0,
        saturation_threshold=100.0,
        daily_growth_rate=5.0,
    )
    assert f_crit.is_critical is True
    assert f_crit.days_to_saturation == 4.0

    # 2. Healthy growth: 20GB used of 100GB, growing 1GB/day -> 80 days
    f_safe = planner.calculate_saturation(
        resource_name="disk_storage_gb",
        current_value=20.0,
        saturation_threshold=100.0,
        daily_growth_rate=1.0,
    )
    assert f_safe.is_critical is False
    assert f_safe.days_to_saturation == 80.0


def test_cost_analyzer_and_optimization_engine():
    analyzer = CostAnalyzer()
    cost = analyzer.calculate_cost(
        tenant_id="tenant-acme",
        cpu_hours=100.0,
        storage_gb=50.0,
        prompt_tokens=50000,
        completion_tokens=20000,
    )
    assert cost.compute_usd == 4.0
    assert cost.ai_tokens_usd > 0
    assert cost.total_cost_usd > 4.0

    # Cost optimizations
    optimizer = CostOptimizationEngine()
    recs = optimizer.evaluate_optimizations(
        cache_hit_rate_pct=15.0,
        idle_worker_hours=80.0,
        stale_documents_gb=200.0,
    )
    assert len(recs) == 3
    rec_types = [r.recommendation_type for r in recs]
    assert RecommendationType.SEMANTIC_CACHE in rec_types
    assert RecommendationType.RIGHTSIZE_WORKERS in rec_types
