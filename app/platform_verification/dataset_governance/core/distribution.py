"""
Dataset Distribution and Delivery Service.
Provides streaming, partition retrieval, and access control.
"""
from typing import List
from app.platform_verification.dataset_governance.domain.models import DatasetSample
from app.platform_verification.dataset_governance.domain.interfaces import DatasetDistributionInterface
from app.platform_verification.dataset_governance.core.registry import dataset_registry


class DatasetDistributionService(DatasetDistributionInterface):
    def fetch_samples(self, dataset_id: str, version: str, partition: str = "eval") -> List[DatasetSample]:
        all_samples = dataset_registry.get_samples(dataset_id, version)
        if partition == "ALL":
            return all_samples
        return [s for s in all_samples if s.partition == partition or partition == "eval"]


dataset_distribution = DatasetDistributionService()
