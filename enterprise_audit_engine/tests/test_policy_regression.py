"""Tests for Policy Regression and Threshold Downgrade Detection."""

import pytest
from enterprise_audit_engine.policy_validation.policy_regression import (
    PolicyRegressionDetector,
    PolicyRegressionReport,
)


@pytest.fixture
def base_policy():
    return {
        "minimum_confidence": "HIGH",
        "minimum_eqi": 85.0,
        "forbidden_critical_findings": True,
        "required_domains": ["testing", "security", "runtime"],
        "max_unsupported_claims": 0,
    }


def test_no_regression_identical_policies(base_policy):
    report = PolicyRegressionDetector.check_policy_regression(base_policy, base_policy)
    assert isinstance(report, PolicyRegressionReport)
    assert report.has_regression is False
    assert report.regressions_count == 0
    assert report.status == "NO_REGRESSION"


def test_no_regression_stricter_policy(base_policy):
    stricter = {
        "minimum_confidence": "VERY_HIGH",
        "minimum_eqi": 90.0,
        "forbidden_critical_findings": True,
        "required_domains": ["testing", "security", "runtime", "provenance"],
        "max_unsupported_claims": 0,
    }
    report = PolicyRegressionDetector.check_policy_regression(base_policy, stricter)
    assert report.has_regression is False
    assert report.status == "NO_REGRESSION"


def test_detects_confidence_downgrade(base_policy):
    weaker = dict(base_policy)
    weaker["minimum_confidence"] = "MEDIUM"
    report = PolicyRegressionDetector.check_policy_regression(base_policy, weaker)
    assert report.has_regression is True
    assert report.status == "CRITICAL_POLICY_DOWNGRADE"
    assert any("confidence" in r for r in report.regressions)


def test_detects_eqi_threshold_lowering(base_policy):
    weaker = dict(base_policy)
    weaker["minimum_eqi"] = 70.0
    report = PolicyRegressionDetector.check_policy_regression(base_policy, weaker)
    assert report.has_regression is True
    assert any("EQI" in r for r in report.regressions)


def test_detects_critical_findings_bypass(base_policy):
    weaker = dict(base_policy)
    weaker["forbidden_critical_findings"] = False
    report = PolicyRegressionDetector.check_policy_regression(base_policy, weaker)
    assert report.has_regression is True
    assert any("critical findings" in r for r in report.regressions)


def test_detects_domain_removal(base_policy):
    weaker = dict(base_policy)
    weaker["required_domains"] = ["testing"]  # security and runtime omitted
    report = PolicyRegressionDetector.check_policy_regression(base_policy, weaker)
    assert report.has_regression is True
    assert any("domains removed" in r for r in report.regressions)


def test_detects_unsupported_claims_relaxation(base_policy):
    weaker = dict(base_policy)
    weaker["max_unsupported_claims"] = 5
    report = PolicyRegressionDetector.check_policy_regression(base_policy, weaker)
    assert report.has_regression is True
    assert any("unsupported claims" in r for r in report.regressions)


def test_detects_compound_regressions(base_policy):
    weaker = {
        "minimum_confidence": "LOW",
        "minimum_eqi": 50.0,
        "forbidden_critical_findings": False,
        "required_domains": [],
        "max_unsupported_claims": 10,
    }
    report = PolicyRegressionDetector.check_policy_regression(base_policy, weaker)
    assert report.has_regression is True
    assert report.regressions_count >= 4
