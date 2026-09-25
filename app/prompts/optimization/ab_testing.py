"""Prompt A/B Testing & Optimization Engine (Phase 8D).

Conducts controlled traffic experiments, records conversion metrics, and selects winning prompt versions.
"""

from __future__ import annotations

import random
import time
from typing import Dict, List, Optional
from app.prompts.optimization.experiments import ExperimentStatus, PromptExperiment, PromptVariant


class PromptABTestingService:
    """Manages active prompt experiments and variant traffic resolution."""

    def __init__(self):
        # experiment_id -> PromptExperiment
        self._experiments: Dict[str, PromptExperiment] = {}

    def create_experiment(
        self,
        experiment_id: str,
        prompt_id: str,
        name: str,
        organization_id: str,
        variants: List[PromptVariant],
    ) -> PromptExperiment:
        """Create new A/B experiment."""
        exp = PromptExperiment(
            experiment_id=experiment_id,
            prompt_id=prompt_id,
            name=name,
            organization_id=organization_id,
            status=ExperimentStatus.RUNNING,
            variants=variants,
        )
        self._experiments[experiment_id] = exp
        return exp

    def resolve_variant_for_request(self, experiment_id: str) -> Optional[PromptVariant]:
        """Stochastically select variant based on assigned traffic weights."""
        exp = self._experiments.get(experiment_id)
        if not exp or exp.status != ExperimentStatus.RUNNING or not exp.variants:
            return None

        r = random.random()
        cumulative = 0.0
        for variant in exp.variants:
            cumulative += variant.traffic_weight
            if r <= cumulative:
                return variant

        return exp.variants[0]

    def record_outcome(
        self,
        experiment_id: str,
        variant_id: str,
        is_success: bool,
        latency_ms: float = 0.0,
        positive_feedback: bool = False,
    ) -> None:
        """Record runtime outcome for an experimental variant."""
        exp = self._experiments.get(experiment_id)
        if not exp:
            return

        for v in exp.variants:
            if v.variant_id == variant_id:
                v.total_invocations += 1
                if is_success:
                    v.successful_invocations += 1
                v.total_latency_ms += latency_ms
                if positive_feedback:
                    v.positive_feedback_count += 1
                break

    def conclude_experiment(self, experiment_id: str) -> Optional[PromptVariant]:
        """Evaluate outcomes, determine winning variant, and conclude experiment."""
        exp = self._experiments.get(experiment_id)
        if not exp or not exp.variants:
            return None

        # Winner: highest success rate (with tie breaker on positive feedback or lowest latency)
        best_variant = None
        best_score = -1.0

        for v in exp.variants:
            if v.total_invocations == 0:
                continue
            success_rate = v.successful_invocations / v.total_invocations
            feedback_rate = v.positive_feedback_count / v.total_invocations
            score = success_rate * 0.7 + feedback_rate * 0.3

            if score > best_score:
                best_score = score
                best_variant = v

        if best_variant:
            exp.winner_variant_id = best_variant.variant_id
            exp.status = ExperimentStatus.CONCLUDED
            exp.concluded_at = time.time()

        return best_variant
