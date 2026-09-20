"""
Historical Critic for Multi-Critic Reflection System.
Cross-examines extracted outputs against historical episodic records and semantic vendor baselines.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.agents.memory.intelligence.episodic_memory import EpisodicMemory
from app.agents.memory.intelligence.semantic_memory import SemanticMemory
from app.agents.reflection.critics.rule_critic import CritiqueFeedback

logger = logging.getLogger(__name__)


class HistoricalCritic:
    """Evaluates plausibility based on learned historical priors and past episodes."""

    def __init__(
        self,
        episodic_memory: Optional[EpisodicMemory] = None,
        semantic_memory: Optional[SemanticMemory] = None,
    ) -> None:
        self.episodic_memory = episodic_memory
        self.semantic_memory = semantic_memory

    def evaluate(self, extracted_data: Dict[str, Any], vendor_name: Optional[str] = None) -> CritiqueFeedback:
        """Compares values against historical norms and vendor profiles."""
        issues: List[str] = []
        suggestions: List[str] = []
        score = 1.0

        vendor = vendor_name or extracted_data.get("vendor_name")
        if not vendor:
            return CritiqueFeedback(
                critic_name="HistoricalCritic",
                score=0.9,
                passed=True,
                issues=["Vendor name not provided for historical lookup"],
                suggestions=[],
            )

        # 1. Semantic Memory Check (Vendor Profiles)
        if self.semantic_memory:
            facts_with_scores = self.semantic_memory.retrieve_relevant_facts(query=str(vendor), min_score=0.3)
            facts = [f for f, _ in facts_with_scores]
            if facts:
                # Check for known tax ID
                tax_id_fact = next((f for f in facts if f.predicate in ("tax_id", "vat_id")), None)
                if tax_id_fact and "tax_id" in extracted_data:
                    extracted_tax = str(extracted_data["tax_id"]).strip()
                    expected_tax = str(tax_id_fact.fact_value).strip()
                    if extracted_tax != expected_tax:
                        issues.append(
                            f"Extracted tax ID '{extracted_tax}' does not match historical master record '{expected_tax}'"
                        )
                        suggestions.append(f"Verify tax ID: master record suggests '{expected_tax}'.")
                        score -= 0.25

        # 2. Episodic Memory Check (Outlier Detection)
        if self.episodic_memory:
            episodes_with_scores = self.episodic_memory.retrieve_relevant_episodes(query=str(vendor), top_k=5)
            past_episodes = [ep for ep, _ in episodes_with_scores]
            # If past successful episodes exist for this vendor, compare amounts
            total_amt = extracted_data.get("total_amount")
            if past_episodes and total_amt is not None:
                try:
                    curr_val = float(str(total_amt).replace("$", "").replace(",", "").strip())
                    past_amounts = []
                    for ep in past_episodes:
                        val = ep.metadata.get("total_amount")
                        if val is not None:
                            past_amounts.append(float(str(val).replace("$", "").replace(",", "").strip()))

                    if past_amounts:
                        avg_amt = sum(past_amounts) / len(past_amounts)
                        # Flag severe outlier (e.g. 10x average)
                        if curr_val > avg_amt * 10.0 or (avg_amt > 100.0 and curr_val < avg_amt * 0.05):
                            issues.append(
                                f"Extracted amount ${curr_val:.2f} is a significant statistical outlier compared to vendor average ${avg_amt:.2f}"
                            )
                            suggestions.append("Verify OCR decimal point placement.")
                            score -= 0.20
                except Exception:
                    pass

        final_score = max(0.0, min(1.0, score))
        return CritiqueFeedback(
            critic_name="HistoricalCritic",
            score=round(final_score, 4),
            passed=final_score >= 0.80 and len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
        )
