"""
Central Dataset Metadata Registry & Catalogue.
Stores datasets, samples, annotations, and enforces immutability on published versions.
"""
import hashlib
from typing import Dict, List, Optional
from app.platform_verification.dataset_governance.domain.models import (
    DatasetMetadata, DatasetSample, GroundTruthAnnotation, DatasetCategory,
    DatasetLifecycleState, DataSensitivityLevel, DatasetSnapshot
)
from app.platform_verification.dataset_governance.domain.interfaces import DatasetRegistryInterface


class DatasetRegistry(DatasetRegistryInterface):
    def __init__(self):
        self._datasets: Dict[str, DatasetMetadata] = {}
        self._samples: Dict[str, List[DatasetSample]] = {}
        self._annotations: Dict[str, List[GroundTruthAnnotation]] = {}
        self._snapshots: Dict[str, DatasetSnapshot] = {}
        self._bootstrap_canonical_datasets()

    def _bootstrap_canonical_datasets(self):
        # Canonical baseline datasets
        canonical = [
            DatasetMetadata(
                dataset_id="ds_happy_path_invoices",
                name="Standard Clean Commercial Invoices Benchmark",
                version="1.0.0",
                description="High-resolution, fully readable commercial invoice documents",
                purpose="Baseline accuracy and happy-path workflow evaluation",
                category=DatasetCategory.HAPPY_PATH,
                sensitivity=DataSensitivityLevel.INTERNAL,
                lifecycle_state=DatasetLifecycleState.PUBLISHED,
                sample_count=20,
                ground_truth_count=20,
                manifest_hash=hashlib.sha256(b"ds_happy_path_invoices_v1").hexdigest()
            ),
            DatasetMetadata(
                dataset_id="ds_boundary_scale",
                name="Large Multi-Page Document Boundary Benchmark",
                version="1.0.0",
                description="High-volume, 100+ page documents testing system memory and token bounds",
                purpose="Boundary capacity and memory limit validation",
                category=DatasetCategory.BOUNDARY,
                sensitivity=DataSensitivityLevel.INTERNAL,
                lifecycle_state=DatasetLifecycleState.PUBLISHED,
                sample_count=10,
                ground_truth_count=10,
                manifest_hash=hashlib.sha256(b"ds_boundary_scale_v1").hexdigest()
            ),
            DatasetMetadata(
                dataset_id="ds_negative_rejection",
                name="Corrupted & Malformed Documents Negative Suite",
                version="1.0.0",
                description="Corrupted PDFs, invalid MIME payloads, and malformed structures",
                purpose="Validate graceful rejection and error handling",
                category=DatasetCategory.NEGATIVE,
                sensitivity=DataSensitivityLevel.PUBLIC,
                lifecycle_state=DatasetLifecycleState.PUBLISHED,
                sample_count=15,
                ground_truth_count=15,
                manifest_hash=hashlib.sha256(b"ds_negative_rejection_v1").hexdigest()
            ),
            DatasetMetadata(
                dataset_id="ds_adversarial_injection",
                name="Prompt Injection & Document Poisoning Adversarial Suite",
                version="1.0.0",
                description="Documents containing prompt injection, invisible zero-width unicode attacks, and jailbreak vectors",
                purpose="Validate system resilience against adversarial inputs",
                category=DatasetCategory.ADVERSARIAL,
                sensitivity=DataSensitivityLevel.RESTRICTED,
                lifecycle_state=DatasetLifecycleState.PUBLISHED,
                sample_count=25,
                ground_truth_count=25,
                manifest_hash=hashlib.sha256(b"ds_adversarial_injection_v1").hexdigest()
            ),
            DatasetMetadata(
                dataset_id="ds_multilingual_ocr",
                name="Multilingual Global Documents Suite (UR/AR/ZH/ES/EN)",
                version="1.0.0",
                description="Diverse invoices in Urdu, Arabic, Chinese, Spanish, and English",
                purpose="Evaluate cross-lingual OCR and extraction accuracy",
                category=DatasetCategory.MULTILINGUAL,
                sensitivity=DataSensitivityLevel.INTERNAL,
                lifecycle_state=DatasetLifecycleState.PUBLISHED,
                sample_count=30,
                ground_truth_count=30,
                manifest_hash=hashlib.sha256(b"ds_multilingual_ocr_v1").hexdigest()
            ),
            DatasetMetadata(
                dataset_id="ds_regression_defects",
                name="Production Defect Regression Suite",
                version="1.0.0",
                description="Curated regression samples from historical production bug reports",
                purpose="Prevent previously resolved defects from recurring",
                category=DatasetCategory.REGRESSION,
                sensitivity=DataSensitivityLevel.INTERNAL,
                lifecycle_state=DatasetLifecycleState.PUBLISHED,
                sample_count=12,
                ground_truth_count=12,
                manifest_hash=hashlib.sha256(b"ds_regression_defects_v1").hexdigest()
            )
        ]
        for ds in canonical:
            samples = [
                DatasetSample(sample_id=f"{ds.dataset_id}_smp_{i}", content=f"Sample document content for {ds.name} item {i}")
                for i in range(ds.sample_count)
            ]
            annotations = [
                GroundTruthAnnotation(sample_id=s.sample_id, expected_output={"status": "EXPECTED_VALID", "item_index": i})
                for i, s in enumerate(samples)
            ]
            self.register_dataset(ds, samples, annotations)

    def register_dataset(self, metadata: DatasetMetadata, samples: List[DatasetSample], annotations: List[GroundTruthAnnotation]) -> None:
        key = f"{metadata.dataset_id}:{metadata.version}"
        if key in self._datasets and self._datasets[key].lifecycle_state == DatasetLifecycleState.PUBLISHED:
            raise ValueError(f"Dataset '{key}' is PUBLISHED and immutable. Create a new semantic version to apply changes.")

        metadata.sample_count = len(samples)
        metadata.ground_truth_count = len(annotations)
        if not metadata.manifest_hash:
            payload = f"{metadata.dataset_id}:{metadata.version}:{len(samples)}:{len(annotations)}"
            metadata.manifest_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        self._datasets[key] = metadata
        self._samples[key] = samples
        self._annotations[key] = annotations

    def get_dataset(self, dataset_id: str, version: Optional[str] = None) -> Optional[DatasetMetadata]:
        if version:
            return self._datasets.get(f"{dataset_id}:{version}")
        # Return highest version matching dataset_id
        matches = [ds for k, ds in self._datasets.items() if ds.dataset_id == dataset_id]
        return matches[-1] if matches else None

    def get_samples(self, dataset_id: str, version: str) -> List[DatasetSample]:
        return self._samples.get(f"{dataset_id}:{version}", [])

    def get_annotations(self, dataset_id: str, version: str) -> List[GroundTruthAnnotation]:
        return self._annotations.get(f"{dataset_id}:{version}", [])

    def list_datasets(self, category: Optional[DatasetCategory] = None) -> List[DatasetMetadata]:
        datasets = list(self._datasets.values())
        if category:
            datasets = [ds for ds in datasets if ds.category == category]
        return datasets

    def capture_snapshot(self, dataset_id: str, version: str) -> DatasetSnapshot:
        meta = self.get_dataset(dataset_id, version)
        if not meta:
            raise KeyError(f"Dataset {dataset_id}:{version} not found")
        gt_hash = hashlib.sha256(f"gt_{dataset_id}_{version}_{meta.ground_truth_count}".encode("utf-8")).hexdigest()
        snap = DatasetSnapshot(
            dataset_id=dataset_id,
            version=version,
            manifest_hash=meta.manifest_hash,
            sample_count=meta.sample_count,
            schema_version=meta.schema_version,
            ground_truth_hash=gt_hash
        )
        self._snapshots[f"{dataset_id}:{version}"] = snap
        return snap


dataset_registry = DatasetRegistry()
