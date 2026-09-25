"""
Feature Normalizer for Phase 13.3 (ASCE-CGP).
Normalizes raw numerical metrics into standard [0.0, 1.0] confidence interval domains.
"""

import math
from typing import Dict
from app.runtime.confidence.features.feature_registry import FeatureRegistry


class FeatureNormalizer:
    """
    Normalizes feature vectors according to their registered normalization method.
    """

    @classmethod
    def normalize_vector(cls, features: Dict[str, float]) -> Dict[str, float]:
        normalized: Dict[str, float] = {}

        for name, value in features.items():
            definition = FeatureRegistry.get(name)
            if not definition:
                # Default clamp to [0.0, 1.0]
                normalized[name] = max(0.0, min(1.0, value))
                continue

            method = definition.normalization_method
            min_v, max_v = definition.valid_range

            if method == "IDENTITY":
                normalized[name] = max(0.0, min(1.0, value))
            elif method == "MIN_MAX":
                denom = max_v - min_v if (max_v - min_v) != 0 else 1.0
                norm_v = (value - min_v) / denom
                normalized[name] = max(0.0, min(1.0, norm_v))
            elif method == "SIGMOID":
                sigmoid = 1.0 / (1.0 + math.exp(-value))
                normalized[name] = sigmoid
            else:
                normalized[name] = max(0.0, min(1.0, value))

        return normalized
