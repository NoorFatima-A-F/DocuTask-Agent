"""
Multi-Objective Optimization Engine - Optimizer Validator
Verifies Pareto frontier determinism, non-dominance criteria, and constraint satisfaction.
"""

from typing import Dict, List, Any, Tuple
from app.runtime.optimization.pareto_optimizer import ParetoOptimizer


class OptimizerValidator:
    """Validates mathematical properties of the optimizer."""

    @staticmethod
    def assert_pareto_stability(
        candidates: List[Dict[str, Any]],
        trials: int = 5,
    ) -> bool:
        """Verifies that arbitrary permutations of the candidate list produce the exact same Pareto frontier."""
        import random
        base_frontier, _ = ParetoOptimizer.extract_pareto_frontier(candidates)
        base_ids = {c.get("id", c.get("plan_id")) for c in base_frontier}

        cand_copy = list(candidates)
        for _ in range(trials):
            random.shuffle(cand_copy)
            perm_frontier, _ = ParetoOptimizer.extract_pareto_frontier(cand_copy)
            perm_ids = {c.get("id", c.get("plan_id")) for c in perm_frontier}
            if perm_ids != base_ids:
                return False

        return True

    @staticmethod
    def assert_non_dominance(frontier: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """Ensures that no point in the reported Pareto frontier dominates another point in the frontier."""
        errors = []
        for i, a in enumerate(frontier):
            for j, b in enumerate(frontier):
                if i != j and ParetoOptimizer.dominates(a.get("objectives", a), b.get("objectives", b)):
                    errors.append(f"Frontier point {i} dominates frontier point {j}, violating Pareto non-dominance.")
        return len(errors) == 0, errors
