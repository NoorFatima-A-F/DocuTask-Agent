"""
Experience Ranker for Phase 13.5 (ARLP-KIP).
Ranks past mission experiences and reflections by empirical utility and confidence.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class RankedExperience(BaseModel):
    experience_id: str
    rank: int
    utility_score: float
    confidence_score: float
    success_rate: float


class ExperienceRanker:
    """
    Ranks experiences using multi-attribute utility theory (success, duration, confidence).
    """

    @classmethod
    def rank_experiences(cls, experiences: List[Dict[str, Any]]) -> List[RankedExperience]:
        scored = []
        for exp in experiences:
            exp_id = exp.get("id") or exp.get("experience_id") or "exp_unknown"
            succ = float(exp.get("success_rate", 0.9))
            conf = float(exp.get("confidence", 0.9))
            utility = round(0.6 * succ + 0.4 * conf, 4)
            scored.append({
                "experience_id": exp_id,
                "utility": utility,
                "confidence": conf,
                "success_rate": succ,
            })

        # Sort descending by utility
        scored.sort(key=lambda x: x["utility"], reverse=True)

        ranked = []
        for i, item in enumerate(scored):
            ranked.append(
                RankedExperience(
                    experience_id=item["experience_id"],
                    rank=i + 1,
                    utility_score=item["utility"],
                    confidence_score=item["confidence"],
                    success_rate=item["success_rate"],
                )
            )
        return ranked
