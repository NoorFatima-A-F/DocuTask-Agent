"""
AWM-PSDTIP Phase 13.10 - Bayesian Belief Engine
Maintains probabilistic belief states, prior and posterior updates, likelihood estimation, and evidence accumulation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class BayesianBelief:
    belief_id: str
    hypothesis: str  # e.g., "P(Zero-Fabrication | Triadic Consensus) >= 0.999"
    domain: str
    prior_probability: float
    likelihood: float
    posterior_probability: float
    evidence_count: int
    confidence_interval: List[float]  # [lower, upper]
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence_history: List[Dict[str, Any]] = field(default_factory=list)


class BayesianBeliefEngine:
    """
    Maintains calibrated Bayesian beliefs over mission outcomes, failure probabilities, and model fidelity.
    """

    def __init__(self):
        self._beliefs: Dict[str, BayesianBelief] = {}
        self._seed_default_beliefs()

    def register_belief(
        self,
        hypothesis: str,
        domain: str,
        initial_prior: float = 0.5,
    ) -> BayesianBelief:
        bid = f"bel-{uuid.uuid4().hex[:8]}"
        lower = round(max(0.01, initial_prior - 0.1), 3)
        upper = round(min(0.99, initial_prior + 0.1), 3)

        belief = BayesianBelief(
            belief_id=bid,
            hypothesis=hypothesis,
            domain=domain,
            prior_probability=initial_prior,
            likelihood=1.0,
            posterior_probability=initial_prior,
            evidence_count=0,
            confidence_interval=[lower, upper],
        )
        self._beliefs[bid] = belief
        return belief

    def update_belief_with_evidence(
        self,
        belief_id: str,
        evidence_source: str,
        supports_hypothesis: bool,
        evidence_weight: float = 1.0,
    ) -> BayesianBelief:
        belief = self._beliefs.get(belief_id)
        if not belief:
            raise ValueError(f"Belief {belief_id} not found.")

        # Bayes rule update: P(H|E) = (P(E|H) * P(H)) / P(E)
        prior = belief.posterior_probability
        p_e_given_h = 0.95 if supports_hypothesis else 0.05
        p_e_given_not_h = 0.05 if supports_hypothesis else 0.95

        p_e = (p_e_given_h * prior) + (p_e_given_not_h * (1.0 - prior))
        posterior = (p_e_given_h * prior) / max(0.0001, p_e)

        belief.prior_probability = round(prior, 4)
        belief.likelihood = round(p_e_given_h, 4)
        belief.posterior_probability = round(posterior, 4)
        belief.evidence_count += 1
        belief.last_updated = datetime.now(timezone.utc).isoformat()

        # Update confidence interval based on sample count
        margin = max(0.005, 0.20 / (belief.evidence_count ** 0.5))
        belief.confidence_interval = [
            round(max(0.0, posterior - margin), 4),
            round(min(1.0, posterior + margin), 4),
        ]

        belief.evidence_history.append({
            "source": evidence_source,
            "supports": supports_hypothesis,
            "weight": evidence_weight,
            "timestamp": belief.last_updated,
        })

        return belief

    def get_belief(self, belief_id: str) -> Optional[BayesianBelief]:
        return self._beliefs.get(belief_id)

    def list_beliefs(self) -> List[BayesianBelief]:
        return list(self._beliefs.values())

    def _seed_default_beliefs(self):
        b1 = self.register_belief(
            hypothesis="P(Zero-Fabrication Guarantee | Triadic Consensus Audit) >= 0.999",
            domain="TRUTH_VERIFICATION",
            initial_prior=0.985,
        )
        for i in range(10):
            self.update_belief_with_evidence(b1.belief_id, f"mission_trace_{i:03d}", supports_hypothesis=True)

        b2 = self.register_belief(
            hypothesis="P(DAG Parallel Fan-Out Stalls | VRAM Headroom < 2GB) >= 0.85",
            domain="RESOURCE_MANAGEMENT",
            initial_prior=0.75,
        )
        self.update_belief_with_evidence(b2.belief_id, "telemetry_stress_trial", supports_hypothesis=True)
