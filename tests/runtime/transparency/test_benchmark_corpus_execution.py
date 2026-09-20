"""
Test Suite: Multi-Corpus Benchmark Execution & Report Generation
Validates automated corpus execution across invoices/taxes/medical records and official evaluation dossier generation.
"""
import pytest
from app.runtime.benchmark_platform.corpus_runner import MultiCorpusBenchmarkRunner
from app.runtime.benchmark_platform.report_generator import BenchmarkReportGenerator


def test_multi_corpus_benchmark_runner_execution():
    runner = MultiCorpusBenchmarkRunner()
    
    corpora = runner.list_corpora()
    assert len(corpora) >= 3
    
    # Run specific corpus benchmark
    res = runner.run_benchmark("corp_invoices_100")
    assert res is not None
    assert res["status"] == "COMPLETED"
    scorecard = res["scorecard"]
    assert scorecard["document_count"] == 100
    assert scorecard["f1_score"] >= 0.95
    assert scorecard["passed_invariants_pct"] == 100.0


def test_benchmark_report_generator_dossier():
    dossier = BenchmarkReportGenerator.generate_full_dossier()
    
    assert dossier["total_evaluated_documents"] >= 300
    assert dossier["overall_macro_f1"] >= 0.95
    assert dossier["invariant_compliance"] == "100.0%"
    assert len(dossier["corpora"]) >= 3
    assert "reproducibility_proof" in dossier
