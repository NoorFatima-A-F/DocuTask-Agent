"""
Interfaces and Contracts for Enterprise Verification Dataset Architecture.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.platform_verification.dataset_governance.domain.models import (
    DatasetMetadata, DatasetSample, GroundTruthAnnotation, DatasetQualityReport,
    DatasetCategory
)


class DatasetRegistryInterface(ABC):
    @abstractmethod
    def register_dataset(self, metadata: DatasetMetadata, samples: List[DatasetSample], annotations: List[GroundTruthAnnotation]) -> None:
        pass

    @abstractmethod
    def get_dataset(self, dataset_id: str, version: Optional[str] = None) -> Optional[DatasetMetadata]:
        pass

    @abstractmethod
    def list_datasets(self, category: Optional[DatasetCategory] = None) -> List[DatasetMetadata]:
        pass


class DatasetValidatorInterface(ABC):
    @abstractmethod
    def validate_dataset(self, metadata: DatasetMetadata, samples: List[DatasetSample]) -> Tuple[bool, List[str]]:
        pass


class DatasetQualityEngineInterface(ABC):
    @abstractmethod
    def evaluate_quality(self, dataset_id: str, samples: List[DatasetSample], annotations: List[GroundTruthAnnotation]) -> DatasetQualityReport:
        pass


class DatasetLineageTrackerInterface(ABC):
    @abstractmethod
    def record_lineage(self, dataset_id: str, version: str, source: str, transformation: str) -> None:
        pass


class DatasetPrivacyEngineInterface(ABC):
    @abstractmethod
    def anonymize_sample(self, sample: DatasetSample) -> DatasetSample:
        pass


class DatasetDistributionInterface(ABC):
    @abstractmethod
    def fetch_samples(self, dataset_id: str, version: str, partition: str = "eval") -> List[DatasetSample]:
        pass
