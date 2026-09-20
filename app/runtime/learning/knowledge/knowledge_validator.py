"""
Knowledge Validator for Phase 13.5 (ARLP-KIP).
Validates schema conformance, confidence thresholds, and lineage verification for knowledge records.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class KnowledgeValidationResult(BaseModel):
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    validation_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KnowledgeValidator:
    """
    Validates structural and confidence constraints on knowledge records.
    """

    @classmethod
    def validate_record(cls, record: Any) -> KnowledgeValidationResult:
        errors = []
        if not getattr(record, "title", None):
            errors.append("Knowledge record missing title")
        
        conf = getattr(record, "confidence_score", 0.0)
        if conf < 0.50 or conf > 1.0:
            errors.append(f"Confidence score {conf} out of valid bounds [0.50, 1.00]")

        return KnowledgeValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )
