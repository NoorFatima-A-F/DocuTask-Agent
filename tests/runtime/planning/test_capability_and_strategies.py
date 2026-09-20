"""Tests for Capability Discovery and Candidate Strategy Generation."""

import pytest
from app.runtime.planning.goal_engine import GoalUnderstandingEngine
from app.runtime.planning.constraint_engine import ConstraintExtractionEngine
from app.runtime.planning.capability_discovery import CapabilityDiscoveryEngine, CapabilityType, CapabilityHealth
from app.runtime.planning.strategy_generator import CandidateStrategyGenerator, StrategyArchetype


def test_capability_discovery_and_allocation():
    registry = CapabilityDiscoveryEngine()
    ocr_caps = registry.discover_for_type(CapabilityType.OCR_ENGINE)
    assert len(ocr_caps) >= 2

    # Capacity allocation
    cap = ocr_caps[0]
    initial_avail = cap.available_capacity
    assert registry.allocate_capacity(cap.capability_id, 2) is True
    assert cap.available_capacity == initial_avail - 2

    registry.release_capacity(cap.capability_id, 2)
    assert cap.available_capacity == initial_avail


def test_candidate_strategy_generator():
    cap_engine = CapabilityDiscoveryEngine()
    goal_engine = GoalUnderstandingEngine()
    constraint_engine = ConstraintExtractionEngine()

    goal_graph = goal_engine.parse_intent("m1", "Extract tax forms and cross-validate")
    constraints = constraint_engine.extract_constraints("m1")

    generator = CandidateStrategyGenerator(cap_engine)
    strategies = generator.generate_strategies(goal_graph, constraints)

    assert len(strategies) == 4
    archetypes = {s.archetype for s in strategies}
    assert archetypes == {
        StrategyArchetype.ALPHA_FAST,
        StrategyArchetype.BETA_ACCURATE,
        StrategyArchetype.GAMMA_COST,
        StrategyArchetype.DELTA_PARETO,
    }

    # Verify each strategy has steps matching the objectives
    for s in strategies:
        assert len(s.steps) == len(goal_graph.objectives)
        assert s.estimated_total_cost_usd > 0.0
        assert s.estimated_critical_path_ms > 0.0
        assert s.estimated_accuracy > 0.8
