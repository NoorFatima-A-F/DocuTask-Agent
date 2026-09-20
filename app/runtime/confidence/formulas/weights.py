"""
Dynamic Weight Management for Phase 13.3 (ASCE-CGP).
Policy-based dynamic weights for different mission and document types (Financial, Medical, Legal, Standard).
"""

from typing import Dict


class ConfidenceWeightPolicy:
    """
    Provides policy-driven weight matrices for confidence calculations.
    """

    POLICIES: Dict[str, Dict[str, float]] = {
        "FINANCIAL_AUDIT": {
            "validation_constraint_satisfaction": 0.35,
            "ocr_mean_confidence": 0.20,
            "extraction_cross_field_consistency": 0.20,
            "evidence_hash_integrity": 0.15,
            "planner_dag_efficiency": 0.10,
        },
        "MEDICAL_RECORD": {
            "validation_constraint_satisfaction": 0.40,
            "ocr_mean_confidence": 0.30,
            "evidence_hash_integrity": 0.20,
            "extraction_cross_field_consistency": 0.10,
        },
        "STANDARD": {
            "ocr_mean_confidence": 0.25,
            "ocr_coverage_ratio": 0.15,
            "extraction_schema_completeness": 0.20,
            "validation_constraint_satisfaction": 0.25,
            "evidence_hash_integrity": 0.15,
        },
    }

    @classmethod
    def get_weights(cls, policy_name: str = "FINANCIAL_AUDIT") -> Dict[str, float]:
        return cls.POLICIES.get(policy_name, cls.POLICIES["STANDARD"])
