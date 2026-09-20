"""
Unit and integration tests for Phase V10 — Enterprise Performance, Scalability & Reliability Engineering Validation Program (EPSR-VP).
"""

import os
import json
import pytest

from app.performance_validation import (
    VerificationStatus,
    WorkloadComplexity,
    FailureType,
    ReliabilityTier,
    LatencyProfile,
    AICostMetric,
    ChaosExperimentResult,
    PerformanceAssertionResult,
    PillarPerformanceResult,
    PerformanceScorecard,
    BaselineBenchmarkVerifier,
    WorkloadGeneratorVerifier,
    AIPerformanceVerifier,
    LoadTestVerifier,
    StressTestVerifier,
    EnduranceScalingVerifier,
    DistributedResourceVerifier,
    CostOptimizerVerifier,
    ChaosEngineeringVerifier,
    DisasterRecoveryVerifier,
    SREReliabilityVerifier,
    ReliabilityDashboardVerifier,
    PerformanceScorer,
    PerformanceReportGenerator,
)


def test_domain_models():
    profile = LatencyProfile(
        endpoint="/api/v1/extract",
        p50_ms=100.0,
        p95_ms=250.0,
        p99_ms=400.0,
        sla_target_ms=500.0,
        requests_per_sec=300.0,
    )
    d = profile.to_dict()
    assert d["endpoint"] == "/api/v1/extract"
    assert d["p95_ms"] == 250.0

    cost = AICostMetric(
        operation="ocr_extraction",
        tokens_per_doc=2000,
        cost_per_doc=0.0015,
        caching_hit_rate_pct=85.0,
        savings_pct=50.0,
    )
    cd = cost.to_dict()
    assert cd["tokens_per_doc"] == 2000
    assert cd["savings_pct"] == 50.0


def test_part_01_baseline_verifier():
    v = BaselineBenchmarkVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_02_workload_verifier():
    v = WorkloadGeneratorVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_03_ai_metrics_verifier():
    v = AIPerformanceVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_04_load_testing_verifier():
    v = LoadTestVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_05_stress_testing_verifier():
    v = StressTestVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_06_scalability_verifier():
    v = EnduranceScalingVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_07_distributed_resources_verifier():
    v = DistributedResourceVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_08_cost_optimizer_verifier():
    v = CostOptimizerVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_09_chaos_verifier():
    v = ChaosEngineeringVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_10_disaster_recovery_verifier():
    v = DisasterRecoveryVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_11_sre_reliability_verifier():
    v = SREReliabilityVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_12_reliability_dashboard_verifier():
    v = ReliabilityDashboardVerifier()
    res = v.verify()
    assert res.score == 100.0
    assert res.status == VerificationStatus.PASSED
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_performance_scorer():
    scorer = PerformanceScorer()
    scorecard = scorer.run_all()
    assert scorecard.composite_score == 100.0
    assert scorecard.grade == "A+"
    assert scorecard.availability_pct >= 99.99
    assert scorecard.production_ready is True
    assert scorecard.total_assertions == 48
    assert scorecard.passed_assertions == 48
    assert len(scorecard.pillars) == 12


def test_performance_report_generator(tmp_path):
    scorer = PerformanceScorer()
    scorecard = scorer.run_all()

    exporter = PerformanceReportGenerator(
        output_dir=str(tmp_path / "reports"),
        report_path=str(tmp_path / "report.md"),
    )
    summary = exporter.export_all(scorecard)

    assert os.path.exists(summary["output_dir"])
    assert os.path.exists(summary["manifest_file"])
    assert os.path.exists(summary["report_path"])

    with open(summary["manifest_file"], "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert len(manifest["checksums"]) == 13  # 12 pillars + 1 summary
    assert "Phase V10" in manifest["verification_program"]
    assert manifest["composite_score"] == 100.0
