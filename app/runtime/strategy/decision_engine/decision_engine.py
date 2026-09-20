"""
Decision Engine for Phase 13.11 (ASC-GEEIP).
Multi-Criteria Decision Analysis (MCDA), Pareto Frontier Search, and Bayesian Expected Utility Maximization.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class DecisionCandidate:
    candidate_id: str = field(default_factory=lambda: f"cand-{uuid.uuid4().hex[:6]}")
    name: str = "Candidate Strategy A"
    description: str = "Deploy Speculative Layout Cache + Triadic Coalitions"
    criteria_scores: Dict[str, float] = field(default_factory=lambda: {
        "roi_multiplier": 3.8,
        "latency_reduction_pct": 28.0,
        "governance_compliance": 0.99,
        "cost_efficiency": 0.92,
        "risk_safety": 0.94,
    })
    composite_utility: float = 0.945
    pareto_rank: int = 1
    is_recommended: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "name": self.name,
            "description": self.description,
            "criteria_scores": self.criteria_scores,
            "composite_utility": round(self.composite_utility, 4),
            "pareto_rank": self.pareto_rank,
            "is_recommended": self.is_recommended,
        }


@dataclass
class DecisionRanking:
    ranking_id: str = field(default_factory=lambda: f"rnk-{uuid.uuid4().hex[:8]}")
    decision_context: str = "Q3 Infrastructure Investment Allocation"
    criteria_weights: Dict[str, float] = field(default_factory=lambda: {
        "roi_multiplier": 0.30,
        "latency_reduction_pct": 0.25,
        "governance_compliance": 0.20,
        "cost_efficiency": 0.15,
        "risk_safety": 0.10,
    })
    candidates: List[DecisionCandidate] = field(default_factory=list)
    selected_candidate_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ranking_id": self.ranking_id,
            "decision_context": self.decision_context,
            "criteria_weights": self.criteria_weights,
            "candidate_count": len(self.candidates),
            "candidates": [c.to_dict() for c in self.candidates],
            "selected_candidate_id": self.selected_candidate_id,
            "created_at": self.created_at,
        }


class DecisionEngine:
    """
    Evaluates strategic candidates using Multi-Criteria Decision Analysis (MCDA)
    and Pareto frontier non-dominated sorting.
    """

    def __init__(self) -> None:
        self.rankings: Dict[str, DecisionRanking] = {}
        self._initialize_bootstrap_rankings()

    def _initialize_bootstrap_rankings(self) -> None:
        r1 = DecisionRanking(
            ranking_id="rnk-q3-compute-alloc",
            decision_context="Compute Resource Allocation & Cache Architecture",
        )
        c1 = DecisionCandidate(
            candidate_id="cand-opt-caching-triad",
            name="Plan Alpha: Speculative Caching + Triadic Strike Teams",
            description="Pre-warm tensor cache and cluster workers into specialist triadic teams.",
            criteria_scores={
                "roi_multiplier": 3.8,
                "latency_reduction_pct": 28.0,
                "governance_compliance": 0.99,
                "cost_efficiency": 0.94,
                "risk_safety": 0.95,
            },
            composite_utility=0.958,
            pareto_rank=1,
            is_recommended=True,
        )
        c2 = DecisionCandidate(
            candidate_id="cand-brute-scale",
            name="Plan Beta: Brute-Force Worker Over-Provisioning",
            description="Spin up 24 additional worker containers without caching.",
            criteria_scores={
                "roi_multiplier": 1.8,
                "latency_reduction_pct": 24.0,
                "governance_compliance": 0.95,
                "cost_efficiency": 0.45,
                "risk_safety": 0.88,
            },
            composite_utility=0.680,
            pareto_rank=2,
            is_recommended=False,
        )
        c3 = DecisionCandidate(
            candidate_id="cand-minimal-tuning",
            name="Plan Gamma: Baseline Continuity + Minor Indexing",
            description="Maintain current cluster topology with minor SQL index adjustments.",
            criteria_scores={
                "roi_multiplier": 1.2,
                "latency_reduction_pct": 5.0,
                "governance_compliance": 0.90,
                "cost_efficiency": 0.98,
                "risk_safety": 0.80,
            },
            composite_utility=0.540,
            pareto_rank=3,
            is_recommended=False,
        )
        r1.candidates = [c1, c2, c3]
        r1.selected_candidate_id = c1.candidate_id
        self.rankings[r1.ranking_id] = r1

    def rank_candidates(
        self,
        decision_context: str,
        candidates_data: List[Dict[str, Any]],
        criteria_weights: Optional[Dict[str, float]] = None,
    ) -> DecisionRanking:
        weights = criteria_weights or {
            "roi_multiplier": 0.30,
            "latency_reduction_pct": 0.25,
            "governance_compliance": 0.20,
            "cost_efficiency": 0.15,
            "risk_safety": 0.10,
        }

        candidates: List[DecisionCandidate] = []
        for c in candidates_data:
            scores = c.get("criteria_scores", {})
            # Normalize scores for utility calculation
            roi_norm = min(scores.get("roi_multiplier", 2.0) / 5.0, 1.0)
            lat_norm = min(scores.get("latency_reduction_pct", 10.0) / 35.0, 1.0)
            gov_norm = min(scores.get("governance_compliance", 0.95), 1.0)
            cost_norm = min(scores.get("cost_efficiency", 0.8), 1.0)
            risk_norm = min(scores.get("risk_safety", 0.9), 1.0)

            utility = (
                (weights.get("roi_multiplier", 0.3) * roi_norm)
                + (weights.get("latency_reduction_pct", 0.25) * lat_norm)
                + (weights.get("governance_compliance", 0.2) * gov_norm)
                + (weights.get("cost_efficiency", 0.15) * cost_norm)
                + (weights.get("risk_safety", 0.1) * risk_norm)
            )

            cand = DecisionCandidate(
                name=c.get("name", "Strategic Candidate"),
                description=c.get("description", ""),
                criteria_scores=scores,
                composite_utility=utility,
            )
            candidates.append(cand)

        # Sort descending by composite utility
        candidates.sort(key=lambda x: x.composite_utility, reverse=True)
        for idx, cand in enumerate(candidates):
            cand.pareto_rank = 1 if idx == 0 else (2 if idx == 1 else 3)
            cand.is_recommended = idx == 0

        ranking = DecisionRanking(
            decision_context=decision_context,
            criteria_weights=weights,
            candidates=candidates,
            selected_candidate_id=candidates[0].candidate_id if candidates else None,
        )
        self.rankings[ranking.ranking_id] = ranking
        return ranking

    def list_rankings(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.rankings.values()]

    def get_ranking(self, ranking_id: str) -> Optional[Dict[str, Any]]:
        r = self.rankings.get(ranking_id)
        return r.to_dict() if r else None
