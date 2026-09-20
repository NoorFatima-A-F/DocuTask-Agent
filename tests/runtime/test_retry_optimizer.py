"""
Unit & Marginal Benefit Tests for Retry Optimizer (QDIOP / SDIOP).
"""

import pytest
from app.runtime.retry import (
    RetryOptimizer,
    RetryPolicy,
    DEFAULT_RETRY_POLICY,
    retry_statistics,
)


def test_retry_optimizer_recommends_retry_on_first_transient_failure():
    eval_res = RetryOptimizer.evaluate(
        current_retry_count=0,
        failure_type="timeout",
        base_cost_usd=0.003,
        base_latency_ms=600.0,
    )
    assert eval_res.decision == "RETRY"
    assert eval_res.marginal_benefit > 0.0
    assert eval_res.probability_of_recovery >= 0.50


def test_retry_optimizer_escalates_when_max_retries_exceeded():
    eval_res = RetryOptimizer.evaluate(
        current_retry_count=DEFAULT_RETRY_POLICY.max_retries,
        failure_type="timeout",
    )
    assert eval_res.decision == "ESCALATE"
    assert "Exceeded max allowed retries" in eval_res.reason
