"""
Test Suite: Enterprise SLA Intelligence & SRE Error Budget Governor
Validates SLA compliance reports, MTTR, MTBF, 99.9% availability, and error budget burn rate throttling.
"""
import pytest
from app.runtime.sla.sla_tracker import SLATracker
from app.runtime.sla.error_budget_governor import ErrorBudgetGovernor


def test_sla_tracker_metrics():
    reports = SLATracker.get_canonical_sla_reports()
    assert len(reports) == 8

    # All departments compliant
    for r in reports:
        assert r.availability_pct >= 99.8
        assert r.observed_p95_latency_ms <= r.target_sla_latency_ms
        assert r.is_in_sla_breach is False

    summary = SLATracker.get_enterprise_sla_summary()
    assert summary["enterprise_availability_pct"] >= 99.9
    assert summary["macro_mttr_seconds"] > 0.0
    assert summary["macro_mtbf_hours"] > 100.0


def test_error_budget_governor():
    statuses = ErrorBudgetGovernor.evaluate_error_budgets()
    assert len(statuses) >= 5

    # Check that error budget remaining is positive
    for s in statuses:
        assert s.budget_remaining_pct > 70.0
        assert s.burn_rate_multiplier >= 0.0

    summary = ErrorBudgetGovernor.get_summary()
    assert summary["overall_error_budget_healthy"] is True
