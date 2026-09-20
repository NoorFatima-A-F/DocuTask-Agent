"""Data Quality Scoring Engine (Phase 8B)."""

from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.data_governance.quality.validators import QualityValidationResult, DataQualityValidators


class DataQualityReport(BaseModel):
    """Overall Data Quality Assessment Report."""
    asset_id: str
    composite_score: float  # 0.0 to 1.0
    completeness_score: float
    freshness_score: float
    validity_score: float
    is_acceptable: bool
    validation_results: List[QualityValidationResult] = Field(default_factory=list)


class DataQualityScorer:
    """Calculates multidimensional quality scores for data assets."""

    def __init__(
        self,
        completeness_weight: float = 0.40,
        freshness_weight: float = 0.30,
        validity_weight: float = 0.30,
    ):
        self.w_comp = completeness_weight
        self.w_fresh = freshness_weight
        self.w_valid = validity_weight

    def evaluate_quality(
        self,
        asset_id: str,
        record: Dict[str, Any],
        required_fields: List[str],
        record_timestamp: Any,
        schema_types: Dict[str, type],
    ) -> DataQualityReport:
        """Run all quality validations and calculate composite score."""
        comp_res = DataQualityValidators.validate_completeness(record, required_fields)
        fresh_res = DataQualityValidators.validate_freshness(record_timestamp)
        valid_res = DataQualityValidators.validate_validity(record, schema_types)

        composite = (
            self.w_comp * comp_res.score
            + self.w_fresh * fresh_res.score
            + self.w_valid * valid_res.score
        )

        return DataQualityReport(
            asset_id=asset_id,
            composite_score=round(composite, 4),
            completeness_score=round(comp_res.score, 4),
            freshness_score=round(fresh_res.score, 4),
            validity_score=round(valid_res.score, 4),
            is_acceptable=composite >= 0.70,
            validation_results=[comp_res, fresh_res, valid_res],
        )
