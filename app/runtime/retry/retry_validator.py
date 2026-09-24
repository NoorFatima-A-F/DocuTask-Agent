"""
Quantitative Retry Optimization - Retry Validator
Prevents infinite retry loops and ensures non-violation of budget and latency invariants.
"""

from typing import List, Tuple
from app.runtime.retry.retry_policy import RetryPolicy


class RetryValidator:
    """Validates that retry decisions comply with budget ceilings and hard loop boundaries."""

    @staticmethod
    def validate_retry_eligibility(
        current_retries: int,
        cumulative_cost: float,
        cumulative_delay: float,
        policy: RetryPolicy,
    ) -> Tuple[bool, List[str]]:
        errors = []
        if current_retries >= policy.max_retries:
            errors.append(f"Exceeded max allowed retries ({current_retries} >= {policy.max_retries})")

        if cumulative_cost > policy.max_cumulative_cost_usd:
            errors.append(f"Cumulative retry cost ${cumulative_cost:.4f} exceeded policy cap ${policy.max_cumulative_cost_usd:.4f}")

        if cumulative_delay > policy.max_cumulative_delay_ms:
            errors.append(f"Cumulative retry delay {cumulative_delay:.1f}ms exceeded policy cap {policy.max_cumulative_delay_ms:.1f}ms")

        return len(errors) == 0, errors
