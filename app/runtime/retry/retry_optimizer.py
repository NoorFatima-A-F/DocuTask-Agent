"""
Quantitative Retry Optimization - Retry Optimizer
Calculates Expected Improvement, Probability of Recovery, Marginal Benefit, and decides quantitative action.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

from app.runtime.retry.retry_policy import RetryPolicy, DEFAULT_RETRY_POLICY
from app.runtime.retry.retry_validator import RetryValidator
from app.runtime.retry.retry_statistics import retry_statistics


@dataclass
class RetryEvaluation:
    decision: str  # RETRY | FALLBACK | ESCALATE
    expected_improvement: float
    probability_of_recovery: float
    retry_cost_usd: float
    expected_delay_ms: float
    marginal_benefit: float
    current_retry_count: int
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RetryOptimizer:
    """Calculates whether executing a retry yields positive net marginal utility."""

    @classmethod
    def evaluate(
        cls,
        current_retry_count: int,
        failure_type: str,
        base_cost_usd: float = 0.005,
        base_latency_ms: float = 800.0,
        policy: Optional[RetryPolicy] = None,
        cumulative_cost_usd: float = 0.0,
        cumulative_delay_ms: float = 0.0,
    ) -> RetryEvaluation:
        pol = policy or DEFAULT_RETRY_POLICY

        # 1. Invariant check
        is_eligible, eligibility_errors = RetryValidator.validate_retry_eligibility(
            current_retries=current_retry_count,
            cumulative_cost=cumulative_cost_usd,
            cumulative_delay=cumulative_delay_ms,
            policy=pol,
        )

        if not is_eligible:
            decision = "ESCALATE"
            reason = f"Ineligible for retry: {'; '.join(eligibility_errors)}"
            eval_res = RetryEvaluation(
                decision=decision,
                expected_improvement=0.0,
                probability_of_recovery=0.0,
                retry_cost_usd=0.0,
                expected_delay_ms=0.0,
                marginal_benefit=-1.0,
                current_retry_count=current_retry_count,
                reason=reason,
            )
            retry_statistics.record(decision)
            return eval_res

        # 2. Probability of recovery decays with prior retries
        # P_rec = P_0 * (decay ^ retries)
        decay = 0.65
        p0 = 0.85 if failure_type.lower() in ("timeout", "rate_limit", "transient_network") else 0.50
        p_recovery = p0 * (decay ** current_retry_count)

        # 3. Expected improvement in utility: delta_U ~ 0.8 (rescuing failed task)
        expected_delta_u = 0.85

        # 4. Retry cost & delay scaling with exponential backoff
        backoff = pol.backoff_multiplier ** current_retry_count
        retry_cost = base_cost_usd * 1.0
        expected_delay = base_latency_ms * backoff

        # 5. Marginal Utility Benefit:
        # Marginal Benefit = P_rec * delta_U - (cost_penalty) - (delay_penalty)
        delay_cost = pol.delay_penalty_factor * expected_delay
        marginal_benefit = (p_recovery * expected_delta_u) - (retry_cost * 10.0) - delay_cost

        # 6. Action selection
        if marginal_benefit >= pol.min_marginal_benefit and p_recovery >= 0.20:
            decision = "RETRY"
            reason = (
                f"Positive marginal benefit ({marginal_benefit:.3f} >= {pol.min_marginal_benefit:.3f}) "
                f"with {p_recovery*100:.1f}% recovery probability."
            )
        elif failure_type.lower() in ("schema_violation", "low_confidence", "ocr_degradation"):
            decision = "FALLBACK"
            reason = f"Marginal benefit too low for raw retry; fallback to multi-modal reasoning recommended."
        else:
            decision = "ESCALATE"
            reason = f"Recovery probability {p_recovery*100:.1f}% below minimum viable threshold."

        retry_statistics.record(decision)

        return RetryEvaluation(
            decision=decision,
            expected_improvement=round(expected_delta_u, 4),
            probability_of_recovery=round(p_recovery, 4),
            retry_cost_usd=round(retry_cost, 5),
            expected_delay_ms=round(expected_delay, 1),
            marginal_benefit=round(marginal_benefit, 4),
            current_retry_count=current_retry_count,
            reason=reason,
        )
