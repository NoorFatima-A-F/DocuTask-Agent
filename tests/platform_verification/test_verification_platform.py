"""
Unit and Integration Tests for Foundational Verification Platform Architecture (FVPA)
"""
from app.platform_verification.core.lifecycle_orchestrator import lifecycle_orchestrator
from app.platform_verification.core.statistical_engine import statistical_engine
from app.platform_verification.core.quality_gate_engine import quality_gate_engine
from app.platform_verification.core.provenance_tracker import provenance_tracker
from app.platform_verification.core.plugin_registry import plugin_registry
from app.platform_verification.infrastructure.evidence_store import evidence_store
from app.platform_verification.infrastructure.certification_authority import certification_authority
from app.platform_verification.domain.models import (
    VerificationDefinition, QualityGateRule, MetricResult, VerificationStatus,
    VerificationLifecycleStage
)

def test_plugin_registry_and_discovery():
    plugins = plugin_registry.list_plugins()
    assert len(plugins) >= 6
    plugin_names = [p["plugin_name"] for p in plugins]
    assert "ocr_verification_plugin" in plugin_names
    assert "ai_extraction_verification_plugin" in plugin_names
    assert "rag_evaluation_plugin" in plugin_names
    assert "agent_orchestration_plugin" in plugin_names
    assert "security_compliance_plugin" in plugin_names
    assert "chaos_resilience_plugin" in plugin_names

def test_statistical_engine_confidence_intervals():
    # Deterministic samples
    samples = [0.98, 0.99, 0.97, 0.99, 0.98, 0.985]
    ci = statistical_engine.calculate_confidence_interval(samples, confidence_level=0.95, baseline_comparison=0.95)
    assert ci.sample_size == 6
    assert ci.lower_bound > 0.96
    assert ci.upper_bound <= 1.0
    assert ci.p_value is not None
    assert ci.p_value < 0.05  # Statistically significantly higher than 0.95

def test_statistical_drift_detection():
    baseline = [0.98, 0.99, 0.97, 0.99, 0.98]
    drifted = [0.85, 0.84, 0.86, 0.83, 0.85]
    drift = statistical_engine.detect_distribution_drift(drifted, baseline, threshold_p_value=0.01)
    assert drift is True

    stable = [0.98, 0.985, 0.975, 0.98, 0.99]
    no_drift = statistical_engine.detect_distribution_drift(stable, baseline, threshold_p_value=0.01)
    assert no_drift is False

def test_quality_gate_evaluation():
    metrics = [
        MetricResult(metric_name="accuracy", category="DETERMINISTIC", value=0.99, target_threshold=0.95, passed=True),
        MetricResult(metric_name="latency_ms", category="PERFORMANCE", value=120.0, target_threshold=150.0, passed=True)
    ]
    rules = [
        QualityGateRule(rule_id="r1", metric_name="accuracy", operator=">=", threshold=0.95, is_hard_blocker=True),
        QualityGateRule(rule_id="r2", metric_name="latency_ms", operator="<=", threshold=150.0, is_hard_blocker=True)
    ]
    res = quality_gate_engine.evaluate_gates(metrics, rules)
    assert res.gate_passed is True
    assert res.hard_violations_count == 0

    # Test failure
    failing_rules = [
        QualityGateRule(rule_id="r3", metric_name="accuracy", operator=">=", threshold=0.999, is_hard_blocker=True)
    ]
    fail_res = quality_gate_engine.evaluate_gates(metrics, failing_rules)
    assert fail_res.gate_passed is False
    assert fail_res.hard_violations_count == 1

def test_evidence_sealing_and_tamper_verification():
    raw_data = {"test_batch_id": "batch-1234", "scores": [0.99, 0.98, 1.0], "model": "gemini-2.5-flash"}
    sealed = evidence_store.seal_evidence("run-test-01", raw_data)
    assert sealed.sha256_hash is not None
    assert sealed.byte_size > 0
    
    # Verify integrity
    is_valid = evidence_store.verify_integrity(sealed.evidence_id)
    assert is_valid is True

def test_provenance_and_environment_capture():
    profile = provenance_tracker.capture_environment_profile()
    assert profile.host_os is not None
    assert profile.python_version is not None
    assert len(profile.config_hash) > 0
    assert len(profile.prompt_hash) > 0

def test_complete_12_stage_verification_lifecycle():
    definition = VerificationDefinition(
        id="vdef-test-ocr",
        name="Unit Test OCR Verification",
        description="Verify OCR pipeline through 12 stages",
        plugin_name="ocr_verification_plugin",
        target_subsystem="OCR",
        repetition_count=5,
        quality_gates=[
            QualityGateRule(rule_id="qg-cer", metric_name="character_error_rate", operator="<=", threshold=0.02),
            QualityGateRule(rule_id="qg-wer", metric_name="word_error_rate", operator="<=", threshold=0.03)
        ]
    )
    run = lifecycle_orchestrator.execute_verification_run(definition)
    assert run.status == VerificationStatus.PASSED
    assert run.overall_score >= 0.90
    assert len(run.stage_history) == 12  # All 12 stages executed
    assert run.current_stage == VerificationLifecycleStage.STAGE_12_ARCHIVAL
    assert len(run.evidence_records) > 0
    assert run.certificate is not None
    assert run.certificate.is_valid is True

    # Validate certificate cryptographic signature
    is_cert_valid = certification_authority.verify_certificate(run.certificate)
    assert is_cert_valid is True
