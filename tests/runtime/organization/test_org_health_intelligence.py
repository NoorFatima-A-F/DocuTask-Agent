"""
Test Suite: Organization Health Intelligence & Diagnostics
Validates granular department health breakdowns, queue penalties, burnout risk, and enterprise health indexing.
"""
import pytest
from app.runtime.organization.department import CANONICAL_DEPARTMENTS
from app.runtime.org_health.department_health import DepartmentHealthScorer
from app.runtime.org_health.org_health_aggregator import OrgHealthAggregator


def test_department_health_scorer_nominal():
    dept_gov = CANONICAL_DEPARTMENTS["dept_governance"]
    breakdown = DepartmentHealthScorer.evaluate_department(dept_gov)
    
    assert breakdown.composite_health_score == 100.0
    assert breakdown.utilization_penalty == 0.0
    assert breakdown.burnout_risk_status == "NOMINAL"
    assert breakdown.is_throttling_recommended is False


def test_department_health_scorer_with_penalties():
    dept_ocr = CANONICAL_DEPARTMENTS["dept_ocr"]
    breakdown = DepartmentHealthScorer.evaluate_department(dept_ocr)
    
    assert breakdown.composite_health_score > 90.0
    assert breakdown.queue_congestion_penalty >= 0.0
    assert breakdown.error_rate_penalty >= 0.0


def test_org_health_aggregator_report():
    report = OrgHealthAggregator.get_organization_health_report()
    
    assert report["organization_health_score"] >= 95.0
    assert report["organization_health_tier"] == "OPTIMAL_RESILIENT"
    assert "primary_bottleneck_department" in report
    assert len(report["department_breakdowns"]) == 8
    assert "formula_documentation" in report
