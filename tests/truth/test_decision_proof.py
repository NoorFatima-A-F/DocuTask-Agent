"""
Tests for Decision Proof Engine (Pillar 2).
"""

from app.runtime.truth.decision_proof import DecisionProofEngine


def test_decision_proof_generation_and_utility_ranking():
    engine = DecisionProofEngine()
    
    candidates = [
        {"strategy_id": "s_fast", "strategy_name": "Fast Track", "expected_accuracy": 0.99, "expected_latency_ms": 700.0, "expected_cost_usd": 0.008},
        {"strategy_id": "s_slow", "strategy_name": "Deep Scan", "expected_accuracy": 0.995, "expected_latency_ms": 2500.0, "expected_cost_usd": 0.030},
        {"strategy_id": "s_invalid", "strategy_name": "Over Budget", "expected_accuracy": 0.90, "expected_latency_ms": 4000.0, "expected_cost_usd": 0.080},
    ]

    proof = engine.generate_proof(
        mission_id="msn_1001",
        document_type="invoice",
        candidates=candidates,
        latency_budget_ms=3000.0,
        cost_budget_usd=0.050,
    )

    assert proof.selected_strategy_id == "s_fast"
    assert proof.winning_utility_score > 0
    assert len(proof.candidates_evaluated) == 3
    
    # Over Budget should be marked infeasible
    infeasible = [c for c in proof.candidates_evaluated if not c.is_feasible]
    assert len(infeasible) == 1
    assert "Exceeded latency SLA budget" in infeasible[0].rejection_reason
