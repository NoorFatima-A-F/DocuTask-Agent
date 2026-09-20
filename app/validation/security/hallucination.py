"""
Hallucination Evaluation & Factuality Benchmarking Subsystem.
Measures hallucination rate, unsupported claim rate, and fabricated field rate across sparse or conflicting documents.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field
from app.core.logging import logger


class HallucinationMetrics(BaseModel):
    """Metrics quantifying AI hallucination behavior."""
    total_requested_fields: int
    missing_data_fields: int
    fabricated_fields: int
    unsupported_claims: int
    hallucination_rate: float
    unsupported_claim_rate: float
    fabricated_field_rate: float


class HallucinationEvaluator:
    """Evaluator assessing hallucination and factuality performance."""

    @classmethod
    def evaluate_hallucinations(
        cls,
        actual_extraction: Dict[str, Any],
        ground_truth: Dict[str, Any],
        raw_ocr_text: str
    ) -> HallucinationMetrics:
        """
        Calculates hallucination, unsupported claim, and fabricated field rates.
        """
        total_fields = len(ground_truth) if ground_truth else 1
        missing_count = 0
        fabricated_count = 0
        unsupported_count = 0

        for key, expected_val in ground_truth.items():
            actual_val = actual_extraction.get(key)

            if expected_val is None:
                # Field was absent from document
                missing_count += 1
                if actual_val is not None and actual_val != "" and actual_val != []:
                    # AI fabricated a value for an absent field!
                    fabricated_count += 1
                    logger.warning(f"Hallucination detected for key '{key}': Fabricated '{actual_val}' for null ground truth.")

            elif actual_val is not None:
                # Check if extracted string value appears anywhere in raw OCR text context
                str_val = str(actual_val).strip()
                if len(str_val) > 2 and str_val.lower() not in raw_ocr_text.lower():
                    unsupported_count += 1

        hallucination_rate = round(fabricated_count / total_fields, 4)
        unsupported_rate = round(unsupported_count / total_fields, 4)
        fabricated_rate = round(fabricated_count / total_fields, 4)

        return HallucinationMetrics(
            total_requested_fields=total_fields,
            missing_data_fields=missing_count,
            fabricated_fields=fabricated_count,
            unsupported_claims=unsupported_count,
            hallucination_rate=hallucination_rate,
            unsupported_claim_rate=unsupported_rate,
            fabricated_field_rate=fabricated_rate
        )
