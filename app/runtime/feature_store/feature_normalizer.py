"""
Scientific Feature Store - Feature Normalizer
Implements deterministic, bounded mathematical normalization schemes.
"""

import math
from typing import Dict, Any, List, Optional
from app.runtime.feature_store.feature_registry import FeatureDefinition, NormalizationType


class FeatureNormalizer:
    """Normalizes raw physical metrics into standard [0, 1] or calibrated intervals."""

    @staticmethod
    def normalize_value(val: float, defn: FeatureDefinition) -> float:
        """Applies designated normalization transformation based on definition."""
        if val is None or math.isnan(val):
            val = defn.default_value

        # Clamp within declared physical bounds first
        clamped = max(defn.min_bound, min(defn.max_bound, float(val)))

        if defn.normalization_type == NormalizationType.IDENTITY:
            return clamped

        elif defn.normalization_type == NormalizationType.MIN_MAX:
            span = defn.max_bound - defn.min_bound
            if span <= 0:
                return 0.0
            return (clamped - defn.min_bound) / span

        elif defn.normalization_type == NormalizationType.LOG:
            # Scaled log1p: log(1 + x) / log(1 + max)
            val_shift = max(0.0, clamped - defn.min_bound)
            max_shift = max(1e-9, defn.max_bound - defn.min_bound)
            denom = math.log1p(max_shift)
            if denom <= 0:
                return 0.0
            return math.log1p(val_shift) / denom

        elif defn.normalization_type == NormalizationType.SIGMOID:
            # Standard logistic sigmoid shifted to midpoint
            midpoint = (defn.min_bound + defn.max_bound) / 2.0
            scale = (defn.max_bound - defn.min_bound) / 6.0 or 1.0
            z = (clamped - midpoint) / scale
            return 1.0 / (1.0 + math.exp(-z))

        elif defn.normalization_type == NormalizationType.Z_SCORE:
            # Scaled around default as mean
            std = (defn.max_bound - defn.min_bound) / 4.0 or 1.0
            z = (clamped - defn.default_value) / std
            # Map z in [-3, 3] to [0, 1]
            return max(0.0, min(1.0, (z + 3.0) / 6.0))

        return clamped

    @classmethod
    def normalize_vector(cls, raw_features: Dict[str, float], definitions: Dict[str, FeatureDefinition]) -> Dict[str, float]:
        """Normalizes an entire dictionary of features."""
        normalized: Dict[str, float] = {}
        for name, defn in definitions.items():
            raw_val = raw_features.get(name, defn.default_value)
            normalized[name] = cls.normalize_value(raw_val, defn)
        return normalized
