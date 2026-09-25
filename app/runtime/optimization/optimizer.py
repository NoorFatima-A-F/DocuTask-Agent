"""
Multi-Objective Optimization Engine - Unified Optimizer
Solves multi-objective plan optimization, calculates Pareto frontiers, and selects optimal plan.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import uuid

from app.runtime.optimization.pareto_optimizer import ParetoOptimizer
from app.runtime.optimization.objective_functions import ObjectiveFunctions
from app.runtime.optimization.optimization_statistics import OptimizationStatistics
from app.runtime.optimization.optimization_history import OptimizationRunRecord, optimization_history
from app.runtime.constraints.constraint_solver import ConstraintSolver


class MultiObjectivePlanOptimizer:
    """Core multi-objective optimizer selecting mathematically defensible execution plans."""

    DEFAULT_WEIGHTS = {
        "accuracy": 0.35,
        "latency_ms": 0.20,
        "cost_usd": 0.15,
        "safety_compliance": 0.15,
        "reliability": 0.15,
    }

    IS_COST_MAP = {
        "cost_usd": True,
        "latency_ms": True,
        "risk": True,
        "accuracy": False,
        "safety_compliance": False,
        "reliability": False,
    }

    @classmethod
    def optimize(
        cls,
        candidate_plans: List[Dict[str, Any]],
        constraints: Optional[Dict[str, float]] = None,
        weights: Optional[Dict[str, float]] = None,
        context_id: str = "default_context",
    ) -> Dict[str, Any]:
        applied_weights = dict(weights or cls.DEFAULT_WEIGHTS)
        active_constraints = dict(constraints or {})

        # 1. Feasibility filtering via ConstraintSolver
        solver_res = ConstraintSolver.solve(candidate_plans, active_constraints)
        valid_candidates = solver_res.feasible_candidates if solver_res.feasible_candidates else candidate_plans

        # 2. Pareto Frontier Extraction
        frontier, dominated = ParetoOptimizer.extract_pareto_frontier(valid_candidates, cls.IS_COST_MAP)

        # 3. Score candidates using Chebyshev & Weighted Sum
        scored_candidates = []
        best_candidate = None
        highest_utility = -1.0

        for cand in valid_candidates:
            objs = cand.get("objectives", {
                "accuracy": cand.get("accuracy", 0.95),
                "latency_ms": cand.get("latency_ms", 1200.0) / 5000.0,  # normalized
                "cost_usd": cand.get("cost_usd", 0.02) / 0.10,         # normalized
                "safety_compliance": cand.get("safety_compliance", 1.0),
                "reliability": cand.get("reliability", 0.98),
            })
            # Scalarize utility
            score = ObjectiveFunctions.weighted_sum_scalarization(objs, applied_weights, cls.IS_COST_MAP)
            chebyshev_score = ObjectiveFunctions.chebyshev_scalarization(objs, applied_weights, cls.IS_COST_MAP)
            dist_utopian = ObjectiveFunctions.distance_to_utopian_point(objs, cls.IS_COST_MAP)

            scored = dict(cand)
            scored["scalar_utility"] = score
            scored["chebyshev_utility"] = chebyshev_score
            scored["distance_to_utopian"] = dist_utopian
            scored["is_pareto_optimal"] = any(
                (c.get("id") or c.get("plan_id")) == (cand.get("id") or cand.get("plan_id"))
                for c in frontier
            )
            scored_candidates.append(scored)

            if score > highest_utility:
                highest_utility = score
                best_candidate = scored

        # 4. Compute frontier statistics
        stats = OptimizationStatistics.compute_frontier_metrics(frontier, dominated)

        # 5. Record run to history
        run_id = f"opt_run_{uuid.uuid4().hex[:8]}"
        record = OptimizationRunRecord(
            run_id=run_id,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            context_id=context_id,
            weights=applied_weights,
            selected_plan_id=best_candidate.get("id", best_candidate.get("plan_id", "plan_0")) if best_candidate else "none",
            selected_plan_utility=highest_utility,
            candidate_count=len(candidate_plans),
            pareto_frontier_count=len(frontier),
            raw_candidates=candidate_plans,
            pareto_frontier=frontier,
        )
        optimization_history.record_run(record)

        return {
            "run_id": run_id,
            "selected_plan": best_candidate,
            "selected_utility": highest_utility,
            "pareto_frontier": frontier,
            "dominated_candidates": dominated,
            "all_scored_candidates": scored_candidates,
            "statistics": stats,
            "constraint_satisfiability": solver_res.is_satisfiable,
            "active_bindings": solver_res.active_bindings,
        }
