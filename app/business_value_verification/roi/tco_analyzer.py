"""
3-Year Total Cost of Ownership (TCO) Comparative Analyzer.
"""

from typing import Dict, Any
from app.business_value_verification.domain.models import TCOComparison


class TCOAnalyzer:
    """Compares 3-Year Total Cost of Ownership between human operations and autonomous AI platform."""

    @staticmethod
    def calculate_3yr_tco(
        annual_docs: int = 120000,
        labor_cost_per_doc: float = 7.46,
        labor_inflation_rate: float = 0.05,
        ai_fixed_annual_platform_fee: float = 24000.0,
        ai_token_infra_cost_per_doc: float = 0.0080,
    ) -> TCOComparison:
        # Year 1
        y1_human = annual_docs * labor_cost_per_doc
        y1_ai = (annual_docs * ai_token_infra_cost_per_doc) + ai_fixed_annual_platform_fee

        # Year 2 (5% labor inflation, 10% AI token price drop)
        y2_human = y1_human * (1.0 + labor_inflation_rate)
        y2_ai = (annual_docs * (ai_token_infra_cost_per_doc * 0.90)) + ai_fixed_annual_platform_fee

        # Year 3 (additional 5% labor inflation, additional 10% AI token price drop)
        y3_human = y2_human * (1.0 + labor_inflation_rate)
        y3_ai = (annual_docs * (ai_token_infra_cost_per_doc * 0.81)) + ai_fixed_annual_platform_fee

        cum_human = y1_human + y2_human + y3_human
        cum_ai = y1_ai + y2_ai + y3_ai
        net_savings_3yr = cum_human - cum_ai

        return TCOComparison(
            year_1_human_tco=y1_human,
            year_1_ai_tco=y1_ai,
            year_2_human_tco=y2_human,
            year_2_ai_tco=y2_ai,
            year_3_human_tco=y3_human,
            year_3_ai_tco=y3_ai,
            cumulative_3yr_human_tco=cum_human,
            cumulative_3yr_ai_tco=cum_ai,
            cumulative_3yr_net_savings=net_savings_3yr,
            scaling_elasticity="Near-Zero Marginal Labor Scaling Cost (O(1) vs O(N))",
        )
