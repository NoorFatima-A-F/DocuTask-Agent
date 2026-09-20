"""
Enterprise Performance, Reliability & Readiness Score Calculator.
"""

from typing import Dict, Any
from app.performance_verification.domain.models import EnterpriseReadinessScore


class ReadinessScorer:
    """Calculates weighted composite readiness score across Performance, Reliability, Efficiency, and Observability."""

    WEIGHTS = {
        "performance": 0.30,
        "reliability": 0.35,
        "efficiency": 0.20,
        "observability": 0.15,
    }

    @classmethod
    def calculate_score(
        cls,
        perf_score: float = 100.0,
        rel_score: float = 100.0,
        eff_score: float = 100.0,
        obs_score: float = 100.0,
    ) -> EnterpriseReadinessScore:
        composite = (
            (perf_score * cls.WEIGHTS["performance"])
            + (rel_score * cls.WEIGHTS["reliability"])
            + (eff_score * cls.WEIGHTS["efficiency"])
            + (obs_score * cls.WEIGHTS["observability"])
        )

        grade = "A+"
        if composite < 80.0:
            grade = "C"
        elif composite < 90.0:
            grade = "B"
        elif composite < 95.0:
            grade = "A"

        cert_status = (
            "ENTERPRISE PRODUCTION HARDENED"
            if composite >= 95.0
            else "PROVISIONAL DEPLOYMENT"
        )

        return EnterpriseReadinessScore(
            performance_score=perf_score,
            reliability_score=rel_score,
            efficiency_score=eff_score,
            observability_score=obs_score,
            overall_readiness_score=composite,
            grade=grade,
            certification_status=cert_status,
        )
