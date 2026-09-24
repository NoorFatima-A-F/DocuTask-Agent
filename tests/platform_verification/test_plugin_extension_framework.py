"""
Comprehensive Unit & Integration Test Suite for Part 1.1F:
Enterprise Verification Extension Framework, Interfaces & Plugin Architecture (EV-EFIPA).
"""
import pytest
from app.platform_verification.extension_framework.domain.models import (
    PluginMetadata,
    PluginLifecycleState,
    PluginHealthState,
    PluginPermission,
    PluginSecurityContext,
    PluginDependencyDeclaration,
    SecurityClassification,
)
from app.platform_verification.extension_framework.core.registry import PluginRegistry
from app.platform_verification.extension_framework.core.lifecycle import PluginLifecycleManager
from app.platform_verification.extension_framework.core.security import plugin_security_manager
from app.platform_verification.extension_framework.core.health import plugin_health_monitor
from app.platform_verification.extension_framework.core.dependencies import plugin_dependency_validator
from app.platform_verification.extension_framework.core.configuration import plugin_config_engine
from app.platform_verification.extension_framework.tooling.scaffolding import plugin_scaffolder
from app.platform_verification.extension_framework.tooling.validator import plugin_contract_validator
from app.platform_verification.extension_framework.tooling.docs_generator import plugin_doc_generator
from app.platform_verification.extension_framework.plugins.ocr_plugin import OCRVerificationPlugin
from app.platform_verification.extension_framework.plugins.ai_extraction_plugin import AIExtractionEvaluationPlugin
from app.platform_verification.extension_framework.runtime.extension_framework_runtime import extension_framework_runtime


def test_plugin_metadata_and_capabilities():
    ocr_p = OCRVerificationPlugin()
    meta = ocr_p.metadata

    assert meta.plugin_id == "ocr_verification_plugin"
    assert meta.version == "2.0.0"
    assert "character_error_rate" in meta.capabilities
    assert "word_error_rate" in meta.capabilities
    assert PluginPermission.READ_DATASET in meta.granted_permissions
    assert meta.security_classification == SecurityClassification.INTERNAL


def test_plugin_contract_validator():
    ocr_p = OCRVerificationPlugin()
    is_valid, errors = plugin_contract_validator.validate_plugin_instance(ocr_p)
    assert is_valid is True
    assert len(errors) == 0

    # Test invalid mock object
    class NonCompliantPlugin:
        pass

    invalid_p = NonCompliantPlugin()
    is_valid, errors = plugin_contract_validator.validate_plugin_instance(invalid_p)
    assert is_valid is False
    assert any("does not inherit" in e for e in errors)


def test_plugin_registry_and_capability_indexing():
    reg = PluginRegistry()
    ocr_p = OCRVerificationPlugin()
    ai_p = AIExtractionEvaluationPlugin()

    reg.register_plugin(ocr_p)
    reg.register_plugin(ai_p)

    assert len(reg.list_plugins()) == 2
    assert reg.get_plugin("ocr_verification_plugin") is not None

    # Test capability search
    ocr_plugins = reg.list_plugins(capability="character_error_rate")
    assert len(ocr_plugins) == 1
    assert ocr_plugins[0].plugin_id == "ocr_verification_plugin"

    ai_plugins = reg.list_plugins(capability="entity_f1_score")
    assert len(ai_plugins) == 1
    assert ai_plugins[0].plugin_id == "ai_extraction_eval_plugin"

    # Unregister
    assert reg.unregister_plugin("ocr_verification_plugin") is True
    assert reg.get_plugin("ocr_verification_plugin") is None


def test_plugin_lifecycle_10_state_machine():
    lm = PluginLifecycleManager()
    pid = "custom_test_plugin"

    lm.set_initial_state(pid, PluginLifecycleState.DISCOVERED)
    assert lm.get_state(pid) == PluginLifecycleState.DISCOVERED

    # Valid progression
    lm.transition_state(pid, PluginLifecycleState.VALIDATED, "Schema validated")
    assert lm.get_state(pid) == PluginLifecycleState.VALIDATED

    lm.transition_state(pid, PluginLifecycleState.REGISTERED, "Registered in catalogue")
    lm.transition_state(pid, PluginLifecycleState.INITIALIZED, "Model weights loaded")
    lm.transition_state(pid, PluginLifecycleState.READY, "Warmup complete")
    lm.transition_state(pid, PluginLifecycleState.EXECUTING, "Running verification workload")
    lm.transition_state(pid, PluginLifecycleState.READY, "Workload complete")
    assert lm.get_state(pid) == PluginLifecycleState.READY

    # Illegal transition (READY -> VALIDATED)
    with pytest.raises(ValueError) as exc:
        lm.transition_state(pid, PluginLifecycleState.VALIDATED)
    assert "Illegal state transition" in str(exc.value)

    # Audit trail check
    trail = lm.get_audit_trail(pid)
    assert len(trail) >= 6


def test_plugin_security_permissions_enforcement():
    # 1. Authorized context
    auth_ctx = PluginSecurityContext(
        caller_identity="TestRunner",
        permissions=[PluginPermission.READ_DATASET, PluginPermission.WRITE_EVIDENCE]
    )
    is_auth, msg = plugin_security_manager.validate_permissions(PluginPermission.READ_DATASET, auth_ctx)
    assert is_auth is True

    # 2. Denied context
    unauth_ctx = PluginSecurityContext(
        caller_identity="UntrustedGuest",
        permissions=[PluginPermission.EXECUTE_CODE]
    )
    is_auth, msg = plugin_security_manager.validate_permissions(PluginPermission.READ_DATASET, unauth_ctx)
    assert is_auth is False
    assert "Missing required permission" in msg


def test_plugin_execution_adapter_sandboxing():
    # Setup runtime with registered plugin
    res = extension_framework_runtime.execute_verification_plugin(
        plugin_id="ocr_verification_plugin",
        verification_id="ver_run_1001",
        dataset_ref={"name": "invoice_ocr_v1"}
    )
    assert res.is_success is True
    assert res.plugin_id == "ocr_verification_plugin"
    assert res.execution_time_ms >= 0.0
    assert len(res.metrics) >= 3
    assert any(m["metric"] == "character_error_rate" for m in res.metrics)
    assert "cer_samples" in res.raw_evidence


def test_plugin_health_monitor():
    pid = "ocr_verification_plugin"
    health = plugin_health_monitor.get_health(pid)
    assert health.total_executions >= 1
    assert health.success_rate == 1.0
    assert health.state == PluginHealthState.HEALTHY

    # Simulate failures
    for _ in range(5):
        plugin_health_monitor.record_execution(pid, is_success=False, latency_ms=100.0, error="Simulated GPU OOM")

    updated_health = plugin_health_monitor.get_health(pid)
    assert updated_health.failed_executions >= 5
    assert updated_health.success_rate < 0.70
    assert updated_health.state == PluginHealthState.UNHEALTHY


def test_plugin_dependency_validation():
    meta = PluginMetadata(
        plugin_id="complex_rag_plugin",
        name="Complex RAG Plugin",
        description="Plugin with strict dependencies",
        dependencies=[
            PluginDependencyDeclaration(name="ocr_verification_plugin", min_version="1.5.0"),
            PluginDependencyDeclaration(name="non_existent_plugin", min_version="1.0.0", is_optional=False)
        ]
    )

    available = {"ocr_verification_plugin": "2.0.0"}
    is_valid, errors = plugin_dependency_validator.validate_dependencies(meta, available)
    assert is_valid is False
    assert any("Missing required plugin dependency: 'non_existent_plugin'" in e for e in errors)


def test_plugin_configuration_engine():
    schema = {
        "properties": {
            "timeout_seconds": {"type": "integer", "default": 60},
            "strict_mode": {"type": "boolean", "default": True},
            "api_key": {"type": "string"}
        },
        "required": ["api_key"]
    }

    # 1. Valid with defaults applied
    raw_cfg = {"api_key": "secret-xyz"}
    resolved, errors = plugin_config_engine.validate_and_apply_defaults(raw_cfg, schema)
    assert len(errors) == 0
    assert resolved["timeout_seconds"] == 60
    assert resolved["strict_mode"] is True
    assert resolved["api_key"] == "secret-xyz"

    # 2. Missing required
    bad_cfg = {"timeout_seconds": 120}
    resolved, errors = plugin_config_engine.validate_and_apply_defaults(bad_cfg, schema)
    assert any("Missing required plugin configuration property: 'api_key'" in e for e in errors)


def test_plugin_scaffolding_and_docs_generation():
    # 1. Scaffolding
    scaffold = plugin_scaffolder.generate_plugin_scaffold(
        plugin_name="ChaosInjection",
        plugin_id="chaos_injection_plugin",
        author="SRE Squad",
        capabilities=["latency_spike", "process_crash"]
    )
    assert "plugin.py" in scaffold
    assert "metadata.yaml" in scaffold
    assert "ChaosInjectionPlugin" in scaffold["plugin.py"]

    # 2. Docs Generation
    ocr_p = OCRVerificationPlugin()
    doc = plugin_doc_generator.generate_markdown(ocr_p)
    assert "# OCR Invariant & Fidelity Verification Plugin" in doc
    assert "`character_error_rate`" in doc
    assert "`READ_DATASET`" in doc


def test_core_reference_plugins_end_to_end():
    # 1. AI Extraction
    res_ai = extension_framework_runtime.execute_verification_plugin(
        plugin_id="ai_extraction_eval_plugin",
        verification_id="ver_run_ai_101"
    )
    assert res_ai.is_success is True
    assert any(m["metric"] == "extraction_precision" for m in res_ai.metrics)

    # 2. RAG Evaluation
    res_rag = extension_framework_runtime.execute_verification_plugin(
        plugin_id="rag_evaluation_plugin",
        verification_id="ver_run_rag_202"
    )
    assert res_rag.is_success is True
    assert any(m["metric"] == "faithfulness" for m in res_rag.metrics)

    # 3. Prompt Injection Security
    res_sec = extension_framework_runtime.execute_verification_plugin(
        plugin_id="prompt_injection_security_plugin",
        verification_id="ver_run_sec_303"
    )
    assert res_sec.is_success is True
    assert any(m["metric"] == "adversarial_robustness" for m in res_sec.metrics)
