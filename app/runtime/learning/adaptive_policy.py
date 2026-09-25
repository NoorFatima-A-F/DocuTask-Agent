"""
Adaptive Weight Learning - Adaptive Policy Execution
Executes planner decisions with active certified policy and supports shadow testing.
"""

from typing import Dict
from app.runtime.learning.policy_store import policy_store
from app.runtime.learning.weight_learner import AdaptiveWeightLearner, WeightProposal


class AdaptivePolicyManager:
    """Provides access to certified active weights and records learning proposals."""

    @classmethod
    def get_current_weights(cls) -> Dict[str, float]:
        active = policy_store.get_active_policy()
        return dict(active.weights)

    @classmethod
    def trigger_learning_cycle(cls, observed_outcomes: list[Dict[str, float]]) -> WeightProposal:
        current_w = cls.get_current_weights()
        proposal = AdaptiveWeightLearner.propose_weights(current_w, observed_outcomes)
        return proposal
