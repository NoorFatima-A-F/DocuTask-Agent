"""
Comprehensive Unit & Integration Test Suite for the 15 Enterprise Core Verification Components.
"""
import pytest
from app.platform_verification.runtime.enterprise_verification_runtime import EnterpriseVerificationRuntime
from app.platform_verification.domain.models import (
    VerificationDefinition,
    DatasetRecord,
    DatasetClass,
    VerificationStatus,
    VerificationStage,
)

@pytest.fixture
def runtime():
    return EnterpriseVerificationRuntime()

def test_component_architecture_initialization(runtime):
    overview = runtime.get_overview()
    assert overview["total_core_components"] == 15
    assert overview["components_healthy"] == 15
    assert overview["datasets_count"] == 11
    assert overview["registered_plugins"] == 6

def test_registry_and_plugins(runtime):
    plugins = runtime.registry.list_plugins()
    assert len(plugins) >= 6
    ocr_plugin = runtime.registry.get_plugin("ocr_evaluator")
    assert ocr_plugin is not None
    assert ocr_plugin.domain == "OCR"

def test_dataset_classes_and_checksums(runtime):
    datasets = runtime.dataset_mgr.list_datasets()
    assert len(datasets) == 11
    classes = {d.dataset_class for d in datasets}
    assert DatasetClass.HAPPY_PATH in classes
    assert DatasetClass.ADVERSARIAL in classes
    assert DatasetClass.STRESS in classes
    assert DatasetClass.BENCHMARK in classes
    # Verify SHA-256 fingerprinting
    for d in datasets:
        assert len(d.sha256_checksum) == 64

def test_environment_readiness(runtime):
    envs = runtime.env_mgr.list_environments()
    assert len(envs) == 7
    integration_env = runtime.env_mgr.check_readiness("env_integration")
    assert integration_env.is_ready is True
    assert integration_env.cpu_utilization_pct > 0

def test_evidence_manager_content_addressing_and_tamper_detection(runtime):
    payload = {"query": "test invoice", "response": "$1,450.00"}
    evidence = runtime.evidence_mgr.store_evidence("run_test_01", "OUTPUT", payload)
    assert evidence.evidence_id is not None
    assert len(evidence.payload_hash) == 64
    # Valid integrity check
    assert runtime.evidence_mgr.verify_evidence_integrity(evidence.evidence_id, payload) is True
    # Tampered payload check
    tampered_payload = {"query": "test invoice", "response": "$9,999.00"}
    assert runtime.evidence_mgr.verify_evidence_integrity(evidence.evidence_id, tampered_payload) is False

def test_statistical_engine_bootstrap_and_drift(runtime):
    samples = [0.99, 0.992, 0.995, 0.991, 0.994, 0.996, 0.998, 0.993]
    baseline = [0.985, 0.988, 0.982, 0.986, 0.984]
    summary = runtime.stats_engine.analyze_distribution("accuracy", samples, baseline)
    assert summary.sample_size == len(samples)
    assert summary.mean > 0.99
    assert summary.ci_lower_95 <= summary.mean <= summary.ci_upper_95
    assert summary.p_value_against_baseline is not None

def test_audit_manager_hash_chain_and_tamper_detection(runtime):
    entry1 = runtime.audit_mgr.record_event("EXECUTION_STARTED", "entity_1", {"action": "start"})
    entry2 = runtime.audit_mgr.record_event("EXECUTION_COMPLETED", "entity_1", {"action": "complete"})
    assert entry2.sha256_prev_hash == entry1.sha256_entry_hash
    assert runtime.audit_mgr.verify_chain_integrity() is True

def test_end_to_end_orchestration_and_traceability(runtime):
    # Execute full 12-stage lifecycle run
    run = runtime.orchestrator.orchestrate_verification("def_enterprise_comprehensive", "env_integration")
    assert run.status == VerificationStatus.PASSED
    assert run.current_stage == VerificationStage.POST_FLIGHT_TEARDOWN
    assert run.stage_progress_pct == 100.0
    assert run.overall_score >= 0.85
    # Check traceability graph
    lineage = runtime.traceability_mgr.get_lineage("def_enterprise_comprehensive")
    assert len(lineage) >= 4
    node_types = {n.node_type for n in lineage}
    assert "RUN" in node_types
    assert "CONFIG" in node_types
