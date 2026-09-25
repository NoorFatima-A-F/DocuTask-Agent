"""Grounding Confidence Scorer & Metric Models."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class GroundingClaim(BaseModel):
    claim_text: str
    is_grounded: bool = True
    supporting_chunk_id: Optional[str] = None
    confidence: float = 1.0
    reason: Optional[str] = None


class GroundingReport(BaseModel):
    is_grounded: bool
    grounding_score: float  # 0.0 (completely hallucinated) to 1.0 (fully grounded)
    total_claims: int
    grounded_claims: int
    ungrounded_claims: List[GroundingClaim] = Field(default_factory=list)
    citations_mapped: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GroundingConfidenceScorer:
    """Computes grounding metrics and hallucination confidence scores."""

    def score_claims(self, claims: List[GroundingClaim]) -> GroundingReport:
        if not claims:
            return GroundingReport(
                is_grounded=True,
                grounding_score=1.0,
                total_claims=0,
                grounded_claims=0,
            )

        total = len(claims)
        grounded = [c for c in claims if c.is_grounded]
        ungrounded = [c for c in claims if not c.is_grounded]
        grounded_count = len(grounded)

        score = grounded_count / total
        is_grounded = score >= 0.70  # Standard enterprise grounding threshold

        citations = [c.supporting_chunk_id for c in grounded if c.supporting_chunk_id]

        return GroundingReport(
            is_grounded=is_grounded,
            grounding_score=round(score, 3),
            total_claims=total,
            grounded_claims=grounded_count,
            ungrounded_claims=ungrounded,
            citations_mapped=list(set(citations)),
        )
