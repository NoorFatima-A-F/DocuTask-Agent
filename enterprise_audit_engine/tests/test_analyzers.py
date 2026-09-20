"""Unit tests for Analyzers (Test Quality, API Contracts, AI Quality, Security, Benchmarks, Runtime)."""

from pathlib import Path
from enterprise_audit_engine.analyzers.test_quality_analyzer import TestQualityAnalyzer
from enterprise_audit_engine.analyzers.api_contract_verifier import APIContractVerifier
from enterprise_audit_engine.analyzers.ai_quality_verifier import AIQualityVerifier
from enterprise_audit_engine.analyzers.security_pipeline import SecurityPipelineVerifier
from enterprise_audit_engine.analyzers.benchmark_runner import BenchmarkRunnerVerifier
from enterprise_audit_engine.analyzers.runtime_verifier import RuntimeVerifier


def test_test_quality_analyzer(tmp_path: Path):
    test_file = tmp_path / "test_sample.py"
    test_file.write_text("""
def test_addition():
    x = 1 + 1
    assert x == 2
    assert x > 0
""", encoding="utf-8")

    res = TestQualityAnalyzer.analyze_test_directory(tmp_path)
    assert res["total_test_files"] == 1
    assert res["total_test_functions"] == 1
    assert res["total_assertions"] == 2
    assert res["assertion_density"] == 2.0


def test_security_pipeline_verifier(tmp_path: Path):
    clean_file = tmp_path / "service.py"
    clean_file.write_text("import os\nAPI_KEY = os.getenv('API_KEY')\n", encoding="utf-8")
    
    res = SecurityPipelineVerifier.scan_security_posture(tmp_path)
    assert res["secrets_detected_count"] == 0


def test_benchmark_runner_verifier(tmp_path: Path):
    res = BenchmarkRunnerVerifier.inspect_benchmarks(tmp_path)
    assert res["has_benchmark_suite"] is False
    assert res["benchmark_maturity"] == "LOW"


def test_runtime_verifier(tmp_path: Path):
    res = RuntimeVerifier.verify_runtime_environment(tmp_path)
    assert res["has_dockerfile"] is False
    assert res["runtime_readiness_score"] == 0.0
