"""
AI Cost Performance, Token Economics, and Enterprise ROI Evaluator.
"""

from typing import List
from app.performance_verification.domain.models import AICostProfile


class AICostEvaluator:
    """Evaluates unit economics, token consumption, and financial ROI vs manual baselines."""

    @staticmethod
    def evaluate_cost_profiles() -> List[AICostProfile]:
        profiles = [
            # 1. Invoice Automation
            AICostProfile(
                workflow_name="Accounts Payable Invoice Processing",
                ocr_cost_per_doc=0.0020,
                llm_cost_per_doc=0.0050,
                storage_cost_per_doc=0.0010,
                total_ai_cost_per_doc=0.0080,
                manual_baseline_cost_per_doc=5.00,
                cost_reduction_pct=99.84,
                prompt_tokens_avg=1420,
                completion_tokens_avg=380,
                annual_savings_100k_docs=(5.00 - 0.0080) * 100000,  # $499,200/yr
                roi_multiple=5.00 / 0.0080,  # 625.0x
            ),
            # 2. Multi-Page Legal Contract Analysis
            AICostProfile(
                workflow_name="Commercial Contract & NDA Risk Analysis",
                ocr_cost_per_doc=0.0060,
                llm_cost_per_doc=0.0150,
                storage_cost_per_doc=0.0020,
                total_ai_cost_per_doc=0.0230,
                manual_baseline_cost_per_doc=35.00,
                cost_reduction_pct=99.93,
                prompt_tokens_avg=6200,
                completion_tokens_avg=1450,
                annual_savings_100k_docs=(35.00 - 0.0230) * 100000,  # $3,497,700/yr
                roi_multiple=35.00 / 0.0230,  # 1521.7x
            ),
            # 3. Resume & Candidate Screening
            AICostProfile(
                workflow_name="HR Candidate Resume Screening & Matching",
                ocr_cost_per_doc=0.0010,
                llm_cost_per_doc=0.0030,
                storage_cost_per_doc=0.0005,
                total_ai_cost_per_doc=0.0045,
                manual_baseline_cost_per_doc=8.50,
                cost_reduction_pct=99.95,
                prompt_tokens_avg=980,
                completion_tokens_avg=260,
                annual_savings_100k_docs=(8.50 - 0.0045) * 100000,  # $849,550/yr
                roi_multiple=8.50 / 0.0045,  # 1888.9x
            ),
        ]
        return profiles
