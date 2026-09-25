"""
Scientific Constraints - Feasibility Engine
Evaluates constraint slack variables and projects candidate plans into feasible subspaces.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class FeasibilityEvaluation:
    is_feasible: bool
    violated_constraints: List[str]
    slack_variables: Dict[str, float]
    binding_constraints: List[str]
    feasibility_score: float  # 1.0 = fully feasible, < 1.0 = degree of violation


class FeasibilityEngine:
    """Evaluates slack and feasibility for candidate execution plans."""

    @classmethod
    def evaluate(
        cls,
        candidate_metrics: Dict[str, float],
        constraints: Dict[str, float],
    ) -> FeasibilityEvaluation:
        """
        constraints schema:
        - max_budget_usd: float
        - max_latency_ms: float
        - min_accuracy: float
        - max_risk: float
        - max_compliance_flags: float
        """
        violations: List[str] = []
        slacks: Dict[str, float] = {}
        bindings: List[str] = []

        # 1. Budget constraint: cost <= max_budget
        if "max_budget_usd" in constraints:
            limit = constraints["max_budget_usd"]
            actual = candidate_metrics.get("cost_usd", 0.0)
            slack = limit - actual
            slacks["budget_slack_usd"] = round(slack, 4)
            if slack < 0:
                violations.append(f"Budget exceeded: ${actual:.4f} > ${limit:.4f}")
            elif abs(slack) < 0.005:
                bindings.append("max_budget_usd")

        # 2. Latency constraint: latency <= max_latency
        if "max_latency_ms" in constraints:
            limit = constraints["max_latency_ms"]
            actual = candidate_metrics.get("latency_ms", 0.0)
            slack = limit - actual
            slacks["latency_slack_ms"] = round(slack, 1)
            if slack < 0:
                violations.append(f"Latency deadline exceeded: {actual:.1f}ms > {limit:.1f}ms")
            elif abs(slack) < 100.0:
                bindings.append("max_latency_ms")

        # 3. Accuracy constraint: accuracy >= min_accuracy
        if "min_accuracy" in constraints:
            limit = constraints["min_accuracy"]
            actual = candidate_metrics.get("accuracy", 1.0)
            slack = actual - limit
            slacks["accuracy_slack"] = round(slack, 4)
            if slack < 0:
                violations.append(f"Accuracy below threshold: {actual:.4f} < {limit:.4f}")
            elif abs(slack) < 0.02:
                bindings.append("min_accuracy")

        # 4. Risk constraint: risk <= max_risk
        if "max_risk" in constraints:
            limit = constraints["max_risk"]
            actual = candidate_metrics.get("overall_risk", 0.0)
            slack = limit - actual
            slacks["risk_slack"] = round(slack, 4)
            if slack < 0:
                violations.append(f"Risk exceeded limit: {actual:.4f} > {limit:.4f}")
            elif abs(slack) < 0.05:
                bindings.append("max_risk")

        is_feasible = len(violations) == 0
        feasibility_score = 1.0 if is_feasible else max(0.0, 1.0 - (len(violations) * 0.25))

        return FeasibilityEvaluation(
            is_feasible=is_feasible,
            violated_constraints=violations,
            slack_variables=slacks,
            binding_constraints=bindings,
            feasibility_score=round(feasibility_score, 4),
        )
