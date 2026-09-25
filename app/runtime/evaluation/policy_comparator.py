"""
Policy Evaluation Engine - Policy Comparator
Compares two planner policies side-by-side across utility, cost, latency, and success distributions.
"""

from typing import Dict, List, Any


class PolicyComparator:
    """Computes differential performance statistics between policy versions A and B."""

    @staticmethod
    def compare_policies(
        policy_a_metrics: List[Dict[str, float]],
        policy_b_metrics: List[Dict[str, float]],
    ) -> Dict[str, Any]:
        if not policy_a_metrics or not policy_b_metrics:
            return {}

        n = min(len(policy_a_metrics), len(policy_b_metrics))
        a_slice = policy_a_metrics[:n]
        b_slice = policy_b_metrics[:n]

        u_a = [m.get("utility", 0.0) for m in a_slice]
        u_b = [m.get("utility", 0.0) for m in b_slice]

        mean_u_a = sum(u_a) / n
        mean_u_b = sum(u_b) / n

        # B win count over A
        b_wins = sum(1 for ua, ub in zip(u_a, u_b) if ub > ua)
        win_rate_b = (b_wins / n) * 100.0

        utility_delta = mean_u_b - mean_u_a
        pct_improvement = (utility_delta / (mean_u_a + 1e-6)) * 100.0

        # Latency & Cost comparisons
        lat_a = sum(m.get("latency_ms", 1000.0) for m in a_slice) / n
        lat_b = sum(m.get("latency_ms", 1000.0) for m in b_slice) / n

        cost_a = sum(m.get("cost_usd", 0.02) for m in a_slice) / n
        cost_b = sum(m.get("cost_usd", 0.02) for m in b_slice) / n

        return {
            "sample_size": n,
            "policy_a_mean_utility": round(mean_u_a, 4),
            "policy_b_mean_utility": round(mean_u_b, 4),
            "utility_gain_percentage": round(pct_improvement, 2),
            "win_rate_policy_b_percent": round(win_rate_b, 2),
            "latency_reduction_ms": round(lat_a - lat_b, 1),
            "cost_savings_usd": round(cost_a - cost_b, 5),
            "is_statistically_superior": win_rate_b > 55.0 and utility_delta > 0.01,
        }
