"""
Test Suite: Cost & Energy Intelligence Accounting
Validates token cost models, prompt cache discounts, carbon footprints, and budget governor threshold enforcement.
"""
from app.runtime.cost_intelligence.cost_calculator import CostCalculator
from app.runtime.cost_intelligence.cost_aggregator import CostAggregator
from app.runtime.cost_intelligence.budget_governor import BudgetGovernor


def test_step_cost_calculation_with_prompt_cache():
    # Gemini 2.5 Flash: input $0.075 / 1M, cached input $0.01875 / 1M, output $0.30 / 1M
    breakdown = CostCalculator.calculate_step_cost(
        model_id="gemini-2.5-flash",
        input_tokens=2_000_000,
        output_tokens=1_000_000,
        cached_tokens=1_000_000,
        api_overhead_usd=0.001,
    )

    # 1M uncached input = $0.075, 1M cached input = $0.01875 -> input total = $0.09375
    # 1M output = $0.30
    # Net cost = 0.09375 + 0.30 + 0.001 = 0.39475
    assert round(breakdown.net_cost_usd, 5) == 0.39475
    assert breakdown.cached_cost_discount_usd > 0.05
    assert breakdown.energy_kwh > 0.0
    assert breakdown.co2_grams > 0.0


def test_cost_aggregator_mission_report():
    report = CostAggregator.get_canonical_mission_cost("mission_cost_001")
    
    assert report.mission_id == "mission_cost_001"
    assert report.total_net_cost_usd > 0.0
    assert report.total_tokens_consumed > 0
    assert "gemini-2.5-flash" in report.cost_by_model
    assert report.total_co2_grams > 0.0


def test_budget_governor_compliance_and_mitigation():
    # Under 80%
    status_nominal = BudgetGovernor.evaluate_budget(
        mission_id="m1",
        accumulated_cost_usd=0.002,
        projected_cost_usd=0.005,
        budget_ceiling_usd=0.010,
    )
    assert status_nominal.is_within_budget is True
    assert status_nominal.recommended_action == "PROCEED_NOMINAL"

    # Near threshold (>= 80%)
    status_near = BudgetGovernor.evaluate_budget(
        mission_id="m2",
        accumulated_cost_usd=0.007,
        projected_cost_usd=0.0085,
        budget_ceiling_usd=0.010,
    )
    assert status_near.is_within_budget is True
    assert status_near.recommended_action == "APPLY_PROMPT_CACHING"

    # Over budget (> 100%)
    status_breach = BudgetGovernor.evaluate_budget(
        mission_id="m3",
        accumulated_cost_usd=0.012,
        projected_cost_usd=0.015,
        budget_ceiling_usd=0.010,
    )
    assert status_breach.is_within_budget is False
    assert status_breach.recommended_action == "DOWNGRADE_TO_FLASH_LITE"
