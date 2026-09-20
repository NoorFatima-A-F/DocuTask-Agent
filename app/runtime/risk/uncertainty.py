"""
Scientific Risk Engine - Uncertainty Model
Aggregates multidimensional environmental, parametric, and execution variance.
"""

from typing import Dict, Any, List
import math


class MultiDimensionalUncertainty:
    """Calculates multidimensional uncertainty vector across system dimensions."""

    @staticmethod
    def calculate_uncertainty_vector(normalized_features: Dict[str, float]) -> Dict[str, float]:
        epistemic = normalized_features.get("epistemic_uncertainty", 0.1)
        anomaly = normalized_features.get("anomaly_score", 0.05)
        complexity = normalized_features.get("document_complexity", 0.5)
        gpu_load = normalized_features.get("gpu_load", 0.25)
        queue_len = normalized_features.get("queue_length", 0.1)

        # Environmental variance
        env_variance = min(1.0, 0.5 * gpu_load + 0.5 * queue_len)

        # Model ambiguity
        model_ambiguity = min(1.0, 0.6 * epistemic + 0.4 * anomaly)

        # Input noise
        input_noise = min(1.0, complexity * (1.0 - normalized_features.get("ocr_confidence", 0.85)))

        # Composite uncertainty index
        composite_index = math.sqrt((env_variance**2 + model_ambiguity**2 + input_noise**2) / 3.0)

        return {
            "environmental_variance": round(env_variance, 4),
            "model_ambiguity": round(model_ambiguity, 4),
            "input_noise": round(input_noise, 4),
            "composite_uncertainty_index": round(composite_index, 4),
        }
