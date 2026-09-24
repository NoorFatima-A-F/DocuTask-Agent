"""Tests for External Calibration Benchmark Suite."""

from enterprise_audit_engine.benchmark.benchmark_suite import (
    ExternalBenchmarkSuite,
    BenchmarkSuiteReport,
)


def test_benchmark_suite_accuracy():
    rep = ExternalBenchmarkSuite.run_all_benchmarks()

    assert isinstance(rep, BenchmarkSuiteReport)
    assert rep.overall_calibration_accuracy == 100.0
    assert rep.status == "BENCHMARK_CALIBRATED"
    assert rep.total_archetypes_tested == 3
    assert rep.archetypes_passed == 3


def test_benchmark_archetypes_discrimination():
    rep = ExternalBenchmarkSuite.run_all_benchmarks()

    archetype_map = {r.archetype_name: r for r in rep.results}
    assert archetype_map["GOOD_ENTERPRISE_SYSTEM"].actual_outcome == "PASS"
    assert archetype_map["VULNERABLE_SYSTEM"].actual_outcome == "FAIL"
    assert archetype_map["MISLEADING_SYSTEM_WITH_INFLATED_CLAIMS"].actual_outcome == "DETECTED_AND_BLOCKED"
