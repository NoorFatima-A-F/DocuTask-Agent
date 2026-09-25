"""
AMAEOP Pillar 3 - Nash Bargaining Utility Negotiator
Finds mathematically optimal Pareto agreements balancing competing utility functions across departments.
"""

from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class BargainingSolution:
    dept_a: str
    dept_b: str
    optimal_allocation_a: float
    optimal_allocation_b: float
    dept_a_utility: float
    dept_b_utility: float
    nash_product: float
    is_pareto_optimal: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class UtilityNegotiator:
    """Calculates Nash Bargaining Solutions: max (U_A(x) - d_A) * (U_B(x) - d_B) over resource splits."""

    @classmethod
    def solve_nash_bargaining(
        cls,
        dept_a: str,
        dept_b: str,
        total_resource: float = 100.0,
        disagreement_a: float = 10.0,
        disagreement_b: float = 10.0,
        weight_a: float = 0.6,
        weight_b: float = 0.4,
    ) -> BargainingSolution:
        # Generalized Nash Bargaining: argmax (u_a - d_a)^w_a * (u_b - d_b)^w_b
        # Analytical solution with linear utilities:
        # alloc_a = d_a + (w_a / (w_a + w_b)) * (total_resource - d_a - d_b)
        surplus = max(0.0, total_resource - disagreement_a - disagreement_b)
        sum_w = weight_a + weight_b
        share_a = disagreement_a + (weight_a / sum_w) * surplus
        share_b = disagreement_b + (weight_b / sum_w) * surplus

        u_a = round(share_a, 2)
        u_b = round(share_b, 2)
        nash_prod = round((u_a - disagreement_a) ** weight_a * (u_b - disagreement_b) ** weight_b, 4)

        return BargainingSolution(
            dept_a=dept_a,
            dept_b=dept_b,
            optimal_allocation_a=u_a,
            optimal_allocation_b=u_b,
            dept_a_utility=u_a,
            dept_b_utility=u_b,
            nash_product=nash_prod,
            is_pareto_optimal=True,
        )
