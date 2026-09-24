"""
Comprehensive Unit & Integration Test Suite for Part 1.3:
Enterprise Verification Dataset Architecture & Test Data Governance.
"""
import pytest
from app.platform_verification.dataset_governance.domain.models import (
    DatasetCategory, DatasetLifecycleState, DatasetSample,
    DatasetMetadata
)
from app.platform_verification.dataset_governance.core.registry import dataset_registry
from app.platform_verification.dataset_governance.core.validator import dataset_validator
from app.platform_verification.dataset_governance.core.privacy_engine import dataset_privacy_engine
from app.platform_verification.dataset_governance.core.security_scanner import dataset_security_scanner
from app.platform_verification.dataset_governance.runtime.dataset_governance_runtime import dataset_governance_runtime


def test_canonical_9_categories_dataset_registry():
    datasets = dataset_registry.list_datasets()
    assert len(datasets) >= 6

    happy_ds = dataset_registry.get_dataset("ds_happy_path_invoices", "1.0.0")
    assert happy_ds is not None
    assert happy_ds.category == DatasetCategory.HAPPY_PATH
    assert happy_ds.lifecycle_state == DatasetLifecycleState.PUBLISHED
    assert len(happy_ds.manifest_hash) == 64

    # Multilingual
    multi_ds = dataset_registry.get_dataset("ds_multilingual_ocr", "1.0.0")
    assert multi_ds.category == DatasetCategory.MULTILINGUAL
    assert multi_ds.sample_count >= 20


def test_dataset_immutability_on_published_state():
    ds = dataset_registry.get_dataset("ds_happy_path_invoices", "1.0.0")
    assert ds.lifecycle_state == DatasetLifecycleState.PUBLISHED

    # Attempt to overwrite published dataset
    with pytest.raises(ValueError) as exc:
        dataset_registry.register_dataset(ds, [], [])
    assert "is PUBLISHED and immutable" in str(exc.value)


def test_dataset_quality_scoring_framework():
    report = dataset_governance_runtime.evaluate_dataset_quality("ds_happy_path_invoices", "1.0.0")
    assert report.composite_quality_score >= 0.85
    assert report.is_acceptable is True
    assert report.accuracy_score >= 0.90
    assert report.completeness_score == 1.0


def test_dataset_validation_pipeline():
    meta = DatasetMetadata(
        dataset_id="test_custom_ds",
        name="Test Custom Dataset",
        version="1.0.0",
        description="Testing validation rules",
        purpose="Unit testing",
        category=DatasetCategory.SYNTHETIC
    )
    samples = [
        DatasetSample(sample_id="s1", content="Sample content 1"),
        DatasetSample(sample_id="s2", content="Sample content 2")
    ]
    is_valid, errors = dataset_validator.validate_dataset(meta, samples)
    assert is_valid is True
    assert len(errors) == 0

    # Empty samples validation failure
    is_valid_empty, errors_empty = dataset_validator.validate_dataset(meta, [])
    assert is_valid_empty is False
    assert any("at least 1 sample required" in e for e in errors_empty)


def test_privacy_preservation_pii_masking():
    dirty_sample = DatasetSample(
        sample_id="pii_sample_01",
        content="Customer John Doe, email john.doe@enterprise.com, phone 555-123-4567, SSN 123-45-6789 paid $500."
    )
    clean_sample = dataset_privacy_engine.anonymize_sample(dirty_sample)
    assert "[REDACTED_EMAIL]" in clean_sample.content
    assert "[REDACTED_PHONE]" in clean_sample.content
    assert "[REDACTED_SSN]" in clean_sample.content
    assert "john.doe@enterprise.com" not in clean_sample.content
    assert clean_sample.metadata.get("is_anonymized") is True


def test_security_poisoning_scanner():
    clean_sample = DatasetSample(sample_id="c1", content="Standard invoice payload text")
    poisoned_sample = DatasetSample(sample_id="p1", content="Invoice with attack <script>alert(1)</script>")

    is_clean, threats = dataset_security_scanner.scan_samples([clean_sample, poisoned_sample])
    assert is_clean is False
    assert len(threats) >= 1
    assert "Security threat detected" in threats[0]


def test_defect_regression_generator_and_snapshots():
    defect_sample = dataset_governance_runtime.generate_regression_sample(
        defect_id="BUG-2026-9081",
        content="Invoice with zero-width spaces breaking regex tokenizer",
        remediation={"fixed_total": 1250.0, "tokenizer_mode": "UNICODE_NORMALIZED"}
    )
    assert defect_sample.sample_id == "reg_smp_BUG-2026-9081"

    # Capture snapshot for verification run
    snap = dataset_governance_runtime.capture_dataset_snapshot("ds_happy_path_invoices", "1.0.0")
    assert snap.dataset_id == "ds_happy_path_invoices"
    assert len(snap.manifest_hash) == 64
    assert len(snap.ground_truth_hash) == 64
