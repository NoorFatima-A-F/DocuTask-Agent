"""Tests for Goal Understanding Engine."""

from app.runtime.planning.goal_engine import (
    GoalUnderstandingEngine,
    CompletionCriteria,
)


def test_completion_criteria_evaluation():
    crit_gte = CompletionCriteria(metric_name="confidence", target_value=0.90, comparator=">=")
    assert crit_gte.evaluate(0.95) is True
    assert crit_gte.evaluate(0.90) is True
    assert crit_gte.evaluate(0.85) is False

    crit_lte = CompletionCriteria(metric_name="error_rate", target_value=0.05, comparator="<=")
    assert crit_lte.evaluate(0.02) is True
    assert crit_lte.evaluate(0.05) is True
    assert crit_lte.evaluate(0.08) is False

    crit_eq = CompletionCriteria(metric_name="status", target_value=1.0, comparator="==")
    assert crit_eq.evaluate(1.0) is True
    assert crit_eq.evaluate(0.99) is False


def test_goal_understanding_engine_parse_intent():
    engine = GoalUnderstandingEngine()
    mission_id = "test_mission_001"
    raw_intent = "Extract all invoice line items and validate tax cross-checks"

    goal_graph = engine.parse_intent(mission_id=mission_id, raw_intent=raw_intent)

    assert goal_graph.mission_id == mission_id
    assert goal_graph.root_intent == raw_intent
    assert len(goal_graph.objectives) >= 4

    # Verify topological order
    order = goal_graph.get_topological_order()
    assert len(order) == len(goal_graph.objectives)

    # Ingestion should precede Extraction, which precedes Validation
    types_in_order = [goal_graph.objectives[oid].name for oid in order]
    assert any("Ingestion" in name for name in types_in_order[:2])
    assert any("Validation" in name for name in types_in_order[2:])
