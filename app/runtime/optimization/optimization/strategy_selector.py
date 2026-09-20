"""
Strategy Selector for Phase 13.6 (ARIA-EOP).
Evaluates candidate execution strategies under multi-objective scalarization and selects Pareto-optimal plans.
"""

from typing import Dict, Any, List, Optional
import uuid
from pydantic import BaseModel, Field


class CandidateExecutionStrategy(BaseModel):
    strategy_id: str = Field(default_factory=lambda: f"strat_{uuid.uuid4().hex[:8]}")
    strategy_name: str
    target_model: str = "gemini-1.5-flash"
    ocr_engine: str = "TESSERACT_FAST"
    worker_concurrency: int = 4
    estimated_cost_usd: float = 0.0025
    estimated_latency_ms: float = 1450.0
    estimated_confidence: float = 0.962
    estimated_energy_joules: float = 12.4
    utility_score: float = 0.0
    is_pareto_optimal: bool = True


class StrategySelector:
    """
    Ranks and selects candidate execution strategies using weighted multi-objective utility functions.
    """

    @classmethod
    def score_and_select(
        cls,
        candidates: List[CandidateExecutionStrategy],
        objective: str = "BALANCED_UTILITY",
        w_cost: float = 0.25,
        w_speed: float = 0.35,
        w_conf: float = 0.40,
    ) -> CandidateExecutionStrategy:
        if not candidates:
            return CandidateExecutionStrategy(
                strategy_name="Default Fallback Strategy",
                target_model="gemini-1.5-flash",
                ocr_engine="TESSERACT_FAST",
                worker_concurrency=4,
                estimated_cost_usd=0.003,
                estimated_latency_ms=1800.0,
                estimated_confidence=0.96,
                utility_score=0.92,
            )

        best_cand = candidates[0]
        max_utility = -1.0

        for cand in candidates:
            # Normalize components
            cost_norm = max(0.0, 1.0 - (cand.estimated_cost_usd / 0.02))
            speed_norm = max(0.0, 1.0 - (cand.estimated_latency_ms / 5000.0))
            conf_norm = cand.estimated_confidence

            if objective == "MINIMIZE_COST":
                u = 0.85 * cost_norm + 0.05 * speed_norm + 0.10 * conf_norm
            elif objective == "MINIMIZE_LATENCY":
                u = 0.05 * cost_norm + 0.85 * speed_norm + 0.10 * conf_norm
            elif objective == "MAXIMIZE_CONFIDENCE":
                u = 0.02 * cost_norm + 0.03 * speed_norm + 0.95 * conf_norm
            else:  # BALANCED_UTILITY
                u = (w_cost * cost_norm) + (w_speed * speed_norm) + (w_conf * conf_norm)


            cand.utility_score = round(u, 4)
            if u > max_utility:
                max_utility = u
                best_cand = cand

        return best_cand
