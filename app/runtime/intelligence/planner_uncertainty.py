"""Planner Uncertainty & Decision Stability Engine for DocuTask ADIP.

Decomposes uncertainty into Epistemic (reducible via sensing) and Aleatoric (inherent stochastic noise),
computes decision stability ratios, and generates composite confidence metrics for planning decisions.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.intelligence.belief_state import BeliefStateEngine


class UncertaintyDecomposition(BaseModel):
    """Detailed decomposition of uncertainty sources."""
    mission_id: str
    epistemic_uncertainty: float = Field(ge=0.0, le=1.0, description="Reducible uncertainty from lack of observations")
    aleatoric_uncertainty: float = Field(ge=0.0, le=1.0, description="Irreducible noise in models/APIs")
    model_uncertainty: float = Field(ge=0.0, le=1.0)
    capability_uncertainty: float = Field(ge=0.0, le=1.0)
    decision_stability_index: float = Field(ge=0.0, description="Delta Utility / Sigma(Utility)")
    composite_confidence: float = Field(ge=0.0, le=1.0)
    is_decision_stable: bool
    summary: str = ""


class PlannerUncertaintyEngine:
    """Calculates multidimensional uncertainty profiles for candidate planning strategies."""

    def evaluate_uncertainty(
        self,
        mission_id: str,
        belief_engine: BeliefStateEngine,
        strategy_utility_delta: float = 0.05,
        simulation_variance: float = 0.008,
    ) -> UncertaintyDecomposition:
        # 1. Epistemic Uncertainty: Proportional to normalized total Shannon entropy of belief state
        total_entropy = belief_engine.compute_total_entropy()
        max_possible_entropy = 10.0 * 1.0  # 10 Bernoulli variables with max 1 bit each
        epistemic = min(1.0, total_entropy / max_possible_entropy)

        # 2. Aleatoric Uncertainty: Based on inherent failure probabilities of APIs
        api_belief = belief_engine.get_belief("api_failure")
        doc_belief = belief_engine.get_belief("document_damaged")
        aleatoric = min(1.0, ((api_belief.mean if api_belief else 0.05) + (doc_belief.mean if doc_belief else 0.15)) / 2.0)

        # 3. Model & Capability Uncertainty
        model_unc = min(1.0, math.sqrt(simulation_variance) * 5.0)
        worker_belief = belief_engine.get_belief("worker_alive")
        cap_unc = 1.0 - (worker_belief.mean if worker_belief else 0.95)

        # 4. Decision Stability Ratio: Delta Utility divided by Standard Deviation
        sigma_u = max(1e-4, math.sqrt(simulation_variance))
        stability_ratio = round(strategy_utility_delta / sigma_u, 2)
        is_stable = stability_ratio >= 2.0

        # 5. Composite Confidence: 1 - Harmonic Mean of uncertainties
        avg_uncertainty = (epistemic * 0.4) + (aleatoric * 0.3) + (model_unc * 0.2) + (cap_unc * 0.1)
        composite_conf = round(max(0.0, min(1.0, 1.0 - avg_uncertainty)), 4)

        summary = (
            f"Composite Planner Confidence: {composite_conf*100:.1f}%. "
            f"Epistemic: {epistemic*100:.1f}%, Aleatoric: {aleatoric*100:.1f}%, "
            f"Stability Ratio: {stability_ratio} (Decision {'STABLE' if is_stable else 'UNSTABLE'})."
        )

        return UncertaintyDecomposition(
            mission_id=mission_id,
            epistemic_uncertainty=round(epistemic, 4),
            aleatoric_uncertainty=round(aleatoric, 4),
            model_uncertainty=round(model_unc, 4),
            capability_uncertainty=round(cap_unc, 4),
            decision_stability_index=stability_ratio,
            composite_confidence=composite_conf,
            is_decision_stable=is_stable,
            summary=summary,
        )
