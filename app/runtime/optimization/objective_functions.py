"""
Multi-Objective Optimization Engine - Objective Functions
Implements formal scalarization and distance-to-utopian-point objective formulations.
"""

from typing import Dict, List, Any
import math


class ObjectiveFunctions:
    """Formal mathematical scalarization formulations for multi-objective optimization."""

    @staticmethod
    def weighted_sum_scalarization(
        objectives: Dict[str, float],
        weights: Dict[str, float],
        is_cost_map: Dict[str, bool],
    ) -> float:
        """Scalarized linear score: sum(w_i * (1 - x_i if cost else x_i))."""
        total_score = 0.0
        weight_sum = sum(weights.values()) or 1.0

        for key, val in objectives.items():
            w = weights.get(key, 0.0) / weight_sum
            is_cost = is_cost_map.get(key, False)
            norm_val = 1.0 - val if is_cost else val
            total_score += w * max(0.0, min(1.0, norm_val))

        return round(total_score, 4)

    @staticmethod
    def chebyshev_scalarization(
        objectives: Dict[str, float],
        weights: Dict[str, float],
        is_cost_map: Dict[str, bool],
        utopian_point: Dict[str, float] = None,
        rho: float = 0.01,
    ) -> float:
        """Augmented Chebyshev scalarization (finds solutions on non-convex Pareto boundaries).
        max_i [ w_i * |z*_i - f_i| ] + rho * sum(w_i * |z*_i - f_i|)
        """
        diffs = []
        for key, val in objectives.items():
            w = weights.get(key, 0.2)
            is_cost = is_cost_map.get(key, False)
            target = utopian_point.get(key, 0.0 if is_cost else 1.0) if utopian_point else (0.0 if is_cost else 1.0)
            diff = abs(target - val)
            diffs.append(w * diff)

        max_diff = max(diffs) if diffs else 0.0
        aug_sum = sum(diffs)
        # Utility payoff = 1 - Chebyshev distance
        payoff = max(0.0, 1.0 - (max_diff + rho * aug_sum))
        return round(payoff, 4)

    @staticmethod
    def distance_to_utopian_point(
        objectives: Dict[str, float],
        is_cost_map: Dict[str, bool],
    ) -> float:
        """Euclidean distance to ideal utopian point (1.0 for benefits, 0.0 for costs)."""
        sq_dist = 0.0
        for key, val in objectives.items():
            is_cost = is_cost_map.get(key, False)
            ideal = 0.0 if is_cost else 1.0
            sq_dist += (val - ideal) ** 2
        return round(math.sqrt(sq_dist), 4)
