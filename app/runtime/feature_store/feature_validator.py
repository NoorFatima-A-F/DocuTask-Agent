"""
Scientific Feature Store - Feature Validator
Ensures feature vectors satisfy completeness, type consistency, and physical domain invariants.
"""

from typing import Dict, Any, List, Tuple
import math
from app.runtime.feature_store.feature_registry import FeatureDefinition, feature_registry


class FeatureValidationError(ValueError):
    """Raised when a feature vector violates required mathematical or domain invariants."""
    pass


class FeatureValidator:
    """Validates raw and normalized feature dictionaries against declared constraints."""

    @staticmethod
    def validate_raw(features: Dict[str, Any], require_all: bool = False) -> Tuple[bool, List[str]]:
        """Validates raw feature input."""
        errors: List[str] = []
        registered = {d.name: d for d in feature_registry.list_all()}

        if require_all:
            for name, defn in registered.items():
                if defn.is_required and name not in features:
                    errors.append(f"Missing required feature: '{name}'")

        for key, val in features.items():
            if key not in registered:
                continue

            defn = registered[key]
            if val is None:
                errors.append(f"Feature '{key}' cannot be None.")
                continue

            try:
                fval = float(val)
                if math.isnan(fval) or math.isinf(fval):
                    errors.append(f"Feature '{key}' has invalid NaN or Inf value.")
            except (ValueError, TypeError):
                errors.append(f"Feature '{key}' must be numeric, got {type(val).__name__}.")

        return len(errors) == 0, errors

    @staticmethod
    def validate_normalized(normalized_features: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Ensures all normalized features reside strictly in [0.0, 1.0]."""
        errors: List[str] = []
        for key, val in normalized_features.items():
            if val is None or math.isnan(val) or math.isinf(val):
                errors.append(f"Normalized feature '{key}' is NaN or Inf.")
            elif val < -1e-7 or val > 1.0 + 1e-7:
                errors.append(f"Normalized feature '{key}' = {val} is outside [0, 1].")
        return len(errors) == 0, errors
