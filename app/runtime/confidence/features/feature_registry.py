"""
Feature Registry for Phase 13.3 (ASCE-CGP).
Maintains definitions and metadata for all scientific confidence features.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from app.runtime.confidence.models.confidence_dimensions import ConfidenceDimension
from app.runtime.confidence.models.confidence_models import ConfidenceFeatureDefinition


class FeatureRegistry:
    """
    Central repository of all registered confidence features.
    Guarantees no undocumented metrics or untyped numerical inputs enter the confidence engine.
    """

    _registry: Dict[str, ConfidenceFeatureDefinition] = {}

    @classmethod
    def initialize_defaults(cls):
        if cls._registry:
            return

        defaults = [
            # OCR Dimension
            ConfidenceFeatureDefinition(
                name="ocr_mean_confidence",
                description="Arithmetic mean of per-token OCR bounding box probabilities",
                owner="OCR_DEPARTMENT",
                units="PROBABILITY",
                valid_range=[0.0, 1.0],
                normalization_method="IDENTITY",
                source="WORKER_OCR",
                dimension=ConfidenceDimension.OCR,
            ),
            ConfidenceFeatureDefinition(
                name="ocr_coverage_ratio",
                description="Proportion of non-blank document pixels successfully covered by recognized characters",
                owner="OCR_DEPARTMENT",
                units="RATIO",
                valid_range=[0.0, 1.0],
                normalization_method="MIN_MAX",
                source="WORKER_OCR",
                dimension=ConfidenceDimension.OCR,
            ),
            ConfidenceFeatureDefinition(
                name="ocr_language_certainty",
                description="Classifier certainty of detected primary script/language",
                owner="OCR_DEPARTMENT",
                units="PROBABILITY",
                valid_range=[0.0, 1.0],
                normalization_method="IDENTITY",
                source="WORKER_OCR",
                dimension=ConfidenceDimension.OCR,
            ),
            # Extraction Dimension
            ConfidenceFeatureDefinition(
                name="extraction_schema_completeness",
                description="Percentage of required target JSON schema fields successfully populated",
                owner="EXTRACTION_DEPARTMENT",
                units="RATIO",
                valid_range=[0.0, 1.0],
                normalization_method="IDENTITY",
                source="WORKER_EXTRACT",
                dimension=ConfidenceDimension.EXTRACTION,
            ),
            ConfidenceFeatureDefinition(
                name="extraction_cross_field_consistency",
                description="Consistency score between dependent invoice line items and totals",
                owner="EXTRACTION_DEPARTMENT",
                units="PROBABILITY",
                valid_range=[0.0, 1.0],
                normalization_method="IDENTITY",
                source="WORKER_EXTRACT",
                dimension=ConfidenceDimension.EXTRACTION,
            ),
            # Validation Dimension
            ConfidenceFeatureDefinition(
                name="validation_constraint_satisfaction",
                description="Percentage of deterministic business and arithmetic invariants satisfied",
                owner="VALIDATION_DEPARTMENT",
                units="RATIO",
                valid_range=[0.0, 1.0],
                normalization_method="IDENTITY",
                source="VALIDATION_ENGINE",
                dimension=ConfidenceDimension.VALIDATION,
            ),
            # Planner Dimension
            ConfidenceFeatureDefinition(
                name="planner_dag_efficiency",
                description="Ratio of optimal critical path latency to actual executed path latency",
                owner="CHIEF_PLANNER",
                units="RATIO",
                valid_range=[0.0, 1.0],
                normalization_method="MIN_MAX",
                source="PLANNER_RUNTIME",
                dimension=ConfidenceDimension.PLANNER,
            ),
            # Evidence Dimension
            ConfidenceFeatureDefinition(
                name="evidence_hash_integrity",
                description="Cryptographic Merkle tree proof validity score (1.0 = verified, 0.0 = tampered)",
                owner="GOVERNANCE_DEPARTMENT",
                units="BOOLEAN_SCORE",
                valid_range=[0.0, 1.0],
                normalization_method="IDENTITY",
                source="TRUTH_LEDGER",
                dimension=ConfidenceDimension.EVIDENCE,
            ),
        ]

        for feat in defaults:
            cls._registry[feat.name] = feat

    @classmethod
    def register(cls, feature: ConfidenceFeatureDefinition):
        cls._registry[feature.name] = feature

    @classmethod
    def get(cls, name: str) -> Optional[ConfidenceFeatureDefinition]:
        cls.initialize_defaults()
        return cls._registry.get(name)

    @classmethod
    def list_all(cls) -> List[ConfidenceFeatureDefinition]:
        cls.initialize_defaults()
        return list(cls._registry.values())
