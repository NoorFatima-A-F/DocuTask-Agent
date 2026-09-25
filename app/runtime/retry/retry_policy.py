"""
Quantitative Retry Optimization - Retry Policy
Defines parameterized and versioned retry policies and threshold ceilings.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryPolicy:
    policy_id: str
    max_retries: int
    min_marginal_benefit: float
    max_cumulative_cost_usd: float
    max_cumulative_delay_ms: float
    backoff_multiplier: float
    delay_penalty_factor: float


DEFAULT_RETRY_POLICY = RetryPolicy(
    policy_id="standard_enterprise_v1",
    max_retries=3,
    min_marginal_benefit=0.05,
    max_cumulative_cost_usd=0.05,
    max_cumulative_delay_ms=8000.0,
    backoff_multiplier=1.5,
    delay_penalty_factor=0.0001,
)
