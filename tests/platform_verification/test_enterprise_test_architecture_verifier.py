"""
Comprehensive Test Suite for Part 2G: Enterprise Test Architecture Verification Framework.
"""
import pytest
from app.platform_verification.test_architecture_verification.runtime.test_verification_runtime import TestVerificationRuntime
from app.platform_verification.test_architecture_verification.domain.models import (
    TestCertificationTier,
    FlakinessClass,
)


@pytest.fixture
def test_runtime():
    return TestVerificationRuntime()


def test_test_pyramid_distribution_and_layer_validation(test_runtime):
    """Verifies standard test pyramid distribution and catches inverted pyramids."""
    healthy_manifest = {
        "unit": [f"u_{i}" for i in range(70)],
        "integration": [f"i_{i}" for i in range(15)],
        "e2e": ["e_1"],
        "security": ["s_1"],
        "ai_evaluation": ["ai_1"],
        "regression": ["r_1"],
    }
    healthy_rep = test_runtime.pyramid_analyzer.analyze_pyramid(healthy_manifest)
    assert healthy_rep.status == "PASS"
    assert healthy_rep.distribution.unit_ratio >= 0.70

    inverted_manifest = {
        "unit": ["u_1"],
        "e2e": [f"e_{i}" for i in range(50)],
    }
    inverted_rep = test_runtime.pyramid_analyzer.analyze_pyramid(inverted_manifest)
    assert inverted_rep.status == "FAIL"
    assert "Inverted test pyramid detected: E2E tests exceed Unit tests" in inverted_rep.issues


def test_unit_quality_and_mock_isolation(test_runtime):
    """Verifies that unit tests mock external dependencies and flags unmocked calls."""
    clean_files = ["test_clean_unit.py"]
    clean_rep = test_runtime.unit_evaluator.evaluate_unit_quality(clean_files)
    assert clean_rep.status == "PASS"
    assert clean_rep.isolation_score == 100.0

    dirty_files = ["tests/unit/test_leak.py with genai.Client()", "tests/unit/test_db.py with create_engine()"]
    dirty_rep = test_runtime.unit_evaluator.evaluate_unit_quality(dirty_files)
    assert dirty_rep.status == "FAIL"
    assert len(dirty_rep.unmocked_external_calls) == 2


def test_coverage_and_mutation_testing_evaluation(test_runtime):
    """Evaluates line, branch, and mutation testing coverage scores."""
    good_cov = {
        "line_coverage_pct": 91.0,
        "branch_coverage_pct": 82.5,
        "total_mutants": 100,
        "mutants_killed": 88,
    }
    rep = test_runtime.coverage_engine.evaluate_coverage_and_mutations(good_cov)
    assert rep.meets_enterprise_thresholds
    assert rep.mutation_score_pct == 88.0

    poor_cov = {
        "line_coverage_pct": 65.0,
        "branch_coverage_pct": 50.0,
        "total_mutants": 100,
        "mutants_killed": 40,
    }
    fail_rep = test_runtime.coverage_engine.evaluate_coverage_and_mutations(poor_cov)
    assert not fail_rep.meets_enterprise_thresholds


def test_ai_evaluation_suite_verification(test_runtime):
    """Verifies prompt regression testing, ground truth F1, and hallucination bounds."""
    good_ai = {
        "prompt_regression_passed": True,
        "ground_truth_f1_score": 0.96,
        "hallucination_rate_pct": 0.8,
        "stochastic_consistency_pct": 99.1,
    }
    ai_rep = test_runtime.ai_verifier.verify_ai_evaluation_suite(good_ai)
    assert ai_rep.status == "PASS"

    bad_ai = {
        "prompt_regression_passed": False,
        "ground_truth_f1_score": 0.82,
        "hallucination_rate_pct": 6.5,
        "stochastic_consistency_pct": 88.0,
    }
    bad_rep = test_runtime.ai_verifier.verify_ai_evaluation_suite(bad_ai)
    assert bad_rep.status == "FAIL"
    assert len(bad_rep.issues) >= 3


def test_reliability_and_flakiness_analyzer(test_runtime):
    """Tests detection of flaky/unstable tests and order dependence."""
    history = [
        {"test_name": "test_auth", "runs": 100, "failures": 0},
        {"test_name": "test_flaky_pdf", "runs": 100, "failures": 3},
        {"test_name": "test_broken_worker", "runs": 100, "failures": 12, "order_dependent": True},
    ]
    rel_rep = test_runtime.reliability_analyzer.analyze_reliability_and_flakiness(history)
    assert rel_rep.status == "FAIL"
    assert rel_rep.reliable_tests == 1
    assert rel_rep.flaky_tests == 1
    assert rel_rep.unstable_tests == 1
    assert not rel_rep.order_independence_verified


def test_environment_reproducibility_validator(test_runtime):
    """Tests verification of pinned dependencies and container environment configs."""
    good_env = {
        "pinned_dependencies": True,
        "docker_test_env_configured": True,
        "fixture_isolation_clean": True,
    }
    good_rep = test_runtime.environment_validator.validate_environment_reproducibility(good_env)
    assert good_rep.status == "PASS"
    assert good_rep.reproducibility_score == 100.0

    bad_env = {
        "pinned_dependencies": False,
        "docker_test_env_configured": False,
        "fixture_isolation_clean": False,
    }
    bad_rep = test_runtime.environment_validator.validate_environment_reproducibility(bad_env)
    assert bad_rep.status == "FAIL"
    assert len(bad_rep.issues) == 3


def test_end_to_end_test_architecture_verification_and_api(test_runtime):
    """Verifies full execution pipeline, evidence package sealing, and in-process REST API."""
    package = test_runtime.run_full_verification(commit_sha="commit-abc-987")
    assert package.scorecard.composite_score >= 85.0
    assert package.scorecard.tier in [TestCertificationTier.ENTERPRISE_TEST_READY, TestCertificationTier.PRODUCTION_READY]
    assert package.package_sha256 != ""

    api = test_runtime.api
    scan_res = api.post_scan({"commit_sha": "commit-abc-987"})
    assert scan_res["status"] == "COMPLETED"
    assert "package_id" in scan_res

    report_res = api.get_report(scan_res["package_id"])
    assert report_res is not None
    assert "scorecard" in report_res
    assert report_res["commit_sha"] == "commit-abc-987"

    metrics_res = api.get_metrics()
    assert "supported_layers" in metrics_res
