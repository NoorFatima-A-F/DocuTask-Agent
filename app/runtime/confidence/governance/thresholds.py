"""
Confidence Thresholds Specification for Phase 13.3 (ASCE-CGP).
Configurable industry and SLA confidence thresholds.
"""

from typing import Dict


class ConfidenceThresholds:
    """
    Standard confidence thresholds per domain.
    """

    THRESHOLDS: Dict[str, float] = {
        "FINANCIAL_AUTOMATION": 0.95,
        "MEDICAL_RECORDS": 0.98,
        "LEGAL_CONTRACTS": 0.92,
        "STANDARD_EXTRACTION": 0.85,
        "EXPERIMENTAL": 0.70,
    }

    @classmethod
    def get_threshold(cls, domain: str = "FINANCIAL_AUTOMATION") -> float:
        return cls.THRESHOLDS.get(domain, cls.THRESHOLDS["STANDARD_EXTRACTION"])
