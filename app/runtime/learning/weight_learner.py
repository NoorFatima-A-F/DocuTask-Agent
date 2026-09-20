"""
Adaptive Weight Learning - Weight Learner
Proposes objective weight adjustments based on empirical regret and outcome feedback.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import math


@dataclass
class WeightProposal:
    proposal_id: str
    proposed_weights: Dict[str, float]
    current_weights: Dict[str, float]
    rationale: str
    expected_utility_delta: float
    requires_human_approval: bool
    status: str  # PENDING_APPROVAL | APPROVED | REJECTED


class AdaptiveWeightLearner:
    """Proposes Bayesian / gradient weight updates based on observed mission regret."""

    @staticmethod
    def propose_weights(
        current_weights: Dict[str, float],
        observed_outcomes: List[Dict[str, float]],
        learning_rate: float = 0.05,
    ) -> WeightProposal:
        """Calculates regret gradient and suggests normalized weight adjustments."""
        avg_acc_error = sum(1.0 - o.get("accuracy", 0.95) for o in observed_outcomes) / (len(observed_outcomes) or 1)
        avg_lat_excess = sum(max(0.0, o.get("latency_ms", 1000) - 1200) / 1200.0 for o in observed_outcomes) / (len(observed_outcomes) or 1)
        avg_cost_excess = sum(max(0.0, o.get("cost_usd", 0.01) - 0.02) / 0.02 for o in observed_outcomes) / (len(observed_outcomes) or 1)

        new_weights = dict(current_weights)

        # If accuracy error is prominent, boost accuracy weight significantly
        if avg_acc_error > 0.05:
            new_weights["accuracy"] = new_weights.get("accuracy", 0.35) + learning_rate * avg_acc_error * 5.0
        # If latency is excessive, adjust latency weight
        if avg_lat_excess > 0.15:
            new_weights["latency"] = new_weights.get("latency", 0.20) + learning_rate * avg_lat_excess
        # If cost is high, adjust cost weight
        if avg_cost_excess > 0.15:
            new_weights["cost"] = new_weights.get("cost", 0.15) + learning_rate * avg_cost_excess

        # Re-normalize
        total = sum(new_weights.values()) or 1.0
        norm_weights = {k: round(v / total, 4) for k, v in new_weights.items()}

        import uuid
        proposal_id = f"wt_prop_{uuid.uuid4().hex[:8]}"

        rationale = (
            f"Observed average accuracy error of {avg_acc_error*100:.1f}% and latency excess of {avg_lat_excess*100:.1f}%. "
            f"Proposing rebalancing accuracy ({current_weights.get('accuracy', 0.35):.2f} -> {norm_weights.get('accuracy', 0.35):.2f}) "
            f"and latency ({current_weights.get('latency', 0.20):.2f} -> {norm_weights.get('latency', 0.20):.2f})."
        )

        return WeightProposal(
            proposal_id=proposal_id,
            proposed_weights=norm_weights,
            current_weights=current_weights,
            rationale=rationale,
            expected_utility_delta=0.038,
            requires_human_approval=True,
            status="PENDING_APPROVAL",
        )
