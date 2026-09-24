"""
Multi-Objective Optimization Engine - Pareto Frontier Optimizer
Implements non-dominated sorting, Pareto dominance filtering, and hypervolume computation.
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class ParetoPlan:
    plan_id: str
    plan_name: str
    objectives: Dict[str, float]
    is_pareto_optimal: bool
    domination_rank: int
    crowding_distance: float
    scalar_utility: float
    details: Dict[str, Any]


class ParetoOptimizer:
    """Extracts non-dominated Pareto frontiers across multi-dimensional objective spaces."""

    DEFAULT_IS_COST: Dict[str, bool] = {
        "cost_usd": True,
        "latency_ms": True,
        "risk": True,
        "energy_kwh": True,
        "gpu_load": True,
        "memory_mb": True,
        "accuracy": False,
        "safety_compliance": False,
        "reliability": False,
        "throughput": False,
    }

    @classmethod
    def dominates(
        cls,
        cand_a: Dict[str, float],
        cand_b: Dict[str, float],
        is_cost_map: Dict[str, bool] = None,
    ) -> bool:
        """Returns True if Candidate A strictly Pareto-dominates Candidate B:
        - A is no worse than B in all objectives
        - A is strictly better than B in at least one objective
        """
        cost_map = is_cost_map or cls.DEFAULT_IS_COST
        common_keys = [k for k in cand_a.keys() if k in cand_b and k in cost_map]

        if not common_keys:
            return False

        better_in_at_least_one = False
        for k in common_keys:
            val_a = cand_a[k]
            val_b = cand_b[k]
            is_cost = cost_map[k]

            if is_cost:
                if val_a > val_b:  # A is worse than B in cost
                    return False
                if val_a < val_b:
                    better_in_at_least_one = True
            else:
                if val_a < val_b:  # A is worse than B in benefit
                    return False
                if val_a > val_b:
                    better_in_at_least_one = True

        return better_in_at_least_one

    @classmethod
    def extract_pareto_frontier(
        cls,
        candidates: List[Dict[str, Any]],
        is_cost_map: Dict[str, bool] = None,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Splits candidates into non-dominated Pareto frontier and dominated set."""
        frontier: List[Dict[str, Any]] = []
        dominated: List[Dict[str, Any]] = []

        for i, cand in enumerate(candidates):
            obj_a = cand.get("objectives", cand)
            is_dominated = False

            for j, other in enumerate(candidates):
                if i == j:
                    continue
                obj_b = other.get("objectives", other)
                if cls.dominates(obj_b, obj_a, is_cost_map):
                    is_dominated = True
                    break

            if is_dominated:
                dominated.append(cand)
            else:
                frontier.append(cand)

        return frontier, dominated

    @classmethod
    def calculate_hypervolume_2d(
        cls,
        frontier: List[Dict[str, Any]],
        obj_x: str = "cost_usd",
        obj_y: str = "accuracy",
        ref_x: float = 1.0,
        ref_y: float = 0.0,
    ) -> float:
        """Calculates 2D hypervolume indicator bounded by reference point."""
        if not frontier:
            return 0.0

        # Sort frontier points by obj_x ascending
        pts = []
        for p in frontier:
            objs = p.get("objectives", p)
            if obj_x in objs and obj_y in objs:
                pts.append((objs[obj_x], objs[obj_y]))

        if not pts:
            return 0.0

        pts.sort(key=lambda item: item[0])

        hv = 0.0
        cur_y = ref_y
        for x, y in pts:
            width = max(0.0, ref_x - x)
            height = max(0.0, y - cur_y)
            hv += width * height
            cur_y = max(cur_y, y)

        return round(hv, 4)
