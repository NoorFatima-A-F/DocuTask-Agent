"""Candidate Plan Evaluator and Regret Calculator.

Quantifies candidate planning choices and calculates post-hoc regret metrics
comparing predicted vs realized execution utility.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class CandidatePlan:
    candidate_id: str
    model: str
    dag_depth: int
    parallelism: int
    predicted_cost_usd: float
    predicted_latency_ms: float
    predicted_accuracy: float
    estimated_utility: float
    constraints_satisfied: bool
    selection_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "model": self.model,
            "dag_depth": self.dag_depth,
            "parallelism": self.parallelism,
            "predicted_cost_usd": self.predicted_cost_usd,
            "predicted_latency_ms": self.predicted_latency_ms,
            "predicted_accuracy": self.predicted_accuracy,
            "estimated_utility": self.estimated_utility,
            "constraints_satisfied": self.constraints_satisfied,
            "selection_score": self.selection_score,
        }


class CandidatePlanEvaluator:
    @staticmethod
    def evaluate_candidates(
        candidates_raw: List[Dict[str, Any]],
        max_cost_bound: float = 0.05,
        max_latency_bound: float = 3000.0,
    ) -> List[CandidatePlan]:
        plans: List[CandidatePlan] = []
        for raw in candidates_raw:
            cid = raw.get("candidate_id", "cand-0")
            model = raw.get("model", "gemini-2.5-flash")
            depth = int(raw.get("dag_depth", 3))
            par = int(raw.get("parallelism", 2))
            cost = float(raw.get("predicted_cost_usd", 0.003))
            lat = float(raw.get("predicted_latency_ms", 350.0))
            acc = float(raw.get("predicted_accuracy", 0.96))

            satisfies = (cost <= max_cost_bound) and (lat <= max_latency_bound)
            # Utility function
            utility = (acc * 0.5) - (cost / max_cost_bound * 0.25) - (lat / max_latency_bound * 0.25)
            score = utility if satisfies else -1.0

            plans.append(
                CandidatePlan(
                    candidate_id=cid,
                    model=model,
                    dag_depth=depth,
                    parallelism=par,
                    predicted_cost_usd=cost,
                    predicted_latency_ms=lat,
                    predicted_accuracy=acc,
                    estimated_utility=round(utility, 4),
                    constraints_satisfied=satisfies,
                    selection_score=round(score, 4),
                )
            )

        plans.sort(key=lambda p: p.selection_score, reverse=True)
        return plans


@dataclass
class RegretReport:
    decision_id: str
    selected_candidate_id: str
    optimal_candidate_id: str
    predicted_utility: float
    realized_utility: float
    empirical_regret: float
    counterfactual_gap: float
    is_bounded_optimal: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "selected_candidate_id": self.selected_candidate_id,
            "optimal_candidate_id": self.optimal_candidate_id,
            "predicted_utility": self.predicted_utility,
            "realized_utility": self.realized_utility,
            "empirical_regret": self.empirical_regret,
            "counterfactual_gap": self.counterfactual_gap,
            "is_bounded_optimal": self.is_bounded_optimal,
        }


class RegretCalculator:
    @staticmethod
    def calculate_regret(
        decision_id: str,
        selected_candidate: CandidatePlan,
        realized_metrics: Dict[str, float],
        all_candidates: List[CandidatePlan],
    ) -> RegretReport:
        # Realized utility
        realized_acc = realized_metrics.get("actual_accuracy", 0.98)
        realized_cost = realized_metrics.get("actual_cost_usd", selected_candidate.predicted_cost_usd)
        realized_lat = realized_metrics.get("actual_latency_ms", selected_candidate.predicted_latency_ms)

        realized_utility = round((realized_acc * 0.5) - (realized_cost / 0.05 * 0.25) - (realized_lat / 3000.0 * 0.25), 4)
        best_candidate = max(all_candidates, key=lambda c: c.estimated_utility)

        regret = max(0.0, round(best_candidate.estimated_utility - realized_utility, 4))
        gap = round(abs(selected_candidate.estimated_utility - realized_utility), 4)

        return RegretReport(
            decision_id=decision_id,
            selected_candidate_id=selected_candidate.candidate_id,
            optimal_candidate_id=best_candidate.candidate_id,
            predicted_utility=selected_candidate.estimated_utility,
            realized_utility=realized_utility,
            empirical_regret=regret,
            counterfactual_gap=gap,
            is_bounded_optimal=(regret <= 0.05),
        )
