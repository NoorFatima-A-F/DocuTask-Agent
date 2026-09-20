"""
Comprehensive Unit & Integration Test Suite for Part 1.1E:
Enterprise Verification Configuration, Versioning & Dependency Management Architecture.
"""
import pytest
from datetime import datetime, timezone
from app.platform_verification.config_versioning.domain.models import (
    SemanticVersion,
    DependencyItem,
    DependencyCategory,
    EnvironmentTier,
    AIModelMetadata,
    PromptTemplateVersion,
    RAGRetrievalConfigVersion,
    AgentConfigVersion,
    EnvironmentFingerprint,
    ConfigurationSnapshot,
    ConfigurationDiff,
    DriftReport,
    ChangeRequest,
    ChangeApprovalStatus,
    RollbackRecord,
    SBOMManifest,
)
from app.platform_verification.config_versioning.core.registry import configuration_registry
from app.platform_verification.config_versioning.core.resolver import configuration_resolver
from app.platform_verification.config_versioning.core.validator import configuration_validator
from app.platform_verification.config_versioning.core.snapshot_manager import snapshot_manager
from app.platform_verification.config_versioning.core.diff_engine import configuration_diff_engine
from app.platform_verification.config_versioning.core.dependency_registry import dependency_registry
from app.platform_verification.config_versioning.core.sbom_generator import sbom_generator
from app.platform_verification.config_versioning.core.ai_artifacts import ai_artifact_manager
from app.platform_verification.config_versioning.core.fingerprint import environment_fingerprinter
from app.platform_verification.config_versioning.core.drift_detector import drift_detector
from app.platform_verification.config_versioning.core.change_tracker import change_tracker
from app.platform_verification.config_versioning.runtime.config_versioning_runtime import config_versioning_runtime


def test_semantic_version_comparison_and_bump():
    v1 = SemanticVersion(major=1, minor=2, patch=3)
    assert str(v1) == "1.2.3"

    v1_patch = v1.bump_patch()
    assert str(v1_patch) == "1.2.4"

    v1_minor = v1.bump_minor()
    assert str(v1_minor) == "1.3.0"

    v1_major = v1.bump_major()
    assert str(v1_major) == "2.0.0"

    parsed = SemanticVersion.parse("v2.4.1-rc.1+build.99")
    assert parsed.major == 2
    assert parsed.minor == 4
    assert parsed.patch == 1
    assert parsed.prerelease == "rc.1"
    assert parsed.build == "build.99"


def test_7_tier_configuration_resolution_precedence():
    # 1. Base resolution for integration environment
    configuration_resolver.set_module_config("ocr_verification", {"confidence_threshold": 0.95})
    resolved = configuration_resolver.resolve(
        environment=EnvironmentTier.INTEGRATION,
        module_name="ocr_verification"
    )
    assert resolved["platform_name"] == "DocuTask Enterprise Agent Platform"
    assert resolved["timeout_seconds"] == 180  # from INTEGRATION env
    assert resolved["confidence_threshold"] == 0.95  # from module config

    # 2. Experiment override taking highest precedence
    override_config = {
        "timeout_seconds": 600,
        "confidence_threshold": 0.99
    }
    resolved_with_overrides = configuration_resolver.resolve(
        environment=EnvironmentTier.INTEGRATION,
        module_name="ocr_verification",
        experiment_override=override_config
    )
    assert resolved_with_overrides["timeout_seconds"] == 600
    assert resolved_with_overrides["confidence_threshold"] == 0.99


def test_configuration_validator():
    # Valid config
    valid_cfg = {
        "timeout_seconds": 120,
        "ai": {
            "temperature": 0.2,
            "max_tokens": 4096
        }
    }
    is_valid, errors = configuration_validator.validate_resolved_config(valid_cfg)
    assert is_valid is True
    assert len(errors) == 0

    # Invalid config (missing timeout, invalid temperature)
    invalid_cfg = {
        "timeout_seconds": -5,
        "ai": {
            "temperature": 3.5,  # Exceeds 2.0
            "max_tokens": -50
        }
    }
    is_valid, errors = configuration_validator.validate_resolved_config(invalid_cfg)
    assert is_valid is False
    assert any("must be greater than 0" in e for e in errors)
    assert any("temperature" in e for e in errors)
    assert any("max_tokens" in e for e in errors)


def test_immutable_snapshot_and_canonical_fingerprinting():
    resolved = configuration_resolver.resolve(environment=EnvironmentTier.STAGING)
    fp = environment_fingerprinter.capture_fingerprint(tier=EnvironmentTier.STAGING)

    snapshot = snapshot_manager.create_snapshot(
        resolved_config=resolved,
        environment=EnvironmentTier.STAGING,
        environment_fingerprint=fp,
        creator="Senior Verification Architect"
    )

    assert snapshot.snapshot_id.startswith("cfg_snap_")
    assert len(snapshot.configuration_hash) == 64
    assert snapshot.environment == EnvironmentTier.STAGING
    assert snapshot.creator == "Senior Verification Architect"
    assert snapshot.is_frozen is True

    # Verify retrieval
    retrieved = configuration_registry.get_snapshot(snapshot.snapshot_id)
    assert retrieved is not None
    assert retrieved.configuration_hash == snapshot.configuration_hash


def test_configuration_diff_engine():
    resolved_a = configuration_resolver.resolve(environment=EnvironmentTier.INTEGRATION)
    snap_a = snapshot_manager.create_snapshot(
        resolved_config=resolved_a,
        environment=EnvironmentTier.INTEGRATION,
        creator="Engineer A"
    )

    # Mutate configuration for snapshot B
    resolved_b = dict(resolved_a)
    resolved_b["timeout_seconds"] = 900
    resolved_b["ai"] = {
        "default_model": "gemini-1.5-pro",
        "temperature": 0.7,
        "max_tokens": 8192
    }
    snap_b = snapshot_manager.create_snapshot(
        resolved_config=resolved_b,
        environment=EnvironmentTier.INTEGRATION,
        creator="Engineer B"
    )

    diff = configuration_diff_engine.compare(snap_a.snapshot_id, snap_b.snapshot_id)
    assert diff.source_snapshot_id == snap_a.snapshot_id
    assert diff.target_snapshot_id == snap_b.snapshot_id
    assert diff.has_changes is True
    assert diff.ai_model_drift is True
    assert "timeout_seconds" in diff.modified_keys
    assert "AI Model configuration drift detected" in diff.human_readable_summary


def test_dependency_registry_and_inventory():
    deps = dependency_registry.get_all_dependencies()
    assert len(deps) >= 8

    categories = {d.category for d in deps}
    assert DependencyCategory.PYTHON_PACKAGE in categories
    assert DependencyCategory.AI_MODEL in categories
    assert DependencyCategory.DATABASE in categories

    fastapi_dep = dependency_registry.get_dependency("fastapi")
    assert fastapi_dep is not None
    assert fastapi_dep.version == "0.115.0"
    assert fastapi_dep.license == "MIT"

    # Add custom dynamic dependency
    new_dep = DependencyItem(
        name="custom_eval_tool",
        category=DependencyCategory.CLOUD_SERVICE,
        version="2.4.1",
        license="Apache-2.0"
    )
    dependency_registry.register_dependency(new_dep)
    assert dependency_registry.get_dependency("custom_eval_tool") is not None


def test_sbom_generation_cyclonedx_and_spdx():
    # 1. CycloneDX 1.5 Manifest
    cyclonedx_manifest = sbom_generator.generate_cyclonedx_sbom()
    assert cyclonedx_manifest.format == "CycloneDX_1.5"
    assert cyclonedx_manifest.spec_version == "1.5"
    assert cyclonedx_manifest.components_count >= 8
    assert len(cyclonedx_manifest.components) >= 8

    cyclonedx_json = sbom_generator.export_cyclonedx_json()
    assert cyclonedx_json["bomFormat"] == "CycloneDX"
    assert cyclonedx_json["metadata"]["component"]["name"] == "DocuTask Agent Enterprise Platform"
    assert any(c["name"] == "fastapi" for c in cyclonedx_json["components"])

    # 2. SPDX 2.3 Manifest
    spdx_manifest = sbom_generator.generate_spdx_sbom()
    assert spdx_manifest.format == "SPDX_2.3"
    assert spdx_manifest.spec_version == "2.3"
    assert spdx_manifest.components_count >= 8


def test_ai_artifact_version_manager():
    # 1. Prompt Versioning
    prompt_v1 = PromptTemplateVersion(
        name="ocr_extraction_system",
        semantic_version="1.0.0",
        raw_prompt="Extract key value pairs: {text}",
        author="AI Team"
    )
    registered_prompt = ai_artifact_manager.register_prompt(prompt_v1)
    assert registered_prompt.template_id.startswith("pmt_")
    assert len(registered_prompt.prompt_hash) == 64

    retrieved = ai_artifact_manager.get_prompt("ocr_extraction_system", "1.0.0")
    assert retrieved is not None
    assert retrieved.name == "ocr_extraction_system"

    # 2. RAG Config Versioning
    rag_cfg = RAGRetrievalConfigVersion(
        version="1.1.0",
        embedding_model="text-embedding-004",
        chunk_size=1024,
        chunk_overlap=128,
        top_k=10
    )
    reg_rag = ai_artifact_manager.register_rag_config(rag_cfg)
    assert reg_rag.config_id.startswith("rag_cfg_")

    # 3. Agent Config Versioning
    agent_cfg = AgentConfigVersion(
        version="2.0.0",
        model=AIModelMetadata(model_name="gemini-2.5-flash"),
        allowed_tools=["ocr_reader", "table_parser"]
    )
    reg_agent = ai_artifact_manager.register_agent_config(agent_cfg)
    assert reg_agent.agent_id.startswith("agt_cfg_")


def test_deterministic_environment_fingerprinter():
    fp = environment_fingerprinter.capture_fingerprint(tier=EnvironmentTier.PRODUCTION)
    assert fp.tier == EnvironmentTier.PRODUCTION
    assert fp.python_version is not None
    assert fp.cpu_count > 0
    assert fp.os_kernel is not None
    assert fp.fingerprint_id.startswith("env_fp_")


def test_drift_detector():
    # Baseline snapshot
    baseline_cfg = configuration_resolver.resolve(environment=EnvironmentTier.INTEGRATION)
    baseline_snap = snapshot_manager.create_snapshot(
        resolved_config=baseline_cfg,
        environment=EnvironmentTier.INTEGRATION,
        creator="Baseline Architect"
    )

    # 1. No drift
    report_nodrift = drift_detector.detect_drift(baseline_snap, baseline_cfg)
    assert report_nodrift.is_drifted is False
    assert len(report_nodrift.unauthorized_mutations) == 0

    # 2. Drift detected
    drifted_cfg = dict(baseline_cfg)
    drifted_cfg["timeout_seconds"] = 999
    drifted_cfg["unauthorized_debug_key"] = True

    report_drifted = drift_detector.detect_drift(baseline_snap, drifted_cfg)
    assert report_drifted.is_drifted is True
    assert len(report_drifted.unauthorized_mutations) > 0
    assert any("unauthorized_debug_key" in item for item in report_drifted.unauthorized_mutations)


def test_change_tracker_and_automated_rollback():
    # 1. Create original snapshot (A) and new snapshot (B)
    resolved_a = configuration_resolver.resolve(environment=EnvironmentTier.PRODUCTION)
    snap_a = snapshot_manager.create_snapshot(resolved_a, EnvironmentTier.PRODUCTION, creator="Engineer 1")

    resolved_b = dict(resolved_a)
    resolved_b["timeout_seconds"] = 1200
    snap_b = snapshot_manager.create_snapshot(resolved_b, EnvironmentTier.PRODUCTION, creator="Engineer 2")

    # 2. Submit Change Request
    change_req = change_tracker.submit_change(
        title="Scale Execution Timeout for Q3",
        author="DevOps Lead",
        reason="Extended timeout for intensive verification batches",
        proposed_changes={"timeout_seconds": 1200},
        rollback_plan=f"Revert to baseline snapshot {snap_a.snapshot_id}"
    )
    assert change_req.status == ChangeApprovalStatus.SUBMITTED

    # 3. Approve Change Request
    approved = change_tracker.approve_change(change_req.change_id, approver="VP of Infrastructure")
    assert approved.status == ChangeApprovalStatus.APPROVED
    assert approved.approved_by == "VP of Infrastructure"

    # 4. Execute Automated Rollback
    rollback_record = change_tracker.execute_rollback(
        change_id=change_req.change_id,
        to_snapshot_id=snap_a.snapshot_id,
        reason="Elevated downstream latency detected",
        executed_by="SRE OnCall"
    )
    assert rollback_record.rollback_id.startswith("rbk_")
    assert rollback_record.is_successful is True
    assert rollback_record.to_snapshot_id == snap_a.snapshot_id
    assert rollback_record.change_id == change_req.change_id


def test_config_versioning_runtime_facade():
    snapshot = config_versioning_runtime.resolve_and_snapshot(
        environment=EnvironmentTier.INTEGRATION,
        module_name="rag_verification",
        overrides={"timeout_seconds": 450}
    )
    assert snapshot.environment == EnvironmentTier.INTEGRATION
    assert snapshot.resolved_configuration["timeout_seconds"] == 450
