"""
Scientific Feature Store Package.
Provides centralized, versioned, normalized, and validated runtime features.
"""

from app.runtime.feature_store.feature_registry import (
    FeatureDefinition,
    FeatureCategory,
    NormalizationType,
    FeatureRegistry,
    feature_registry,
    CANONICAL_FEATURES,
)
from app.runtime.feature_store.feature_normalizer import FeatureNormalizer
from app.runtime.feature_store.feature_validator import FeatureValidator, FeatureValidationError
from app.runtime.feature_store.feature_statistics import FeatureStatisticsTracker, feature_statistics_tracker
from app.runtime.feature_store.feature_versioning import FeatureVersionManager, FeatureSnapshot
from app.runtime.feature_store.feature_engine import FeatureEngine
from app.runtime.feature_store.feature_pipeline import FeaturePipeline, ProcessedFeatureVector, feature_pipeline

__all__ = [
    "FeatureDefinition",
    "FeatureCategory",
    "NormalizationType",
    "FeatureRegistry",
    "feature_registry",
    "CANONICAL_FEATURES",
    "FeatureNormalizer",
    "FeatureValidator",
    "FeatureValidationError",
    "FeatureStatisticsTracker",
    "feature_statistics_tracker",
    "FeatureVersionManager",
    "FeatureSnapshot",
    "FeatureEngine",
    "FeaturePipeline",
    "ProcessedFeatureVector",
    "feature_pipeline",
]
