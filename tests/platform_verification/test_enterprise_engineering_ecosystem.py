"""
Comprehensive Verification Test Suite for Part 1.1C.5:
Enterprise Testing, Tooling, Documentation & Deployment Architecture.
"""
import pytest
import os

from app.platform_verification.testing import (
    TestingPyramidRunner, TestTier, TestTierResult,
    PerformanceBenchmarkEngine,
    ChaosFaultInjector, ChaosFaultType, FaultInjectionConfig,
    MutationTestingHarness,
    TestEvidenceReporter
)
from tooling.datasets.dataset_generator import DatasetGenerator
from tooling.benchmarks.benchmark_runner import BenchmarkRunner
from tooling.migrations.migration_runner import MigrationRunner
from tooling.governance.documentation_validator import validate_docs
from app.infrastructure.deployment.rollback_manager import DeploymentRollbackManager
from app.infrastructure.observability import (
    HealthChecker, ProbeStatus, DeploymentMetadataProfiler, TelemetryCollector
)


class TestTestingArchitecture:
    def test_testing_pyramid_runner(self):
        runner = TestingPyramidRunner("ocr_evaluation")
        report = runner.execute_all_tiers()
        assert report.overall_passed is True
        assert report.pass_rate == 1.0
        assert len(report.tier_results) == 10

        # Custom tier failure handling
        runner.register_tier_handler(
            TestTier.SECURITY,
            lambda: TestTierResult(
                tier=TestTier.SECURITY,
                passed=False,
                total_tests=5,
                passed_tests=4,
                failed_tests=1,
                duration_ms=10.0,
                errors=["Vulnerability detected"]
            )
        )
        report_fail = runner.execute_all_tiers(stop_on_failure=True)
        assert report_fail.overall_passed is False

    def test_performance_benchmark_engine(self):
        engine = PerformanceBenchmarkEngine()
        res = engine.run_benchmark("json_serialization", lambda: {"key": "value"}, iterations=50, slo_p99_ms=10.0)
        assert res.latency.sample_count == 50
        assert res.throughput_rps > 0
        assert res.latency.p99_ms <= res.latency.max_ms

    def test_chaos_fault_injector(self):
        # Latency injection
        inj = ChaosFaultInjector(FaultInjectionConfig(fault_type=ChaosFaultType.LATENCY_INJECTION, delay_ms=1.0))
        inj.maybe_inject_fault()

        # Storage outage
        inj_storage = ChaosFaultInjector(FaultInjectionConfig(fault_type=ChaosFaultType.STORAGE_OUTAGE))
        with pytest.raises(IOError):
            inj_storage.maybe_inject_fault()

    def test_mutation_testing_harness(self):
        harness = MutationTestingHarness()
        # Test function asserts values are positive
        test_fn = lambda x: x > 0
        clean = [1, 2, 3]
        mutations = [-1, -2, -3, 0]
        res = harness.evaluate_test_strength("math_validator", test_fn, clean, mutations)
        assert res.mutation_score == 1.0
        assert res.passed_threshold is True

    def test_evidence_reporter(self):
        runner = TestingPyramidRunner("evidence_core")
        report = runner.execute_all_tiers()
        json_out = TestEvidenceReporter.to_json(report)
        md_out = TestEvidenceReporter.to_markdown(report)
        assert "evidence_core" in json_out
        assert "# Verification Platform Test Report" in md_out


class TestEngineeringTooling:
    def test_dataset_generator(self):
        data = DatasetGenerator.generate_dataset("HAPPY_PATH", sample_count=5)
        assert len(data["records"]) == 5
        assert len(data["sha256_fingerprint"]) == 64

    def test_benchmark_runner(self):
        res = BenchmarkRunner.benchmark_ai_inference(iterations=5)
        assert res["task"] == "AI_INFERENCE_EVALUATION"
        assert res["status"] in ["PASS", "FAIL"]

    def test_migration_runner(self):
        mgr = MigrationRunner()
        rec = mgr.apply_migration("m_001", "v1.1.0")
        assert rec.target_version == "v1.1.0"
        assert len(mgr.get_history()) == 1

    def test_documentation_validator(self):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        code = validate_docs(root)
        assert code == 0


class TestDeploymentAndObservability:
    def test_rollback_manager(self):
        mgr = DeploymentRollbackManager()
        rec = mgr.execute_rollback("v1.2.0", "v1.1.0", "Latency regression")
        assert rec.prior_version == "v1.2.0"
        assert rec.target_version == "v1.1.0"
        assert len(mgr.get_rollback_history()) == 1

    def test_health_checks(self):
        assert HealthChecker.is_healthy() is True
        ready = HealthChecker.check_readiness()
        assert ready.status == ProbeStatus.HEALTHY
        assert ready.checks["storage_cas"] is True

    def test_metadata_profiler(self):
        meta = DeploymentMetadataProfiler.get_metadata("staging")
        assert meta.environment == "staging"
        assert meta.version == "1.0.0"

    def test_telemetry_collector(self):
        tele = TelemetryCollector()
        tele.increment("verification_runs", 1)
        tele.gauge("p99_latency_ms", 15.4)
        snap = tele.get_snapshot()
        assert snap["counters"]["verification_runs"] == 1
        assert snap["metrics"]["p99_latency_ms"] == 15.4
