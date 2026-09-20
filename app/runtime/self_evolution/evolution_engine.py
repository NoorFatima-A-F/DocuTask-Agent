"""
Self-Evolution Runtime - Master Evolution Engine Facade
Coordinates policy lifecycle, mutation proposals, stage promotions, and instant rollback.
"""

from typing import Dict, List, Any, Optional
from app.runtime.self_evolution.policy_lifecycle import PolicyLifecycleManager, PolicyDefinition
from app.runtime.self_evolution.mutation_generator import PolicyMutationGenerator
from app.runtime.self_evolution.rollback_manager import RollbackManager, RollbackEvent


class SelfEvolutionEngine:
    """Master engine for continuous self-evolution and policy safety governance."""

    def __init__(self):
        self.lifecycle_mgr = PolicyLifecycleManager()
        self.mutation_gen = PolicyMutationGenerator()
        self.rollback_mgr = RollbackManager(self.lifecycle_mgr)

    def list_all_policies(self) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in self.lifecycle_mgr.list_policies()]

    def propose_candidate_mutation(
        self,
        base_policy_id: str,
        mutation_name: str,
        delta_weight_cost: float = 0.05,
    ) -> Dict[str, Any]:
        base_pol = self.lifecycle_mgr.policies.get(base_policy_id)
        if not base_pol:
            raise ValueError(f"Base policy {base_policy_id} not found")

        mut = self.mutation_gen.generate_mutation(
            base_policy=base_pol,
            mutation_name=mutation_name,
            delta_weight_cost=delta_weight_cost,
        )
        self.lifecycle_mgr.policies[mut.policy_id] = mut
        return mut.to_dict()

    def promote_policy(self, policy_id: str, target_stage: str) -> Dict[str, Any]:
        pol = self.lifecycle_mgr.transition_stage(policy_id, target_stage)
        return pol.to_dict()

    def trigger_instant_rollback(self, active_policy_id: str, reason: str) -> Dict[str, Any]:
        event = self.rollback_mgr.execute_instant_rollback(
            active_policy_id=active_policy_id,
            safe_fallback_policy_id="pol_v4_2",
            reason=reason,
        )
        return event.to_dict()

    def get_rollback_audit_log(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.rollback_mgr.rollback_history]
