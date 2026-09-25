"""
Policy Evaluation Engine - Sensitivity Analysis
Performs local gradient and one-at-a-time (OAT) parameter sensitivity analysis over objective weights.
"""

from typing import Dict, Any, Callable


class WeightSensitivityAnalyzer:
    """Calculates sensitivity gradients of expected utility with respect to objective weights."""

    @staticmethod
    def analyze_weight_sensitivity(
        eval_fn: Callable[[Dict[str, float]], float],
        base_weights: Dict[str, float],
        step_size: float = 0.05,
    ) -> Dict[str, Any]:
        base_utility = eval_fn(base_weights)
        sensitivities: Dict[str, float] = {}

        for key, w_val in base_weights.items():
            perturbed = dict(base_weights)
            perturbed[key] = max(0.0, w_val + step_size)
            # Re-normalize
            total = sum(perturbed.values()) or 1.0
            norm_perturbed = {k: v / total for k, v in perturbed.items()}

            perturbed_u = eval_fn(norm_perturbed)
            gradient = (perturbed_u - base_utility) / step_size
            sensitivities[key] = round(gradient, 4)

        # Identify most influential weight dimension
        most_sensitive = max(sensitivities.items(), key=lambda x: abs(x[1])) if sensitivities else ("none", 0.0)

        return {
            "base_utility": round(base_utility, 4),
            "weight_gradients": sensitivities,
            "most_sensitive_dimension": most_sensitive[0],
            "max_gradient_magnitude": round(abs(most_sensitive[1]), 4),
        }
