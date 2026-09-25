"""
Ranking Engine.
Ranks executions, strategies, tools, or planner alternatives by evaluated performance.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class RankedItem(BaseModel):
    """An individual item evaluated and assigned a relative rank."""
    item_id: str
    rank: int
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class AlternativeRanker:
    """Ranks alternatives in descending order of evaluated composite score."""

    def rank_items(self, items: List[Dict[str, Any]], score_key: str = "score") -> List[RankedItem]:
        """Ranks a list of candidate dictionaries by a target score key."""
        sorted_items = sorted(items, key=lambda x: float(x.get(score_key, 0.0)), reverse=True)
        ranked: List[RankedItem] = []

        for idx, item in enumerate(sorted_items, start=1):
            ranked.append(RankedItem(
                item_id=str(item.get("id", f"item_{idx}")),
                rank=idx,
                score=float(item.get(score_key, 0.0)),
                metadata=item
            ))

        return ranked
