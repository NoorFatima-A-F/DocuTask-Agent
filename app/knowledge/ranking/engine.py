"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Ranking Engine.
Computes multi-factor relevance scores combining semantic similarity, lexical matching, authority, freshness, and trust.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
import math
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from app.knowledge.core.models import RetrievalResult

logger = logging.getLogger(__name__)


class RankingWeights(BaseModel):
    """Configurable weights for multi-factor ranking formula."""
    semantic_weight: float = 0.40
    keyword_weight: float = 0.25
    authority_weight: float = 0.15
    freshness_weight: float = 0.10
    trust_weight: float = 0.10


class RankingEngine:
    """
    Reranks candidate retrieval results by evaluating content freshness, source authority,
    domain trust, and keyword-semantic relevance.
    """

    def __init__(self, weights: Optional[RankingWeights] = None):
        self.weights = weights or RankingWeights()

    def rank(
        self,
        candidates: List[RetrievalResult],
        user_context: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievalResult]:
        """
        Calculates final composite score for all retrieval candidates and returns them sorted descending.
        """
        now = datetime.now(timezone.utc)
        w = self.weights

        for res in candidates:
            # 1. Freshness Score (exponential decay over days)
            created_at = res.chunk.metadata.get("created_at")
            freshness = 1.0
            if created_at and isinstance(created_at, datetime):
                days_old = max(0.0, (now - created_at).total_seconds() / 86400.0)
                freshness = math.exp(-0.01 * days_old)  # half life ~70 days
            res.freshness_score = freshness

            # 2. Authority Score (based on verified source metadata or hierarchy level)
            authority = 1.0
            if res.chunk.metadata.get("verified_official"):
                authority = 1.5
            elif res.chunk.metadata.get("hierarchy_level") == "PARENT":
                authority = 1.2
            res.authority_score = authority

            # 3. Trust Score
            trust = float(res.chunk.metadata.get("trust_score", 1.0))
            res.trust_score = trust

            # 4. Composite Formula
            composite = (
                w.semantic_weight * res.semantic_score
                + w.keyword_weight * res.keyword_score
                + w.authority_weight * res.authority_score
                + w.freshness_weight * res.freshness_score
                + w.trust_weight * res.trust_score
            )
            res.score = composite

        candidates.sort(key=lambda r: r.score, reverse=True)
        return candidates
