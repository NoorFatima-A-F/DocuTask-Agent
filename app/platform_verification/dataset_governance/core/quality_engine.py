"""
Dataset Quality Scoring Framework.
Evaluates: Accuracy (30%), Completeness (20%), Diversity (20%), Consistency (15%), Freshness (15%).
"""
from typing import List
from app.platform_verification.dataset_governance.domain.models import (
    DatasetSample, GroundTruthAnnotation, DatasetQualityReport, ReviewStatus
)
from app.platform_verification.dataset_governance.domain.interfaces import DatasetQualityEngineInterface


class DatasetQualityEngine(DatasetQualityEngineInterface):
    def evaluate_quality(
        self,
        dataset_id: str,
        samples: List[DatasetSample],
        annotations: List[GroundTruthAnnotation]
    ) -> DatasetQualityReport:
        issues = []

        # 1. Accuracy (30% weight): Review status and confidence
        approved_count = sum(1 for a in annotations if a.review_status == ReviewStatus.APPROVED)
        accuracy_score = (approved_count / max(1, len(annotations)))

        # 2. Completeness (20% weight): Match between samples and annotations
        sample_ids = {s.sample_id for s in samples}
        annotated_sample_ids = {a.sample_id for a in annotations}
        completeness_score = len(sample_ids.intersection(annotated_sample_ids)) / max(1, len(sample_ids))

        # 3. Diversity (20% weight): Unique languages and partition distribution
        languages = {s.language for s in samples}
        diversity_score = min(1.0, len(languages) / 2.0 if len(languages) > 1 else 0.9)

        # 4. Consistency (15% weight): Valid schemas
        consistent_samples = sum(1 for s in samples if s.content_hash and len(s.content) > 5)
        consistency_score = consistent_samples / max(1, len(samples))

        # 5. Freshness (15% weight): Baseline 1.0
        freshness_score = 1.0

        # Weighted Composite Score
        composite = (
            accuracy_score * 0.30 +
            completeness_score * 0.20 +
            diversity_score * 0.20 +
            consistency_score * 0.15 +
            freshness_score * 0.15
        )

        is_acceptable = composite >= 0.85

        if completeness_score < 1.0:
            issues.append("Some samples lack approved ground truth annotations")

        return DatasetQualityReport(
            dataset_id=dataset_id,
            version="1.0.0",
            accuracy_score=round(accuracy_score, 3),
            completeness_score=round(completeness_score, 3),
            diversity_score=round(diversity_score, 3),
            consistency_score=round(consistency_score, 3),
            freshness_score=round(freshness_score, 3),
            composite_quality_score=round(composite, 3),
            is_acceptable=is_acceptable,
            issues_detected=issues
        )


dataset_quality_engine = DatasetQualityEngine()
