"""
Master Unified Runtime Facade for Enterprise Verification Dataset Architecture & Governance.
"""
from typing import Any, Dict, List, Optional
from app.platform_verification.dataset_governance.domain.models import (
    DatasetMetadata, DatasetSample, DatasetQualityReport,
    DatasetSnapshot, DatasetCategory
)
from app.platform_verification.dataset_governance.core.registry import dataset_registry
from app.platform_verification.dataset_governance.core.quality_engine import dataset_quality_engine
from app.platform_verification.dataset_governance.core.distribution import dataset_distribution
from app.platform_verification.dataset_governance.core.regression_generator import regression_generator


class EnterpriseDatasetGovernanceRuntime:
    """Unified Facade for verification dataset registry, quality evaluation, lineage, snapshots, and delivery."""

    def get_dataset(self, dataset_id: str, version: Optional[str] = None) -> Optional[DatasetMetadata]:
        return dataset_registry.get_dataset(dataset_id, version)

    def list_datasets_by_category(self, category: DatasetCategory) -> List[DatasetMetadata]:
        return dataset_registry.list_datasets(category=category)

    def fetch_evaluation_samples(self, dataset_id: str, version: str) -> List[DatasetSample]:
        return dataset_distribution.fetch_samples(dataset_id=dataset_id, version=version, partition="eval")

    def capture_dataset_snapshot(self, dataset_id: str, version: str) -> DatasetSnapshot:
        return dataset_registry.capture_snapshot(dataset_id, version)

    def evaluate_dataset_quality(self, dataset_id: str, version: str) -> DatasetQualityReport:
        samples = dataset_registry.get_samples(dataset_id, version)
        annotations = dataset_registry.get_annotations(dataset_id, version)
        return dataset_quality_engine.evaluate_quality(dataset_id, samples, annotations)

    def generate_regression_sample(self, defect_id: str, content: str, remediation: Dict[str, Any]) -> DatasetSample:
        return regression_generator.create_regression_sample_from_defect(defect_id, content, remediation)


dataset_governance_runtime = EnterpriseDatasetGovernanceRuntime()
