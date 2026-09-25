"""
Scientific Benchmark Engine - Baseline Policies
Reference baseline implementations for empirical comparison: Greedy, Random, Cost First, Latency First, Accuracy First.
"""

from typing import Dict, List, Any
import random


class BaselinePolicies:
    """Standard comparison baselines."""

    @staticmethod
    def greedy_planner(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Picks the first plan that satisfies minimum threshold on accuracy."""
        for c in candidates:
            if c.get("accuracy", 0.0) >= 0.90:
                return c
        return candidates[0] if candidates else {}

    @staticmethod
    def random_planner(candidates: List[Dict[str, Any]], seed: int = 42) -> Dict[str, Any]:
        """Selects a plan completely at random."""
        if not candidates:
            return {}
        rng = random.Random(seed)
        return rng.choice(candidates)

    @staticmethod
    def cost_first_planner(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Picks cheapest candidate ignoring latency/accuracy balance."""
        if not candidates:
            return {}
        return min(candidates, key=lambda c: c.get("cost_usd", 1.0))

    @staticmethod
    def latency_first_planner(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Picks fastest candidate ignoring cost."""
        if not candidates:
            return {}
        return min(candidates, key=lambda c: c.get("latency_ms", 99999.0))

    @staticmethod
    def accuracy_first_planner(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Picks highest accuracy candidate regardless of cost/latency."""
        if not candidates:
            return {}
        return max(candidates, key=lambda c: c.get("accuracy", 0.0))
