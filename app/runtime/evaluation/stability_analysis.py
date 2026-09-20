"""
Policy Evaluation Engine - Stability Analysis
Evaluates decision robustness and flips under epsilon-perturbations in input feature telemetry.
"""

from typing import Dict, List, Any, Callable
import random


class DecisionStabilityAnalyzer:
    """Evaluates decision invariance under input noise."""

    @staticmethod
    def evaluate_perturbation_stability(
        decision_fn: Callable[[Dict[str, float]], str],
        base_features: Dict[str, float],
        noise_level: float = 0.05,
        trials: int = 50,
    ) -> Dict[str, Any]:
        base_decision = decision_fn(base_features)
        match_count = 0

        for _ in range(trials):
            noisy = {}
            for k, v in base_features.items():
                noise = random.gauss(0.0, noise_level)
                noisy[k] = max(0.0, min(1.0, v + noise))

            trial_decision = decision_fn(noisy)
            if trial_decision == base_decision:
                match_count += 1

        stability_score = match_count / float(trials)
        return {
            "base_decision": base_decision,
            "perturbation_noise_level": noise_level,
            "trials_conducted": trials,
            "consistent_decision_count": match_count,
            "stability_score": round(stability_score, 4),
            "is_stable": stability_score >= 0.90,
        }
