"""
Test suite for Evidence-Driven Engineering Subsystem:
1. Evidence Registry & SHA-256 Hash Verification
2. Evidence Validator & Tamper Detection
3. Benchmark Collector Statistical Calculations
4. Traceability Engine Claim Binding
5. Production Readiness Assessment Framework
6. Chaos Engineering & Self-Healing Experiments
7. Golden Dataset Evaluation Harness
8. Cost Intelligence Unit Economics
9. FMEA & STRIDE Threat Engine
10. Master Evidence Generator End-to-End Execution
"""

import pytest
from pathlib import Path

from app.evidence.collectors.benchmark_collector import BenchmarkEvidenceCollector
from app.evidence.evaluators.chaos_suite import ChaosEngineeringPlatform
from app.evidence.evaluators.cost_intelligence import CostIntelligencePlatform
from app.evidence.evaluators.fmea_risk_engine import FMEARiskEngine
from app.evidence.evaluators.golden_dataset import GoldenDatasetEvaluationHarness
from app.evidence.evaluators.readiness_evaluator import ProductionReadinessEvaluator
from app.evidence.evaluators.scalability_suite import ScalabilityValidationLaboratory
from app.evidence.generators.evidence_generator import MasterEvidenceGenerator
from app.evidence.registry.evidence_models import EvidenceItem, EvidenceType, VerificationStatus
from app.evidence.registry.evidence_registry import EvidenceRegistry
from app.evidence.traceability.traceability_engine import EvidenceTraceabilityEngine
from app.evidence.validators.evidence_validator import EvidenceValidator


def test_evidence_registry_and_hash_integrity():
    """Test registry append, query, and SHA-256 calculation."""
    registry = EvidenceRegistry()
    item = EvidenceItem(
        evidence_id="evi_test_01",
        title="Unit Test Validation",
        description="Verified execution",
        evidence_type=EvidenceType.UNIT_TEST,
        source="tests/unit",
        generated_by="pytest",
        raw_payload={"tests": 10, "passed": 10},
    )
    reg_item = registry.register(item)
    assert reg_item.evidence_id == "evi_test_01"
    assert reg_item.item_hash == item.compute_hash()
    assert registry.count() == 1
    assert registry.get("evi_test_01") is not None


def test_evidence_validator_detects_hash_tampering():
    """Test validator catches altered payload or modified hash."""
    validator = EvidenceValidator()
    item = EvidenceItem(
        evidence_id="evi_test_tamper",
        title="Benchmark Result",
        description="P50=10ms",
        evidence_type=EvidenceType.BENCHMARK,
        source="benchmarks",
        generated_by="harness",
        raw_payload={"p50": 10.0},
    )
    assert validator.validate_item(item) is True

    # Mutate payload without recomputing hash
    item.raw_payload["p50"] = 1.0
    assert validator.validate_item(item) is False
    assert item.verification_status == VerificationStatus.HASH_MISMATCH


def test_benchmark_collector_statistics():
    """Test statistical computations (P50, P90, P95, P99, Mean, StdDev, Ops/s)."""
    latencies = [10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 50.0, 100.0]
    stats = BenchmarkEvidenceCollector.compute_stats("Memory Lookup", latencies, total_time_seconds=1.0)

    assert stats.iterations == 8
    assert stats.p50_latency_ms == 25.0
    assert stats.p95_latency_ms == 100.0
    assert stats.ops_per_second == 8.0
    assert stats.std_dev_ms > 0.0


def test_traceability_engine_verifies_claims():
    """Test claim verification against registered evidence."""
    registry = EvidenceRegistry()
    evi = EvidenceItem(
        evidence_id="evi_dag_mut",
        title="DAG Mutation Benchmark",
        description="Verified DAG mutation",
        evidence_type=EvidenceType.BENCHMARK,
        source="app.agents.planning",
        generated_by="harness",
    )
    registry.register(evi)

    trace_engine = EvidenceTraceabilityEngine(registry)
    claim = trace_engine.register_claim(
        claim_id="CLM-DAG",
        claim_text="Dynamic DAG mutates in-place on failure",
        subsystem="Planning",
        supporting_evidence_ids=["evi_dag_mut"],
    )
    assert claim.is_verified is True

    unsupported = trace_engine.register_claim(
        claim_id="CLM-UNSUPPORTED",
        claim_text="Magic 1000x speedup claim",
        subsystem="Runtime",
        supporting_evidence_ids=["non_existent_id"],
    )
    assert unsupported.is_verified is False


def test_production_readiness_framework_evaluation():
    """Test measurable readiness framework with checklist and evidence linking."""
    registry = EvidenceRegistry()
    evi = EvidenceItem(
        evidence_id="evi_test_green",
        title="Test Suite Passed",
        description="923 tests passed",
        evidence_type=EvidenceType.UNIT_TEST,
        source="tests/",
        generated_by="pytest",
    )
    registry.register(evi)

    readiness = ProductionReadinessEvaluator(registry)
    linked = readiness.link_evidence("TST-01", "evi_test_green")
    assert linked is True

    report = readiness.evaluate()
    assert report["total_criteria"] == 20
    assert report["passed_criteria"] >= 1


@pytest.mark.asyncio
async def test_chaos_engineering_experiments():
    """Test chaos platform fault injection and self-healing recovery."""
    chaos_lab = ChaosEngineeringPlatform()
    items = await chaos_lab.run_all_experiments()
    assert len(items) == 4
    for it in items:
        assert it.verification_status == VerificationStatus.VERIFIED
        assert it.raw_payload["recovered_successfully"] is True
        assert it.raw_payload["data_loss_detected"] is False


@pytest.mark.asyncio
async def test_scalability_laboratory_tiers():
    """Test scalability laboratory across concurrent worker tiers."""
    scale_lab = ScalabilityValidationLaboratory()
    items = await scale_lab.run_scalability_matrix(worker_tiers=[1, 5, 10])
    assert len(items) == 3
    for it in items:
        assert it.raw_payload["throughput_ops_sec"] > 0.0


def test_golden_dataset_evaluation_harness():
    """Test golden dataset evaluation accuracy and F1 score."""
    harness = GoldenDatasetEvaluationHarness()
    evi = harness.run_evaluation()
    assert evi.raw_payload["f1_score"] >= 0.95
    assert evi.raw_payload["total_samples"] == 6


def test_cost_intelligence_platform():
    """Test cost analytics, per-document unit economics, and monthly projection."""
    cost_intel = CostIntelligencePlatform()
    evi = cost_intel.generate_cost_evidence(monthly_volume_projection=100000)
    assert evi.raw_payload["average_cost_per_document_usd"] > 0.0
    assert evi.raw_payload["projected_monthly_cost_usd"] > 0.0


def test_fmea_and_stride_threat_engine():
    """Test FMEA Risk Priority Numbers and STRIDE threat mitigation."""
    engine = FMEARiskEngine()
    evi = engine.generate_fmea_evidence()
    assert evi.raw_payload["total_failure_modes_analyzed"] == 5
    assert evi.raw_payload["max_rpn"] > 0
    assert evi.raw_payload["stride_threats_count"] == 6


@pytest.mark.asyncio
async def test_master_evidence_generator_end_to_end(tmp_path: Path):
    """Test full MasterEvidenceGenerator execution pipeline."""
    generator = MasterEvidenceGenerator(workspace_root=tmp_path)
    result = await generator.generate_full_evidence_corpus()
    assert result["total_evidence_generated"] >= 15
    assert result["validated_passed"] == result["total_evidence_generated"]
    assert result["readiness_summary"]["passed_criteria"] >= 15
    assert Path(result["catalog_path"]).exists()
    assert Path(result["readiness_md_path"]).exists()
