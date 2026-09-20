"""
Feature Validator for Phase 13.3 (ASCE-CGP).
Ensures feature vectors meet schema ranges, contains no NaNs/Infs, and respects bounds.
"""

import math
from typing import Dict, Tuple
from app.runtime.confidence.features.feature_registry import FeatureRegistry


class FeatureValidator:
    """
    Validates numerical feature values against registered definitions.
    """

    @classmethod
    def validate_features(cls, features: Dict[str, float]) -> Tuple[bool, Dict[str, str]]:
        errors: Dict[str, str] = {}

        for name, value in features.items():
            if math.isnan(value) or math.isinf(value):
                errors[name] = f"Invalid numerical value: {value}"
                continue

            definition = FeatureRegistry.get(name)
            if definition:
                min_v, max_v = definition.valid_range
                if value < min_v or value > max_v:
                    errors[name] = f"Value {value} out of registered range [{min_v}, {max_v}]"

        return len(errors) == 0, errors
