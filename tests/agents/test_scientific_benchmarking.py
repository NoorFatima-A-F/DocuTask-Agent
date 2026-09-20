"""
Unit tests for the Scientific Benchmarking Subsystem.
Verifies Timer Calibration, Advanced Statistics, Hardware Fingerprinting,
SLSA/W3C Provenance, Benchmark Isolation, Scientific Benchmark Runner, and Throughput Engine.
"""

import asyncio
import gc
import math
import pytest
from typing import List

from app.evidence.benchmarking.benchmark_runner import (
    ScientificBenchmarkResult,
    ScientificBenchmarkRunner,
    SteadyStateDetector,
)
from app.evidence.benchmarking.environment_fingerprint import (
    EnvironmentFingerprint,
    EnvironmentFingerprintEngine,
)
from app.evidence.benchmarking.isolation import (
    BenchmarkIsolationContext,
    BenchmarkIsolationSettings,
    WarmupManager,
)
from app.evidence.benchmarking.provenance import (
    EvidenceProvenanceEngine,
    EvidenceProvenanceRecord,
)
from app.evidence.benchmarking.statistics_engine import (
    AdvancedStatisticsEngine,
    ConfidenceInterval,
    DistributionType,
    FullStatisticalReport,
)
from app.evidence.benchmarking.throughput_engine import (
    LittlesLawVerification,
    ThroughputCurvePoint,
    ThroughputEngine,
)
from app.evidence.benchmarking.timer_calibration import (
    ClockSource,
    TimerCalibrationEngine,
    TimerCalibrationProfile,
)
from app.evidence.registry.evidence_models import EvidenceType, VerificationStatus
from app.evidence.registry.evidence_registry import EvidenceRegistry


class TestTimerCalibration:
    """Tests for hardware timer calibration engine."""

    def test_calibrate_perf_counter(self):
        engine = TimerCalibrationEngine(clock_source=ClockSource.PERF_COUNTER_NS)
        profile = engine.calibrate(sample_size=100)

        assert isinstance(profile, TimerCalibrationProfile)
        assert profile.clock_source == ClockSource.PERF_COUNTER_NS
        assert profile.timer_resolution_ns > 0.0
        assert profile.measurement_overhead_ns >= 0.0
        assert profile.noise_variance_ns2 >= 0.0
        assert profile.is_calibrated is True

        profile_dict = profile.to_dict()
        assert "timer_resolution_ns" in profile_dict
        assert "measurement_overhead_ns" in profile_dict
        assert profile_dict["is_calibrated"] is True

    def test_clock_sources(self):
        for clock_src in [ClockSource.PERF_COUNTER_NS, ClockSource.PROCESS_TIME_NS, ClockSource.MONOTONIC_NS]:
            engine = TimerCalibrationEngine(clock_source=clock_src)
            clock_fn = engine._resolve_clock(clock_src)
            t1 = clock_fn()
            t2 = clock_fn()
            assert t2 >= t1


class TestAdvancedStatisticsEngine:
    """Tests for scientific statistics calculation engine."""

    def test_statistical_analysis_normal_data(self):
        # Known synthetic sample
        samples = [10.0, 10.5, 11.0, 9.5, 10.2, 9.8, 10.1, 10.4, 9.9, 10.3]
        report = AdvancedStatisticsEngine.analyze(samples)

        assert isinstance(report, FullStatisticalReport)
        assert report.sample_size == 10
        assert 9.5 <= report.mean <= 11.0
        assert report.median == pytest.approx(10.15, rel=0.1)
        assert report.variance > 0.0
        assert report.std_dev > 0.0
        assert report.mad > 0.0
        assert report.cv > 0.0
        assert report.iqr > 0.0
        assert report.min_val == 9.5
        assert report.max_val == 11.0

        # Confidence intervals
        assert report.ci_95_t.lower_bound <= report.mean <= report.ci_95_t.upper_bound
        assert report.ci_99_t.lower_bound <= report.mean <= report.ci_99_t.upper_bound
        assert report.ci_95_bootstrap.lower_bound <= report.mean <= report.ci_95_bootstrap.upper_bound

        # Outlier checks
        assert report.outliers.iqr_outliers_count == 0

        # Export
        report_dict = report.to_dict()
        assert report_dict["sample_size"] == 10
        assert "percentiles" in report_dict
        assert "p50" in report_dict["percentiles"]
        assert "p95" in report_dict["percentiles"]
        assert "p99" in report_dict["percentiles"]

    def test_outlier_detection(self):
        # Sample with extreme outlier
        samples = [10.0] * 50 + [1000.0]
        report = AdvancedStatisticsEngine.analyze(samples)

        assert report.outliers.iqr_outliers_count >= 1
        assert report.outliers.zscore_outliers_count >= 1

    def test_edge_cases(self):
        # Empty array raises ValueError
        with pytest.raises(ValueError, match="Sample array cannot be empty"):
            AdvancedStatisticsEngine.analyze([])

        # Single element
        report_single = AdvancedStatisticsEngine.analyze([42.0])
        assert report_single.sample_size == 1
        assert report_single.mean == 42.0
        assert report_single.std_dev == 0.0

        # Constant elements
        report_const = AdvancedStatisticsEngine.analyze([5.0, 5.0, 5.0, 5.0])
        assert report_const.variance == 0.0
        assert report_const.cv == 0.0


class TestEnvironmentFingerprintEngine:
    """Tests for hardware environment fingerprint engine."""

    def test_capture_fingerprint(self):
        fingerprint = EnvironmentFingerprintEngine.capture_fingerprint(extra_metadata={"test_mode": True})

        assert isinstance(fingerprint, EnvironmentFingerprint)
        assert fingerprint.logical_cores >= 1
        assert fingerprint.ram_total_gb > 0.0
        assert len(fingerprint.python_version) > 0
        assert len(fingerprint.environment_hash) == 64  # SHA-256
        assert fingerprint.extra_metadata.get("test_mode") is True

        # Idempotent hash verification
        computed = fingerprint.compute_hash()
        assert computed == fingerprint.environment_hash

        fp_dict = fingerprint.to_dict()
        assert "os_name" in fp_dict
        assert "environment_hash" in fp_dict


class TestEvidenceProvenanceEngine:
    """Tests for SLSA Level 3 and W3C PROV provenance engine."""

    def test_create_provenance_record(self):
        input_data = {"prompt": "Analyze invoice", "model": "gemini-2.5-pro"}
        output_data = {"status": "SUCCESS", "confidence": 0.998}

        record = EvidenceProvenanceEngine.create_provenance(
            evidence_id="EVID-TEST-001",
            workflow_id="WF-TEST-1234",
            environment_hash="a" * 64,
            input_data=input_data,
            output_data=output_data,
            git_sha="b" * 40,
        )

        assert isinstance(record, EvidenceProvenanceRecord)
        assert record.evidence_id == "EVID-TEST-001"
        assert record.workflow_id == "WF-TEST-1234"
        assert len(record.input_hash) == 64
        assert len(record.output_hash) == 64
        assert len(record.provenance_hash) == 64
        assert record.slsa_predicate is not None
        assert record.slsa_predicate.invocation_id == "WF-TEST-1234"

        rec_dict = record.to_dict()
        assert rec_dict["evidence_id"] == "EVID-TEST-001"
        assert "slsa_predicate" in rec_dict


class TestBenchmarkIsolationAndWarmup:
    """Tests for benchmark execution isolation and warmup stabilization."""

    def test_isolation_context_gc(self):
        settings = BenchmarkIsolationSettings(
            disable_gc_during_measurement=True,
            collect_gc_before_run=True,
        )

        was_enabled = gc.isenabled()
        with BenchmarkIsolationContext(settings):
            assert not gc.isenabled()
        assert gc.isenabled() == was_enabled

    def test_warmup_manager_sync(self):
        call_count = 0

        def sample_work():
            nonlocal call_count
            call_count += 1

        iterations = WarmupManager.execute_warmup(sample_work, min_iterations=15, min_duration_ms=1.0)
        assert iterations >= 15
        assert call_count >= 15

    @pytest.mark.asyncio
    async def test_warmup_manager_async(self):
        call_count = 0

        async def sample_async_work():
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.0001)

        iterations = await WarmupManager.execute_async_warmup(sample_async_work, min_iterations=5, min_duration_ms=1.0)
        assert iterations >= 5
        assert call_count >= 5


class TestScientificBenchmarkRunner:
    """Tests for end-to-end scientific benchmark runner."""

    def test_steady_state_detector(self):
        # Stable samples (low variance)
        stable_samples = [100.0, 101.0, 99.5, 100.5, 100.0, 101.2, 99.8, 100.1, 100.4, 100.2]
        assert SteadyStateDetector.is_steady(stable_samples, max_cv_threshold=0.15) is True

        # Unstable samples (high variance)
        unstable_samples = [10.0, 100.0, 5.0, 200.0, 12.0, 300.0, 8.0, 150.0, 2.0, 500.0]
        assert SteadyStateDetector.is_steady(unstable_samples, max_cv_threshold=0.15) is False

    def test_run_benchmark_sync(self):
        registry = EvidenceRegistry()
        runner = ScientificBenchmarkRunner(registry=registry)

        counter = 0

        def work():
            nonlocal counter
            counter += 1
            # Some trivial computation
            _ = [x ** 2 for x in range(100)]

        result, evidence = runner.run_benchmark(
            name="micro_math_loop",
            func=work,
            iterations=50,
            warmup_iterations=10,
        )

        assert isinstance(result, ScientificBenchmarkResult)
        assert result.benchmark_name == "micro_math_loop"
        assert result.iterations == 50
        assert result.statistics.mean > 0.0
        assert len(result.raw_samples_ns) == 50
        assert evidence.verification_status == VerificationStatus.VERIFIED
        assert evidence.evidence_type == EvidenceType.PERFORMANCE_TEST
        assert evidence.item_hash != ""

    @pytest.mark.asyncio
    async def test_run_benchmark_async(self):
        registry = EvidenceRegistry()
        runner = ScientificBenchmarkRunner(registry=registry)

        async def async_work():
            await asyncio.sleep(0.0001)

        result, evidence = await runner.run_async_benchmark(
            name="micro_async_sleep",
            coro_func=async_work,
            iterations=15,
            warmup_iterations=5,
        )

        assert isinstance(result, ScientificBenchmarkResult)
        assert result.benchmark_name == "micro_async_sleep"
        assert result.iterations == 15
        assert evidence.verification_status == VerificationStatus.VERIFIED


class TestThroughputEngine:
    """Tests for throughput measurement and Little's Law validation."""

    def test_calculate_throughput(self):
        rate = ThroughputEngine.calculate_throughput(completed_ops=500, elapsed_seconds=2.5)
        assert rate == pytest.approx(200.0)

        # Zero duration guard
        assert ThroughputEngine.calculate_throughput(completed_ops=100, elapsed_seconds=0.0) == 0.0

    def test_verify_littles_law(self):
        # Concurrency L = 10, Throughput lambda = 100 ops/sec, Mean latency W = 100ms (0.1s)
        # Predicted L = 100 * 0.1 = 10 -> Error = 0%
        result = ThroughputEngine.verify_littles_law(
            concurrency=10,
            throughput_ops_sec=100.0,
            mean_latency_ms=100.0,
            tolerance_pct=10.0,
        )

        assert isinstance(result, LittlesLawVerification)
        assert result.observed_concurrency_L == 10.0
        assert result.predicted_concurrency == pytest.approx(10.0)
        assert result.error_percentage == pytest.approx(0.0)
        assert result.law_holds is True

        res_dict = result.to_dict()
        assert res_dict["law_holds"] is True

    def test_saturation_curve_generation(self):
        # Concurrency points: (concurrency, throughput, mean_lat, p95_lat)
        points = [
            (1, 100.0, 10.0, 12.0),
            (10, 850.0, 11.5, 14.0),
            (50, 2500.0, 20.0, 28.0),
        ]
        curve = ThroughputEngine.build_saturation_curve(points)

        assert len(curve) == 3
        assert isinstance(curve[0], ThroughputCurvePoint)
        assert curve[0].concurrency == 1
        assert curve[0].saturation_index >= 0.0
