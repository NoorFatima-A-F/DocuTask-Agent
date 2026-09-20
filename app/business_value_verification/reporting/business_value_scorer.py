"""
Master Business Value and Enterprise Operational Impact Scorer.
"""

from typing import Dict, Any
from app.business_value_verification.domain.models import MasterBusinessValueScore


class BusinessValueScorer:
    """Calculates weighted composite score across Automation (25%), ROI (30%), Efficiency (25%), and Adoption (20%)."""

    WEIGHTS = {
        "automation": 0.25,
        "roi": 0.30,
        "efficiency": 0.25,
        "adoption": 0.20,
    }

    @classmethod
    def calculate_score(
        cls,
        automation_score: float = 100.0,
        roi_score: float = 100.0,
        efficiency_score: float = 100.0,
        adoption_score: float = 100.0,
    ) -> MasterBusinessValueScore:
        composite = (
            (automation_score * cls.WEIGHTS["automation"])
            + (roi_score * cls.WEIGHTS["roi"])
            + (efficiency_score * cls.WEIGHTS["efficiency"])
            + (adoption_score * cls.WEIGHTS["adoption"])
        )

        grade = "A+"
        if composite < 80.0:
            grade = "C"
        elif composite < 90.0:
            grade = "B"
        elif composite < 95.0:
            grade = "A"

        status = (
            "ENTERPRISE VALUE VALIDATED"
            if composite >= 95.0
            else "PROVISIONAL VALUE"
        )

        return MasterBusinessValueScore(
            automation_score=automation_score,
            roi_score=roi_score,
            efficiency_score=efficiency_score,
            adoption_score=adoption_score,
            overall_business_score=composite,
            grade=grade,
            validation_status=status,
        )
