"""
Research Decision Rules (Phase 91C)
===================================
Formal actions and threshold policies for autonomous research governance.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class ResearchAction(str, Enum):
    RUN_EXPERIMENT = "RUN_EXPERIMENT"
    REJECT_EXPERIMENT = "REJECT_EXPERIMENT"
    NEED_MORE_EVIDENCE = "NEED_MORE_EVIDENCE"
    NEED_MORE_DATASETS = "NEED_MORE_DATASETS"
    NEED_MORE_REPETITIONS = "NEED_MORE_REPETITIONS"
    NEED_INDEPENDENT_VERIFICATION = "NEED_INDEPENDENT_VERIFICATION"
    NEED_STATISTICAL_POWER = "NEED_STATISTICAL_POWER"
    NEED_REVIEWER_ATTENTION = "NEED_REVIEWER_ATTENTION"


@dataclass(frozen=True)
class ResearchDecision:
    """Outcome of an automated research deliberation."""
    action: ResearchAction
    target_id: str
    confidence_score: float
    rationale: str
    blocking_factors: List[str] = field(default_factory=list)
    suggested_adjustments: Dict[str, Any] = field(default_factory=dict)
    decision_digest_sha256: str = field(default="")
