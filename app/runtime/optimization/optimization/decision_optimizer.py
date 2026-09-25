"""
Decision Optimizer for Phase 13.6 (ARIA-EOP).
Selects optimal discrete and continuous decision paths for worker allocation, retry policies, and memory cache reuse.
"""

from typing import List
from pydantic import BaseModel, Field


class OptimizationDecision(BaseModel):
    decision_type: str
    selected_option: str
    alternative_options: List[str] = Field(default_factory=list)
    expected_gain_pct: float = 14.5
    rationale: str


class DecisionOptimizer:
    """
    Optimizes micro-level execution decisions (e.g. cache reuse vs fresh extraction).
    """

    @classmethod
    def optimize_memory_decision(cls, cache_similarity: float, recompute_cost_usd: float) -> OptimizationDecision:
        if cache_similarity > 0.90:
            return OptimizationDecision(
                decision_type="MEMORY_REUSE",
                selected_option="USE_CACHED_SCHEMA",
                alternative_options=["FULL_RECOMPUTE", "HYBRID_MERGE"],
                expected_gain_pct=85.0,
                rationale=f"High semantic cache similarity ({cache_similarity*100:.1f}%) saves ${recompute_cost_usd:.4f} USD.",
            )
        return OptimizationDecision(
            decision_type="MEMORY_REUSE",
            selected_option="FULL_RECOMPUTE",
            alternative_options=["USE_CACHED_SCHEMA"],
            expected_gain_pct=12.0,
            rationale="Cache similarity below threshold; fresh extraction ensures zero drift.",
        )
