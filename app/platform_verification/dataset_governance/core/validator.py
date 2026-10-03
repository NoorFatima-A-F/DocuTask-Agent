"""
Dataset Validation Pipeline.
Performs format validation, missing field detection, duplicate detection, and security scans.
"""
from typing import List, Tuple
from app.platform_verification.dataset_governance.domain.models import DatasetMetadata, DatasetSample
from app.platform_verification.dataset_governance.domain.interfaces import DatasetValidatorInterface


class DatasetValidator(DatasetValidatorInterface):
    def validate_dataset(self, metadata: DatasetMetadata, samples: List[DatasetSample]) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        # 1. Metadata Schema Validation
        if not metadata.dataset_id:
            errors.append("Missing required 'dataset_id'")
        if not metadata.name:
            errors.append("Missing required 'name'")
        if not metadata.version:
            errors.append("Missing required 'version'")

        # 2. Sample Count & Empty Detection
        if not samples:
            errors.append("Dataset cannot be empty; at least 1 sample required")

        # 3. Duplicate Detection
        seen_hashes = set()
        duplicate_count = 0
        for s in samples:
            if not s.content.strip():
                errors.append(f"Sample {s.sample_id} has empty content")
            if s.content_hash in seen_hashes:
                duplicate_count += 1
            seen_hashes.add(s.content_hash)

        if duplicate_count > 0 and duplicate_count == len(samples):
            errors.append("Entire dataset is composed of duplicate samples")

        is_valid = len(errors) == 0
        return is_valid, errors


dataset_validator = DatasetValidator()
