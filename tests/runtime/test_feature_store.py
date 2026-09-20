"""
Unit & Regression Tests for Scientific Feature Store (QDIOP / SDIOP).
Tests feature registry, normalizers, validation, and versioned pipelines.
"""

import pytest
import math
from app.runtime.feature_store import (
    feature_registry,
    FeatureNormalizer,
    FeatureValidator,
    FeatureValidationError,
    feature_pipeline,
    FeatureStatisticsTracker,
    FeatureVersionManager,
)
from app.runtime.feature_store.feature_registry import FeatureDefinition, FeatureCategory, NormalizationType


def test_feature_registry_contains_16_canonical_features():
    names = feature_registry.get_names()
    assert len(names) >= 16
    assert "ocr_confidence" in names
    assert "schema_validation_score" in names
    assert "latency_p95_ms" in names
    assert "historical_success_rate" in names
    assert "retry_count" in names
    assert "memory_similarity" in names
    assert "document_complexity" in names
    assert "worker_reliability" in names
    assert "gpu_load" in names
    assert "queue_length" in names
    assert "api_cost_usd" in names
    assert "token_count" in names
    assert "human_validation_rate" in names
    assert "compliance_flags" in names
    assert "anomaly_score" in names
    assert "epistemic_uncertainty" in names


def test_feature_normalizer_schemes():
    defn_minmax = FeatureDefinition(
        name="test_minmax",
        category=FeatureCategory.PERFORMANCE,
        data_type=float,
        min_bound=0.0,
        max_bound=100.0,
        default_value=50.0,
        normalization_type=NormalizationType.MIN_MAX,
        description="Test minmax",
    )
    assert FeatureNormalizer.normalize_value(0.0, defn_minmax) == 0.0
    assert FeatureNormalizer.normalize_value(50.0, defn_minmax) == 0.5
    assert FeatureNormalizer.normalize_value(100.0, defn_minmax) == 1.0
    assert FeatureNormalizer.normalize_value(150.0, defn_minmax) == 1.0  # Clamped

    defn_log = FeatureDefinition(
        name="test_log",
        category=FeatureCategory.RESOURCE,
        data_type=float,
        min_bound=0.0,
        max_bound=1000.0,
        default_value=10.0,
        normalization_type=NormalizationType.LOG,
        description="Test log",
    )
    val_norm = FeatureNormalizer.normalize_value(100.0, defn_log)
    assert 0.0 <= val_norm <= 1.0


def test_feature_validator_enforces_invariants():
    valid_features = {"ocr_confidence": 0.95, "latency_p95_ms": 1200.0}
    is_valid, errors = FeatureValidator.validate_raw(valid_features)
    assert is_valid
    assert len(errors) == 0

    invalid_features = {"ocr_confidence": float("nan")}
    is_valid_nan, errors_nan = FeatureValidator.validate_raw(invalid_features)
    assert not is_valid_nan
    assert any("NaN" in e for e in errors_nan)


def test_feature_pipeline_end_to_end():
    telemetry = {
        "ocr_confidence": 0.98,
        "latency_ms": 750.0,
        "validation_score": 1.0,
        "cost": 0.002,
    }
    processed = feature_pipeline.process_telemetry(telemetry, context_id="mission_test_001")
    assert processed.is_valid
    assert processed.snapshot.schema_hash != ""
    assert 0.0 <= processed.normalized_features["ocr_confidence"] <= 1.0
    assert 0.0 <= processed.normalized_features["latency_p95_ms"] <= 1.0


def test_feature_versioning_hash_determinism():
    names = ["ocr_confidence", "latency_p95_ms", "api_cost_usd"]
    hash1 = FeatureVersionManager.compute_schema_hash(names)
    hash2 = FeatureVersionManager.compute_schema_hash(list(reversed(names)))
    assert hash1 == hash2  # Permutation invariant
