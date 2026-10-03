"""
Review Comment Generator (Phase 82B.10)
=======================================
Generates structured peer review feedback and actionable critique.
Distinguishes Major Findings, Minor Suggestions, and Empirical Strengths.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class CommentCategory(str, Enum):
    STRENGTH = "STRENGTH"
    MAJOR_FINDING = "MAJOR_FINDING"
    MINOR_SUGGESTION = "MINOR_SUGGESTION"
    REPRODUCIBILITY_BLOCKER = "REPRODUCIBILITY_BLOCKER"
    UNCERTAINTY_GAP = "UNCERTAINTY_GAP"


@dataclass(frozen=True)
class ReviewComment:
    comment_id: str
    category: CommentCategory
    dimension: str
    summary: str
    detail: str
    suggested_remediation: Optional[str] = None


class ReviewCommentGenerator:
    """
    Synthesizes actionable peer review feedback.
    """

    @classmethod
    def generate_comments_from_audit(
        cls,
        missing_fields: List[str],
        provenance_valid: bool,
        reproducibility_score: float,
        has_uncertainty_bounds: bool,
    ) -> List[ReviewComment]:
        """Generate structured peer reviewer comments."""
        comments: List[ReviewComment] = []
        idx = 1

        if provenance_valid:
            comments.append(ReviewComment(
                comment_id=f"REV_C_{idx:03d}",
                category=CommentCategory.STRENGTH,
                dimension="Evidence Provenance",
                summary="Unbroken Merkle DAG provenance with complete W3C PROV compliance.",
                detail="The authors provide cryptographic lineage traces from raw observations to final claims.",
            ))
            idx += 1

        if reproducibility_score >= 0.85:
            comments.append(ReviewComment(
                comment_id=f"REV_C_{idx:03d}",
                category=CommentCategory.STRENGTH,
                dimension="Reproducibility",
                summary="High empirical reproducibility across independent replay runs.",
                detail=f"Replication divergence is within acceptable tolerances (score: {reproducibility_score:.2f}).",
            ))
            idx += 1
        elif reproducibility_score < 0.70:
            comments.append(ReviewComment(
                comment_id=f"REV_C_{idx:03d}",
                category=CommentCategory.REPRODUCIBILITY_BLOCKER,
                dimension="Reproducibility",
                summary="Metric divergence across independent runs exceeds empirical tolerance.",
                detail="Authors should isolate random seeds and provide explicit hardware clock compensation.",
                suggested_remediation="Re-run benchmark with locked seeds and publish exact CPU clock frequencies.",
            ))
            idx += 1

        if not has_uncertainty_bounds:
            comments.append(ReviewComment(
                comment_id=f"REV_C_{idx:03d}",
                category=CommentCategory.UNCERTAINTY_GAP,
                dimension="Statistical Rigor",
                summary="Point estimates published without confidence intervals or error bars.",
                detail="Key performance metrics lack Wilson CIs or BCa bootstrap standard errors.",
                suggested_remediation="Compute 95% Wilson score confidence intervals for all binomial metrics.",
            ))
            idx += 1

        for missing in missing_fields:
            comments.append(ReviewComment(
                comment_id=f"REV_C_{idx:03d}",
                category=CommentCategory.MAJOR_FINDING,
                dimension="Artifact Completeness",
                summary=f"Mandatory disclosure missing: '{missing}'.",
                detail=f"The artifact lacks required '{missing}' metadata required by ACM/USENIX guidelines.",
                suggested_remediation=f"Add '{missing}' block to publication manifest.",
            ))
            idx += 1

        return comments
