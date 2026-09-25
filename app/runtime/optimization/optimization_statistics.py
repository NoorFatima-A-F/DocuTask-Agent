"""
Multi-Objective Optimization Engine - Optimization Statistics
Calculates diversity, spacing, dominated candidate ratios, and convergence metrics.
"""

from typing import Dict, List, Any
import math


class OptimizationStatistics:
    """Computes Pareto set diversity and quality indicators."""

    @staticmethod
    def compute_frontier_metrics(
        frontier: List[Dict[str, Any]],
        dominated: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        total = len(frontier) + len(dominated)
        frontier_ratio = (len(frontier) / total) if total > 0 else 0.0

        # Spacing metric across frontier
        spacing = 0.0
        if len(frontier) > 1:
            diffs = []
            for i in range(len(frontier) - 1):
                o1 = frontier[i].get("objectives", frontier[i])
                o2 = frontier[i + 1].get("objectives", frontier[i + 1])
                numeric_keys = [
                    k for k in o1.keys()
                    if k in o2 and isinstance(o1[k], (int, float)) and isinstance(o2[k], (int, float))
                ]
                dist = math.sqrt(sum((float(o1[k]) - float(o2[k])) ** 2 for k in numeric_keys)) if numeric_keys else 0.0
                diffs.append(dist)
            if diffs:
                mean_d = sum(diffs) / len(diffs)
                spacing = math.sqrt(sum((d - mean_d) ** 2 for d in diffs) / len(diffs))

        return {
            "total_candidates": total,
            "pareto_optimal_count": len(frontier),
            "dominated_count": len(dominated),
            "frontier_ratio": round(frontier_ratio, 4),
            "frontier_spacing": round(spacing, 4),
            "is_well_distributed": spacing < 0.25,
        }
