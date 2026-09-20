"""Grounding Verifier across Knowledge Chunks."""

import re
from typing import List, Optional
from ..gateway.context import KnowledgeChunk
from .confidence import GroundingClaim, GroundingReport, GroundingConfidenceScorer


class GroundingVerifier:
    """Verifies that facts and claims in AI output are grounded in retrieved source chunks."""

    def __init__(self, scorer: GroundingConfidenceScorer = None):
        self.scorer = scorer or GroundingConfidenceScorer()

    def split_into_claims(self, text: str) -> List[str]:
        """Splits output text into atomic factual sentence claims."""
        if not text:
            return []
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    def verify_grounding(
        self,
        output_text: str,
        knowledge_chunks: List[KnowledgeChunk],
    ) -> GroundingReport:
        if not output_text or not knowledge_chunks:
            # If no knowledge chunks were provided, skip grounding check (or return neutral)
            return GroundingReport(
                is_grounded=True,
                grounding_score=1.0,
                total_claims=0,
                grounded_claims=0,
            )

        claims = self.split_into_claims(output_text)
        evaluated_claims: List[GroundingClaim] = []

        combined_chunk_text = " ".join([c.content for c in knowledge_chunks]).lower()

        for claim in claims:
            claim_lower = claim.lower()
            # Extract keywords (words >= 4 chars)
            words = [w for w in re.findall(r"\b\w+\b", claim_lower) if len(w) >= 4]
            if not words:
                evaluated_claims.append(GroundingClaim(claim_text=claim, is_grounded=True))
                continue

            # Check matching keywords in chunks
            matches = [w for w in words if w in combined_chunk_text]
            overlap_ratio = len(matches) / len(words)

            # Find best supporting chunk
            best_chunk_id = None
            for chunk in knowledge_chunks:
                chunk_matches = [w for w in words if w in chunk.content.lower()]
                if len(chunk_matches) / len(words) >= 0.5:
                    best_chunk_id = chunk.chunk_id
                    break

            is_grounded = overlap_ratio >= 0.40
            evaluated_claims.append(
                GroundingClaim(
                    claim_text=claim,
                    is_grounded=is_grounded,
                    supporting_chunk_id=best_chunk_id if is_grounded else None,
                    confidence=round(overlap_ratio, 2),
                    reason=None if is_grounded else "Low keyword overlap with source context",
                )
            )

        return self.scorer.score_claims(evaluated_claims)
