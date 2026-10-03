"""
Unit and Integration Tests for Policy Self-Evolution & Rollback (ASVSP Pillar 8).
"""

from app.runtime.self_evolution import (
    PolicyLifecycleManager,
    PolicyMutationGenerator,
    SelfEvolutionEngine,
)


def test_policy_lifecycle_transitions():
    mgr = PolicyLifecycleManager()
    active = mgr.get_active_production_policy()
    assert active is not None
    assert active.stage == "PRODUCTION"

    # Rollback
    rolled = mgr.transition_stage(active.policy_id, "ROLLED_BACK", reason="Test breach")
    assert rolled.stage == "ROLLED_BACK"


def test_mutation_generator():
    mgr = PolicyLifecycleManager()
    base = mgr.get_active_production_policy()
    mut = PolicyMutationGenerator.generate_mutation(base, "Test candidate mutation", delta_weight_cost=0.08)
    assert mut.stage == "DRAFT"
    assert mut.parameters["weight_cost"] > base.parameters["weight_cost"]
    assert len(mut.provenance_hash) > 0


def test_instant_rollback():
    engine = SelfEvolutionEngine()
    active_pol = engine.lifecycle_mgr.get_active_production_policy()
    assert active_pol is not None

    rbk_res = engine.trigger_instant_rollback(active_pol.policy_id, "SLO Latency P99 Breach")
    assert "rollback_id" in rbk_res
    assert len(engine.get_rollback_audit_log()) == 1
