"""Tests for Benchmark Certification and Repeatability Verifier."""

from app.runtime.benchmark_cert.benchmark_certifier import (
    BenchmarkCertifier,
    ReproducibilityVerifier,
)


def test_benchmark_certification():
    cert = BenchmarkCertifier.certify_benchmark(
        suite_name="finance_invoices_500",
        sample_size=500,
        throughput=52.4,
        latency_p95=210.0,
        accuracy_f1=0.995,
        cost_per_1k=1.18,
    )
    assert cert.suite_name == "finance_invoices_500"
    assert cert.reproducibility_score >= 0.99
    assert len(cert.merkle_leaf_hash) == 64
    assert cert.signature.startswith("sig_cert_")
    assert len(cert.confidence_interval_99) == 2


def test_repeatability_verifier():
    proof = ReproducibilityVerifier.verify_repeatability(num_runs=10)
    assert proof.total_runs == 10
    assert proof.all_runs_identical is True
    assert proof.variance_score < 0.001
