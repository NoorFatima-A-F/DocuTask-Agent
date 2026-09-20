"""
Unit and Integration Tests for Counterfactual Simulator & Replay (ASVSP Pillar 3).
"""

import pytest
from app.runtime.counterfactual import (
    ScenarioGenerator,
    AlternatePlanner,
    CounterfactualComparisonEngine,
    CounterfactualReplayOptimizer,
    CounterfactualSimulator,
)


def test_scenario_generation():
    generator = ScenarioGenerator()
    scenarios = generator.list_scenarios()
    assert len(scenarios) >= 4

    features = {"latency_p95_ms": 0.3, "ocr_confidence": 0.95}
    peak_scenario = next(s for s in scenarios if s.scenario_id == "sc_peak_load")
    modified = generator.apply_scenario_to_features(features, peak_scenario)
    assert modified["latency_p95_ms"] > features["latency_p95_ms"]


def test_alternate_planner_and_comparison():
    candidates = AlternatePlanner.generate_alternatives(
        factual_model="gemini-2.5-flash",
        factual_accuracy=0.96,
        factual_latency_ms=450.0,
        factual_cost_usd=0.0015,
        factual_utility=0.88,
    )
    assert len(candidates) == 3

    diff = CounterfactualComparisonEngine.compare_branch(
        factual_model="gemini-2.5-flash",
        factual_acc=0.96,
        factual_lat_ms=450.0,
        factual_cost_usd=0.0015,
        factual_u=0.88,
        candidate=candidates[0],
    )
    assert diff.factual_choice == "gemini-2.5-flash"
    assert isinstance(diff.factual_was_optimal, bool)


def test_counterfactual_replay_optimizer():
    optimizer = CounterfactualReplayOptimizer()
    result = optimizer.replay_mission(
        mission_id="m_test_replay",
        factual_model="gemini-2.5-flash",
        factual_accuracy=0.96,
        factual_latency_ms=480.0,
        factual_cost_usd=0.0018,
        factual_utility=0.89,
        scenario_id="sc_nominal",
    )
    assert result.mission_id == "m_test_replay"
    assert result.factual_decision_efficiency >= 0.0
    assert len(result.evaluated_branches) == 3
