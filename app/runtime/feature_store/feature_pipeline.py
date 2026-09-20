"""
Scientific Feature Store - Feature Pipeline
Orchestrates end-to-end extraction, normalization, validation, versioning, and statistics tracking.
"""

from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass
from app.runtime.feature_store.feature_registry import feature_registry, CANONICAL_FEATURES
from app.runtime.feature_store.feature_engine import FeatureEngine
from app.runtime.feature_store.feature_normalizer import FeatureNormalizer
from app.runtime.feature_store.feature_validator import FeatureValidator, FeatureValidationError
from app.runtime.feature_store.feature_versioning import FeatureVersionManager, FeatureSnapshot
from app.runtime.feature_store.feature_statistics import feature_statistics_tracker


@dataclass
class ProcessedFeatureVector:
    raw_features: Dict[str, float]
    normalized_features: Dict[str, float]
    snapshot: FeatureSnapshot
    is_valid: bool
    validation_errors: list[str]


class FeaturePipeline:
    """Central pipeline ensuring all planner decisions flow through validated, versioned features."""

    def __init__(self):
        self.registry = feature_registry
        self.normalizer = FeatureNormalizer()
        self.validator = FeatureValidator()
        self.version_manager = FeatureVersionManager()
        self.stats_tracker = feature_statistics_tracker

    def process_telemetry(
        self,
        telemetry: Dict[str, Any],
        document_context: Optional[Dict[str, Any]] = None,
        context_id: str = "default_context",
    ) -> ProcessedFeatureVector:
        """Runs the complete feature transformation and validation pipeline."""
        # 1. Extraction
        raw = FeatureEngine.extract_from_telemetry(telemetry, document_context)

        # 2. Raw Validation
        is_raw_valid, raw_errors = self.validator.validate_raw(raw)
        if not is_raw_valid:
            raise FeatureValidationError(f"Raw feature validation failed: {raw_errors}")

        # 3. Normalization
        definitions = {defn.name: defn for defn in self.registry.list_all()}
        normalized = self.normalizer.normalize_vector(raw, definitions)

        # 4. Normalized Validation
        is_norm_valid, norm_errors = self.validator.validate_normalized(normalized)
        if not is_norm_valid:
            raise FeatureValidationError(f"Normalized feature validation failed: {norm_errors}")

        # 5. Versioned Snapshot
        snapshot = self.version_manager.create_snapshot(
            context_id=context_id,
            raw_features=raw,
            normalized_features=normalized,
        )

        # 6. Statistics Tracking
        self.stats_tracker.record(normalized)

        return ProcessedFeatureVector(
            raw_features=raw,
            normalized_features=normalized,
            snapshot=snapshot,
            is_valid=True,
            validation_errors=[],
        )


feature_pipeline = FeaturePipeline()
