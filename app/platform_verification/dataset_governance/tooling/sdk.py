"""
Dataset Authoring & Validation Developer SDK.
"""
from typing import Any, Dict, List
from app.platform_verification.dataset_governance.domain.models import (
    DatasetMetadata, DatasetSample, GroundTruthAnnotation, DatasetCategory,
    DatasetLifecycleState, DatasetQualityReport
)
from app.platform_verification.dataset_governance.core.registry import dataset_registry
from app.platform_verification.dataset_governance.core.validator import dataset_validator
from app.platform_verification.dataset_governance.core.quality_engine import dataset_quality_engine


class DatasetDeveloperSDK:
    @staticmethod
    def create_dataset_asset(
        dataset_id: str,
        name: str,
        version: str,
        description: str,
        category: DatasetCategory,
        samples_raw: List[Dict[str, Any]],
        ground_truth_raw: List[Dict[str, Any]]
    ) -> DatasetMetadata:
        meta = DatasetMetadata(
            dataset_id=dataset_id,
            name=name,
            version=version,
            description=description,
            purpose=f"Verification evaluations for {name}",
            category=category,
            lifecycle_state=DatasetLifecycleState.CREATED
        )
        samples = [
            DatasetSample(sample_id=s.get("id", f"{dataset_id}_{i}"), content=s["content"], language=s.get("language", "en"))
            for i, s in enumerate(samples_raw)
        ]
        annotations = [
            GroundTruthAnnotation(sample_id=a["sample_id"], expected_output=a.get("expected_output", {}))
            for a in ground_truth_raw
        ]

        # Validate
        is_valid, errors = dataset_validator.validate_dataset(meta, samples)
        if not is_valid:
            raise ValueError(f"Dataset validation failed: {errors}")

        dataset_registry.register_dataset(meta, samples, annotations)
        return meta

    @staticmethod
    def evaluate_quality(dataset_id: str, version: str) -> DatasetQualityReport:
        samples = dataset_registry.get_samples(dataset_id, version)
        annotations = dataset_registry.get_annotations(dataset_id, version)
        return dataset_quality_engine.evaluate_quality(dataset_id, samples, annotations)


dataset_sdk = DatasetDeveloperSDK()
