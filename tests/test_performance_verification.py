"""
Comprehensive Unit and Integration Test Suite for Phase V10 — Enterprise Performance, Scalability & Reliability Verification Program (EPSRV).
"""

import os
import pytest
from app.performance_verification.domain.models import (
    PerformanceStatus,
    ChaosFailureType,
    LatencyDistribution,
)
from app.performance_verification.infrastructure.latency_analyzer import LatencyAnalyzer
from app.performance_verification.infrastructure.metric_collector import MetricCollector
from app.performance_verification.infrastructure.resource_profiler import ResourceProfiler
from app.performance_verification.infrastructure.benchmark_engine import BenchmarkEngine
from app.performance_verification.latency.api_latency_benchmarks import APILatencyBenchmark
from app.performance_verification.latency.ai_pipeline_latency import AIPipelineLatencyAnalyzer
from app.performance_verification.throughput.document_throughput_tests import DocumentThroughputVerifier
from app.performance_verification.throughput.agent_throughput_tests import AgentThroughputVerifier
from app.performance_verification.workload_testing.load_tests import EnterpriseLoadTester
from app.performance_verification.workload_testing.stress_tests import StressBoundaryTester
from app.performance_verification.workload_testing.spike_tests import SpikeResilienceTester
from app.performance_verification.workload_testing.endurance_tests import EnduranceSoakTester
from app.performance_verification.efficiency.resource_efficiency_tests import ResourceEfficiencyVerifier
from app.performance_verification.efficiency.ai_cost_evaluator import AICostEvaluator
from app.performance_verification.resilience.chaos_engine import ChaosEngineeringEngine
from app.performance_verification.resilience.disaster_recovery_tests import DisasterRecoveryVerifier
from app.performance_verification.reliability.reliability_evaluator import PlatformReliabilityEvaluator
from app.performance_verification.reliability.observability_verifier import ObservabilityVerifier
from app.performance_verification.reliability.readiness_scorer import ReadinessScorer
from app.performance_verification.reporting.evidence_generator import PerformanceEvidenceGenerator


class TestPerformanceInfrastructure:
    """Test suite for metrics, profiling, and latency analytics."""

    def test_latency_analyzer_percentiles(self):
        samples = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
        dist = LatencyAnalyzer.compute_distribution(samples, sla_target_p95_ms=120.0)

        assert dist.sample_count == 10
        assert dist.p50_ms == pytest.approx(55.0, abs=1.0)
        assert dist.max_ms == 100.0
        assert dist.mean_ms == 55.0
        assert dist.sla_met is True

    def test_latency_analyzer_empty_samples(self):
        dist = LatencyAnalyzer.compute_distribution([], sla_target_p95_ms=500.0)
        assert dist.sample_count == 0
        assert dist.p50_ms == 0.0
        assert dist.sla_met is True

    def test_latency_histogram_bucketing(self):
        samples = [25.0, 45.0, 80.0, 150.0, 300.0, 1200.0, 6000.0]
        histogram = LatencyAnalyzer.bucket_histogram(samples)
        assert histogram["<=50.0ms"] == 2
        assert histogram["<=100.0ms"] == 1
        assert histogram[">5000.0ms"] == 1

    def test_metric_collector_aggregations(self):
        collector = MetricCollector()
        collector.record("cpu_usage", "infra", 20.0, "%")
        collector.record("cpu_usage", "infra", 40.0, "%")
        collector.record("llm_tokens", "ai", 1500.0, "tokens")

        summary = collector.get_summary()
        assert "infra" in summary
        assert summary["infra"]["cpu_usage"]["avg"] == 30.0
        assert summary["infra"]["cpu_usage"]["min"] == 20.0
        assert summary["infra"]["cpu_usage"]["max"] == 40.0
        assert summary["ai"]["llm_tokens"]["avg"] == 1500.0

    def test_resource_profiler_and_efficiency(self):
        profile = ResourceProfiler.profile_runtime()
        assert profile.cpu_returns_to_baseline is True
        assert profile.memory_reclaimed_pct > 90.0
        assert profile.db_connection_exhaustion is False
        assert profile.storage_growth_mb_per_1k_docs > 0.0

    def test_benchmark_engine_execution(self):
        engine = BenchmarkEngine(seed=123)
        res = engine.run_workload(
            name="test_workload",
            iterations=50,
            concurrency=10,
            base_latency_ms=100.0,
            jitter_ms=20.0,
        )
        assert res["iterations"] == 50
        assert res["errors"] == 0
        assert res["status"] in [PerformanceStatus.OPTIMAL, PerformanceStatus.ACCEPTABLE]


class TestLatencyBenchmarks:
    """Test suite for API and AI pipeline latency verification."""

    def test_api_latency_benchmarks_all_endpoints(self):
        bench = APILatencyBenchmark()
        results = bench.run_all_endpoints(iterations_per_endpoint=50)

        assert "POST /api/v1/documents/upload" in results
        assert "GET /api/v1/documents/{id}/status" in results
        assert "POST /api/v1/search/hybrid" in results
        assert "POST /api/v1/agents/execute" in results

        for ep, dist in results.items():
            assert dist.sla_met is True
            assert dist.p95_ms <= dist.sla_target_p95_ms

    def test_ai_pipeline_latency_breakdown(self):
        breakdown = AIPipelineLatencyAnalyzer.measure_invoice_pipeline()
        assert breakdown.pipeline_name == "End-to-End Invoice Intelligence Pipeline"
        assert breakdown.sla_met is True
        assert len(breakdown.stages) == 5

        total_pct = sum(s.percentage_of_total for s in breakdown.stages)
        assert total_pct == pytest.approx(100.0, abs=0.5)


class TestThroughputAndScalability:
    """Test suite for document and agent throughput."""

    def test_document_throughput_tiers(self):
        tiers = DocumentThroughputVerifier.evaluate_throughput_tiers()
        assert len(tiers) == 3
        for t in tiers:
            assert t.completion_rate_pct == 100.0
            assert t.failed_jobs == 0
            assert t.achieved_volume_per_hr >= t.target_volume_per_hr

    def test_agent_swarm_throughput(self):
        swarm = AgentThroughputVerifier.evaluate_swarm_throughput(100, 500, 1000)
        assert swarm["agent_count"] == 100
        assert swarm["task_count"] == 500
        assert swarm["deadlocks_detected"] == 0
        assert swarm["result"].completion_rate_pct == 100.0


class TestWorkloadTesting:
    """Test suite for load, stress, spike, and soak testing."""

    def test_enterprise_load_scenarios(self):
        scenarios = EnterpriseLoadTester.run_scenarios(scale_factor=0.5)
        assert len(scenarios) == 2
        for s in scenarios:
            assert s.error_rate_pct == 0.0
            assert s.status == PerformanceStatus.OPTIMAL
            assert s.latency_dist.sla_met is True

    def test_stress_testing_boundaries(self):
        boundaries = StressBoundaryTester.identify_capacity_boundaries()
        assert len(boundaries) == 5
        classes = [b.classification for b in boundaries]
        assert "STABLE" in classes
        assert "WARNING" in classes
        assert "CRITICAL" in classes

    def test_spike_resilience(self):
        spike = SpikeResilienceTester.run_spike_test(50, 1000)
        assert spike.dropped_jobs == 0
        assert spike.queue_backpressure_engaged is True
        assert spike.recovery_time_sec < 5.0
        assert spike.status == PerformanceStatus.OPTIMAL

    def test_endurance_soak_stability(self):
        soak = EnduranceSoakTester.run_soak_test(duration_hours=72)
        assert soak.duration_simulated_hrs == 72
        assert soak.memory_leak_detected is False
        assert soak.memory_growth_gradient_mb_hr < 0.05
        assert soak.latency_drift_pct < 10.0
        assert soak.stability_rating == "EXCELLENT"


class TestEfficiencyAndCostEconomics:
    """Test suite for resource footprint and AI cost ROI."""

    def test_resource_efficiency_verifier(self):
        prof = ResourceEfficiencyVerifier.verify_resource_efficiency()
        assert prof.cpu_returns_to_baseline is True
        assert prof.memory_reclaimed_pct > 90.0
        assert prof.db_connection_pool_active < prof.db_connection_pool_max

    def test_ai_cost_evaluator(self):
        profiles = AICostEvaluator.evaluate_cost_profiles()
        assert len(profiles) == 3
        for p in profiles:
            assert p.cost_reduction_pct > 95.0
            assert p.roi_multiple > 100.0
            assert p.annual_savings_100k_docs > 100000.0


class TestChaosAndResilience:
    """Test suite for failure injection and disaster recovery."""

    def test_chaos_failure_injections(self):
        scenarios = ChaosEngineeringEngine.run_all_failure_scenarios()
        assert len(scenarios) == 5
        for s in scenarios:
            assert s.injected is True
            assert s.auto_recovered is True
            assert s.data_corrupted is False

    def test_disaster_recovery_metrics(self):
        dr = DisasterRecoveryVerifier.verify_dr_capabilities()
        assert dr.backup_snapshot_valid is True
        assert dr.rto_compliant is True
        assert dr.rpo_compliant is True
        assert dr.rto_minutes_achieved < dr.rto_target_minutes
        assert dr.rpo_minutes_achieved < dr.rpo_target_minutes


class TestReliabilityObservabilityAndScoring:
    """Test suite for reliability math, distributed tracing, and readiness scoring."""

    def test_platform_reliability_evaluator(self):
        rel = PlatformReliabilityEvaluator.evaluate_reliability()
        assert rel.availability_pct >= 99.90
        assert rel.error_rate_pct < 0.10
        assert rel.sla_met is True

    def test_observability_verifier(self):
        trace = ObservabilityVerifier.verify_trace_propagation()
        assert trace.trace_id.startswith("trace-")
        assert trace.spans_count >= 5
        assert trace.structured_logging_compliant is True
        assert trace.otel_context_propagated is True

    def test_readiness_scorer_perfect(self):
        score = ReadinessScorer.calculate_score(100.0, 100.0, 100.0, 100.0)
        assert score.overall_readiness_score == 100.0
        assert score.grade == "A+"
        assert score.certification_status == "ENTERPRISE PRODUCTION HARDENED"

    def test_readiness_scorer_degraded(self):
        score = ReadinessScorer.calculate_score(85.0, 80.0, 75.0, 70.0)
        assert score.overall_readiness_score < 90.0
        assert score.grade == "C"


class TestEvidenceGenerator:
    """Test suite for artifact export and SHA-256 manifest generation."""

    def test_evidence_export_and_manifest(self, tmp_path):
        base_dir = str(tmp_path)
        bench = APILatencyBenchmark()
        api_latencies = bench.run_all_endpoints(iterations_per_endpoint=20)
        pipeline = AIPipelineLatencyAnalyzer.measure_invoice_pipeline()
        tiers = DocumentThroughputVerifier.evaluate_throughput_tiers()
        swarm = AgentThroughputVerifier.evaluate_swarm_throughput(10, 50, 100)
        load_tests = EnterpriseLoadTester.run_scenarios(scale_factor=0.1)
        stress = StressBoundaryTester.identify_capacity_boundaries()
        spike = SpikeResilienceTester.run_spike_test(10, 100)
        soak = EnduranceSoakTester.run_soak_test(24)
        res_prof = ResourceEfficiencyVerifier.verify_resource_efficiency(100)
        costs = AICostEvaluator.evaluate_cost_profiles()
        chaos = ChaosEngineeringEngine.run_all_failure_scenarios()
        dr = DisasterRecoveryVerifier.verify_dr_capabilities()
        rel = PlatformReliabilityEvaluator.evaluate_reliability(1000, 0)
        trace = ObservabilityVerifier.verify_trace_propagation()
        score = ReadinessScorer.calculate_score()

        manifest = PerformanceEvidenceGenerator.export_all_evidence(
            base_dir=base_dir,
            api_latencies=api_latencies,
            pipeline_breakdown=pipeline,
            throughput_tiers=tiers,
            agent_swarm_res=swarm,
            load_test_results=load_tests,
            stress_boundaries=stress,
            spike_result=spike,
            endurance_result=soak,
            resource_profile=res_prof,
            cost_profiles=costs,
            chaos_results=chaos,
            dr_metric=dr,
            reliability_metric=rel,
            trace_sample=trace,
            readiness_score=score,
        )

        assert "artifacts" in manifest
        assert len(manifest["artifacts"]) >= 8
        for name, meta in manifest["artifacts"].items():
            assert os.path.exists(meta["path"])
            assert len(meta["sha256"]) == 64
            assert meta["size_bytes"] > 0
