"""
Human productivity impact and labor liberation analyzer.
"""

from typing import Dict, Any
from app.business_value_verification.domain.models import ProductivityImpact


class ProductivityAnalyzer:
    """Calculates annual human hours saved, FTE capacity liberated, and throughput expansion."""

    @staticmethod
    def calculate_productivity(
        annual_doc_volume: int = 125000,
        baseline_mins_per_doc: float = 18.0,
        ai_mins_per_doc: float = 0.5,  # 30 seconds average human touch on exceptions
        hours_per_fte_annual: float = 2000.0,
    ) -> ProductivityImpact:
        baseline_hours = (annual_doc_volume * baseline_mins_per_doc) / 60.0
        ai_hours = (annual_doc_volume * ai_mins_per_doc) / 60.0
        liberated_hours = max(0.0, baseline_hours - ai_hours)
        ftes_liberated = liberated_hours / hours_per_fte_annual
        throughput_multiplier = baseline_mins_per_doc / max(0.01, ai_mins_per_doc)

        return ProductivityImpact(
            baseline_human_hours_annual=baseline_hours,
            ai_human_hours_annual=ai_hours,
            hours_liberated_annual=liberated_hours,
            fte_capacity_liberated=ftes_liberated,
            throughput_expansion_multiplier=throughput_multiplier,
        )
