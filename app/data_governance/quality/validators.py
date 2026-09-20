"""Data Quality Validators (Phase 8B)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class QualityValidationResult(BaseModel):
    """Result from a specific quality check."""
    dimension: str  # COMPLETENESS, ACCURACY, CONSISTENCY, FRESHNESS, VALIDITY
    is_passed: bool
    score: float  # 0.0 to 1.0
    details: str = ""


class DataQualityValidators:
    """Evaluates data quality across 5 foundational dimensions."""

    @staticmethod
    def validate_completeness(record: Dict[str, Any], required_fields: List[str]) -> QualityValidationResult:
        """Verify presence and non-emptiness of mandatory fields."""
        if not required_fields:
            return QualityValidationResult(dimension="COMPLETENESS", is_passed=True, score=1.0)

        present = sum(1 for f in required_fields if record.get(f) is not None and str(record.get(f)).strip() != "")
        score = present / len(required_fields)
        return QualityValidationResult(
            dimension="COMPLETENESS",
            is_passed=score == 1.0,
            score=score,
            details=f"Present {present}/{len(required_fields)} required fields",
        )

    @staticmethod
    def validate_freshness(record_timestamp: datetime, max_age_days: int = 30) -> QualityValidationResult:
        """Verify data freshness within acceptable staleness threshold."""
        now = datetime.now(timezone.utc)
        age_days = (now - record_timestamp).total_seconds() / 86400.0
        if age_days <= max_age_days:
            score = 1.0 - (age_days / max_age_days * 0.3)  # Score between 0.7 and 1.0
            return QualityValidationResult(dimension="FRESHNESS", is_passed=True, score=score, details=f"Age: {age_days:.1f} days")
        else:
            score = max(0.0, 1.0 - (age_days / (max_age_days * 3)))
            return QualityValidationResult(dimension="FRESHNESS", is_passed=False, score=score, details=f"Data is stale: {age_days:.1f} days old")

    @staticmethod
    def validate_validity(record: Dict[str, Any], schema_types: Dict[str, type]) -> QualityValidationResult:
        """Validate field value types against expected types."""
        if not schema_types:
            return QualityValidationResult(dimension="VALIDITY", is_passed=True, score=1.0)

        valid_count = 0
        for field, expected_type in schema_types.items():
            val = record.get(field)
            if val is None or isinstance(val, expected_type):
                valid_count += 1

        score = valid_count / len(schema_types)
        return QualityValidationResult(
            dimension="VALIDITY",
            is_passed=score == 1.0,
            score=score,
            details=f"Valid types: {valid_count}/{len(schema_types)}",
        )
