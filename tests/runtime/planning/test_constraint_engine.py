"""Tests for Constraint Extraction & Verification Engine."""

import pytest
from app.runtime.planning.constraint_engine import (
    ConstraintExtractionEngine,
    MissionConstraintSet,
    MissionConstraint,
    ConstraintType,
    ConstraintEnforcement,
)


def test_constraint_satisfaction_and_margin():
    cnstr = MissionConstraint(
        name="Budget Limit",
        constraint_type=ConstraintType.BUDGET_USD,
        enforcement=ConstraintEnforcement.HARD,
        limit_value=0.50,
        comparator="<=",
    )

    assert cnstr.is_satisfied(0.25) is True
    assert cnstr.is_satisfied(0.50) is True
    assert cnstr.is_satisfied(0.75) is False
    assert cnstr.compute_violation_margin(0.75) == 0.25
    assert cnstr.compute_violation_margin(0.25) == 0.0


def test_constraint_set_candidate_validation():
    engine = ConstraintExtractionEngine()
    cset = engine.extract_constraints(
        mission_id="m1",
        user_constraints={"budget_usd": 0.10, "max_latency_ms": 3000.0, "min_accuracy": 0.95},
    )

    # Compliant candidate
    valid, violations, penalty = cset.validate_candidate({
        "budget_usd": 0.05,
        "latency_ms": 2000.0,
        "sla_deadline_ms": 2000.0,
        "token_limit": 5000.0,
        "accuracy_gate": 0.98,
        "concurrency_limit": 4.0,
    })
    assert valid is True
    assert len(violations) == 0
    assert penalty == 0.0

    # Violating candidate (hard budget breach)
    valid_fail, violations_fail, _ = cset.validate_candidate({
        "budget_usd": 0.25,
        "latency_ms": 2000.0,
        "sla_deadline_ms": 2000.0,
        "token_limit": 5000.0,
        "accuracy_gate": 0.98,
        "concurrency_limit": 4.0,
    })
    assert valid_fail is False
    assert len(violations_fail) > 0
    assert any("Budget" in v for v in violations_fail)
