"""Bayesian Update Engine & Evidence Provenance Network for DocuTask ADIP.

Implements exact conjugate Bayesian updating (Prior -> Likelihood -> Posterior),
computes 95% Credible Intervals, and maintains an immutable cryptographic evidence accumulation chain.
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field

from app.runtime.intelligence.belief_state import BeliefStateEngine


class BayesianEvidenceNode(BaseModel):
    """Single observed piece of empirical evidence."""
    evidence_id: str = Field(default_factory=lambda: f"evi_{uuid.uuid4().hex[:8]}")
    variable_name: str
    observed_signal: str
    success_increment: float
    failure_increment: float
    likelihood_p_given_s: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_worker_id: Optional[str] = None
    hash_signature: str = ""

    def compute_hash(self, prev_hash: str = "") -> str:
        payload = f"{self.evidence_id}:{self.variable_name}:{self.observed_signal}:{self.success_increment}:{self.failure_increment}:{self.timestamp}:{prev_hash}"
        self.hash_signature = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return self.hash_signature


class BayesianPosteriorReport(BaseModel):
    """Complete posterior probability report with credible intervals and algebraic provenance."""
    variable_name: str
    prior_mean: float
    posterior_mean: float
    likelihood: float
    credible_interval_95: List[float]
    evidence_count: int
    formula_provenance: str = "P(S \\mid O) = \\frac{P(O \\mid S) P(S)}{P(O)}"
    merkle_evidence_root: str
    version: str = "1.0.0"


class BayesianUpdateEngine:
    """Manages Bayesian inference, evidence accumulation, and posterior generation."""

    def __init__(self, belief_engine: BeliefStateEngine) -> None:
        self.belief_engine = belief_engine
        self._evidence_chain: List[BayesianEvidenceNode] = []
        self._latest_merkle_hash: str = "genesis_evidence_block_00000000"

    def submit_observation(
        self,
        variable_name: str,
        observed_signal: str,
        success_increment: float,
        failure_increment: float,
        likelihood: float = 0.95,
        worker_id: Optional[str] = None,
    ) -> BayesianPosteriorReport:
        """Applies exact Bayesian update and records evidence in cryptographic chain."""
        # 1. Fetch prior
        prior_belief = self.belief_engine.get_belief(variable_name)
        prior_mean = prior_belief.mean if prior_belief else 0.5

        # 2. Record evidence node
        node = BayesianEvidenceNode(
            variable_name=variable_name,
            observed_signal=observed_signal,
            success_increment=success_increment,
            failure_increment=failure_increment,
            likelihood_p_given_s=likelihood,
            source_worker_id=worker_id,
        )
        self._latest_merkle_hash = node.compute_hash(self._latest_merkle_hash)
        self._evidence_chain.append(node)

        # 3. Update belief state engine
        updated_belief, _ = self.belief_engine.update_belief(
            variable_name, success_increment, failure_increment
        )
        ci_lower, ci_upper = updated_belief.get_credible_interval_95()

        return BayesianPosteriorReport(
            variable_name=variable_name,
            prior_mean=round(prior_mean, 4),
            posterior_mean=round(updated_belief.mean, 4),
            likelihood=round(likelihood, 4),
            credible_interval_95=[ci_lower, ci_upper],
            evidence_count=len(self._evidence_chain),
            merkle_evidence_root=self._latest_merkle_hash,
        )

    def get_evidence_chain(self) -> List[BayesianEvidenceNode]:
        return list(self._evidence_chain)
