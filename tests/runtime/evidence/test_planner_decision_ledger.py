"""Tests for Planner Decision Ledger and Regret Calculation."""

from app.runtime.decision_ledger.candidate_plan_evaluator import (
    CandidatePlanEvaluator,
)
from app.runtime.decision_ledger.decision_ledger import DecisionLedger


def test_candidate_plan_evaluation():
    candidates_raw = [
        {"candidate_id": "c1", "model": "gemini-2.5-flash", "predicted_cost_usd": 0.002, "predicted_latency_ms": 250.0, "predicted_accuracy": 0.97},
        {"candidate_id": "c2", "model": "gemini-2.5-pro", "predicted_cost_usd": 0.020, "predicted_latency_ms": 1100.0, "predicted_accuracy": 0.99},
    ]
    plans = CandidatePlanEvaluator.evaluate_candidates(candidates_raw)
    assert len(plans) == 2
    assert plans[0].candidate_id == "c1"  # Higher utility due to lower cost/latency
    assert plans[0].constraints_satisfied is True


def test_decision_ledger_chain_and_regret():
    ledger = DecisionLedger()
    candidates = [
        {"candidate_id": "c1", "model": "gemini-2.5-flash", "predicted_cost_usd": 0.002, "predicted_latency_ms": 250.0, "predicted_accuracy": 0.97},
    ]

    entry1 = ledger.record_decision(
        decision_id="dec-1",
        mission_id="m-1",
        candidates_raw=candidates,
        realized_metrics={"actual_accuracy": 0.98, "actual_cost_usd": 0.0019, "actual_latency_ms": 240.0},
    )

    assert entry1.entry_hash is not None
    assert entry1.previous_entry_hash == "genesis_decision_block_0000"
    assert entry1.regret_report is not None
    assert entry1.regret_report.is_bounded_optimal is True

    entry2 = ledger.record_decision(
        decision_id="dec-2",
        mission_id="m-1",
        candidates_raw=candidates,
    )

    assert entry2.previous_entry_hash == entry1.entry_hash
    assert ledger.count() == 2
    assert ledger.verify_chain() is True
