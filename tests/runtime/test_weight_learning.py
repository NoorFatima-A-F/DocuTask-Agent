"""
Unit & Governance Tests for Adaptive Weight Learning (QDIOP / SDIOP).
"""

import pytest
from app.runtime.learning import (
    AdaptiveWeightLearner,
    policy_store,
    AdaptivePolicyManager,
)


def test_adaptive_weight_learning_proposes_normalized_weights():
    current_w = {"accuracy": 0.35, "latency": 0.20, "cost": 0.15, "safety_compliance": 0.15, "reliability": 0.15}
    outcomes = [
        {"accuracy": 0.85, "latency_ms": 1600.0, "cost_usd": 0.03},
        {"accuracy": 0.88, "latency_ms": 1400.0, "cost_usd": 0.025},
    ]

    proposal = AdaptiveWeightLearner.propose_weights(current_w, outcomes)
    assert proposal.requires_human_approval
    assert proposal.status == "PENDING_APPROVAL"
    assert proposal.proposed_weights["accuracy"] >= current_w["accuracy"]
    assert abs(sum(proposal.proposed_weights.values()) - 1.0) < 1e-3


def test_policy_store_version_approval_gate():
    policy_store.register_policy(
        version="v2.0.0-draft",
        weights={"accuracy": 0.40, "latency": 0.20, "cost": 0.15, "safety_compliance": 0.15, "reliability": 0.10},
        description="Candidate high-accuracy policy",
    )
    # Activation requires approved_by authority
    approved = policy_store.approve_and_activate("v2.0.0-draft", approved_by="Chief Risk Officer")
    assert approved.is_active
    assert approved.approved_by == "Chief Risk Officer"
