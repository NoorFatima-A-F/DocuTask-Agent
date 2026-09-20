"""
Scientific Constraints - Deterministic Constraint Solver
Solves feasible boundary envelopes across budget, latency, memory, compliance, and worker limits.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from app.runtime.constraints.constraint_graph import ConstraintGraph, ConstraintNode
from app.runtime.constraints.feasibility_engine import FeasibilityEngine, FeasibilityEvaluation


@dataclass
class SolverResult:
    is_satisfiable: bool
    feasible_candidates: List[Dict[str, Any]]
    infeasible_candidates: List[Dict[str, Any]]
    graph: Dict[str, Any]
    active_bindings: List[str]
    conflict_report: List[str]


class ConstraintSolver:
    """Solves constraint satisfaction problems over candidate plan spaces."""

    @classmethod
    def solve(
        cls,
        candidate_plans: List[Dict[str, Any]],
        constraints: Dict[str, float],
    ) -> SolverResult:
        graph = ConstraintGraph()

        # Build graph nodes
        if "max_budget_usd" in constraints:
            graph.add_constraint(
                ConstraintNode("budget", "Max Cost USD", "HARD", "cost <= max_budget_usd", constraints["max_budget_usd"])
            )
        if "max_latency_ms" in constraints:
            graph.add_constraint(
                ConstraintNode("latency", "Max Latency ms", "HARD", "latency <= max_latency_ms", constraints["max_latency_ms"])
            )
        if "min_accuracy" in constraints:
            graph.add_constraint(
                ConstraintNode("accuracy", "Min Accuracy", "HARD", "accuracy >= min_accuracy", constraints["min_accuracy"])
            )
        if "max_risk" in constraints:
            graph.add_constraint(
                ConstraintNode("risk", "Max Failure Risk", "SOFT", "risk <= max_risk", constraints["max_risk"])
            )

        # Detect conflicting constraints
        conflicts = graph.detect_conflicts()

        feasible_list = []
        infeasible_list = []
        all_bindings = set()

        for plan in candidate_plans:
            metrics = {
                "cost_usd": plan.get("cost_usd", 0.01),
                "latency_ms": plan.get("latency_ms", 1000.0),
                "accuracy": plan.get("accuracy", 0.95),
                "overall_risk": plan.get("overall_risk", 0.05),
            }
            eval_res = FeasibilityEngine.evaluate(metrics, constraints)
            plan_record = dict(plan)
            plan_record["feasibility"] = eval_res

            if eval_res.is_feasible:
                feasible_list.append(plan_record)
                all_bindings.update(eval_res.binding_constraints)
            else:
                infeasible_list.append(plan_record)

        return SolverResult(
            is_satisfiable=len(feasible_list) > 0,
            feasible_candidates=feasible_list,
            infeasible_candidates=infeasible_list,
            graph=graph.get_graph_data(),
            active_bindings=list(all_bindings),
            conflict_report=conflicts,
        )
