"""
Advanced Verification Tests for Part 1.1F:
Multi-Category Plugins (Execution, Dataset, Metric, AI, Storage, Notification),
Marketplace Certification, Developer SDK, and Quarantine Governance.
"""
import pytest
from app.platform_verification.extension_framework.domain.models import (
    PluginCategory, SecurityClassification, PluginPermission, PluginSecurityContext
)
from app.platform_verification.extension_framework.core.marketplace import plugin_marketplace
from app.platform_verification.extension_framework.core.registry import plugin_registry
from app.platform_verification.extension_framework.tooling.sdk import plugin_sdk
from app.platform_verification.extension_framework.runtime.extension_framework_runtime import extension_framework_runtime


def test_multi_category_plugin_registration_and_execution():
    # 1. Execution Backend Plugin
    res_k8s = extension_framework_runtime.execute_verification_plugin(
        plugin_id="k8s_executor_plugin",
        verification_id="ver_k8s_001"
    )
    assert res_k8s.is_success is True
    assert res_k8s.raw_evidence["status"] == "COMPLETED"

    # 2. Dataset Provider Plugin
    res_ds = extension_framework_runtime.execute_verification_plugin(
        plugin_id="synthetic_dataset_plugin",
        verification_id="ver_ds_002"
    )
    assert res_ds.is_success is True
    assert res_ds.raw_evidence["sample_count"] == 10

    # 3. Metric Evaluator Plugin
    res_metric = extension_framework_runtime.execute_verification_plugin(
        plugin_id="composite_metric_plugin",
        verification_id="ver_met_003"
    )
    assert res_metric.is_success is True
    assert any(m["metric"] == "composite_accuracy" for m in res_metric.metrics)

    # 4. AI Provider Plugin
    res_ai = extension_framework_runtime.execute_verification_plugin(
        plugin_id="gemini_ai_provider_plugin",
        verification_id="ver_ai_004"
    )
    assert res_ai.is_success is True
    assert "Gemini Evaluation Response" in res_ai.raw_evidence["response_text"]

    # 5. Storage Provider Plugin
    res_store = extension_framework_runtime.execute_verification_plugin(
        plugin_id="local_cas_storage_plugin",
        verification_id="ver_cas_005"
    )
    assert res_store.is_success is True
    assert res_store.raw_evidence["storage_uri"].startswith("cas://")

    # 6. Notification Plugin
    res_notif = extension_framework_runtime.execute_verification_plugin(
        plugin_id="webhook_notification_plugin",
        verification_id="ver_notif_006"
    )
    assert res_notif.is_success is True


def test_marketplace_publishing_and_signature_verification():
    entry = plugin_marketplace.get_entry("gemini_ai_provider_plugin")
    assert entry is not None
    assert entry.category == PluginCategory.AI_PROVIDER
    assert entry.certification_level == SecurityClassification.ENTERPRISE_CERTIFIED
    assert len(entry.digital_signature) == 64

    # Verify digital signature
    assert plugin_marketplace.verify_signature("gemini_ai_provider_plugin") is True


def test_plugin_developer_sdk_scaffolding_and_validation():
    # Scaffold new compliance plugin
    files = plugin_sdk.create_plugin_project(
        plugin_name="HIPAAComplianceValidator",
        plugin_id="hipaa_compliance_plugin",
        category=PluginCategory.COMPLIANCE,
        author="SecOps Squad",
        capabilities=["phi_redaction_audit", "access_log_integrity"]
    )
    assert "plugin.py" in files
    assert "metadata.yaml" in files
    assert "HIPAAComplianceValidatorPlugin" in files["plugin.py"]


def test_category_based_discovery():
    exec_plugins = extension_framework_runtime.list_plugins_by_category(PluginCategory.EXECUTION)
    assert len(exec_plugins) >= 1
    assert any(p.plugin_id == "k8s_executor_plugin" for p in exec_plugins)

    storage_plugins = extension_framework_runtime.list_plugins_by_category(PluginCategory.STORAGE)
    assert len(storage_plugins) >= 1
    assert any(p.plugin_id == "local_cas_storage_plugin" for p in storage_plugins)
