"""
Advanced Verification Tests for Part 1.1E:
Configuration Domains, Lifecycle, Reproducibility Engine, Database Migrations,
Feature Flags, and Secret Governance.
"""
from app.platform_verification.config_versioning.domain.models import (
    SemanticVersion, EnvironmentTier, ConfigDomain, PromptTemplateVersion
)
from app.platform_verification.config_versioning.domain.schemas import schema_validator
from app.platform_verification.config_versioning.domain.lifecycle import (
    ConfigurationLifecycleRecord, ConfigurationLifecycleState
)
from app.platform_verification.config_versioning.core.migrations import migration_manager
from app.platform_verification.config_versioning.core.feature_flags import feature_flag_manager
from app.platform_verification.config_versioning.core.secrets import secret_manager_service
from app.platform_verification.config_versioning.core.reproducibility import reproducibility_engine
from app.platform_verification.config_versioning.runtime.config_versioning_runtime import config_versioning_runtime


def test_semantic_version_range_evaluation_and_comparisons():
    v1 = SemanticVersion.parse("1.2.3")
    v2 = SemanticVersion.parse("1.2.4")
    v3 = SemanticVersion.parse("2.0.0")

    assert v1 < v2
    assert v2 < v3
    assert v1 <= v2
    assert v3 > v2

    # Range satisfaction
    assert v1.satisfies(">=1.0.0, <2.0.0")
    assert v1.satisfies("^1.2.0")
    assert v1.satisfies("~1.2.0")
    assert not v3.satisfies("^1.0.0")
    assert v3.is_breaking(v1) is True


def test_configuration_domain_schema_validations():
    # Valid AI config
    ai_cfg = {
        "provider": "gemini",
        "model": "gemini-2.5-flash",
        "temperature": 0.1,
        "top_p": 0.9,
        "max_tokens": 4096,
        "request_timeout_seconds": 30
    }
    is_valid, errors = schema_validator.validate_domain_config(ConfigDomain.AI, ai_cfg)
    assert is_valid is True

    # Invalid AI config (temperature > 2.0)
    bad_ai_cfg = {"temperature": 5.0}
    is_valid, errors = schema_validator.validate_domain_config(ConfigDomain.AI, bad_ai_cfg)
    assert is_valid is False
    assert len(errors) > 0


def test_configuration_lifecycle_state_machine():
    record = ConfigurationLifecycleRecord(config_id="cfg_ocr_prod")
    assert record.current_state == ConfigurationLifecycleState.CREATED

    record.transition_to(ConfigurationLifecycleState.VALIDATED, actor="ValidatorAgent")
    assert record.current_state == ConfigurationLifecycleState.VALIDATED

    record.transition_to(ConfigurationLifecycleState.APPROVED, actor="SecOpsLead")
    record.transition_to(ConfigurationLifecycleState.VERSIONED, actor="ReleaseBot")
    record.transition_to(ConfigurationLifecycleState.ACTIVATED, actor="DeploymentPipeline")
    assert record.current_state == ConfigurationLifecycleState.ACTIVATED
    assert len(record.history) == 4


def test_database_migration_versioning_and_rollback():
    m1 = migration_manager.register_migration(
        migration_id="001_create_evidence_cas_table",
        version="1.0.0",
        author="Principal Data Architect",
        description="Creates CAS table for evidence storage",
        forward_sql="CREATE TABLE evidence_cas (hash TEXT PRIMARY KEY, content BLOB);",
        rollback_sql="DROP TABLE evidence_cas;"
    )
    assert m1.is_applied is False

    # Apply
    applied = migration_manager.apply_migration(m1.migration_id)
    assert applied.is_applied is True
    assert applied.applied_at is not None

    # Rollback
    rolled_back = migration_manager.rollback_migration(m1.migration_id)
    assert rolled_back.is_applied is False


def test_feature_flag_percentage_and_environment_gating():
    feature_flag_manager.define_flag(
        flag_key="experimental_llm_judge",
        name="Experimental LLM Judge Evaluation",
        description="Enables Gemini 2.5 Flash as synthetic judge",
        is_enabled=True,
        rollout_percentage=50,
        enabled_environments=[EnvironmentTier.STAGING, EnvironmentTier.PRODUCTION_SHADOW]
    )
    # Production should be disabled (not in enabled_environments)
    assert feature_flag_manager.is_flag_active("experimental_llm_judge", EnvironmentTier.PRODUCTION) is False

    # Staging should be active
    assert feature_flag_manager.is_flag_active("experimental_llm_judge", EnvironmentTier.STAGING) is True


def test_secret_management_masking_and_rotation():
    # Register secret
    sec = secret_manager_service.register_secret_reference(
        key_name="GEMINI_API_KEY",
        vault_path="secret/data/gemini_key",
        initial_value="TEST_SECRET_VAL_ALPHA_12345"
    )
    assert sec.version == 1

    # Rotation
    rot = secret_manager_service.rotate_secret(
        key_name="GEMINI_API_KEY",
        new_value="TEST_SECRET_VAL_BETA_98765",
        reason="Quarterly key rotation"
    )
    assert rot.new_version == 2
    assert sec.version == 2

    # Leak masking
    dirty_log = "Error connecting with token TEST_SECRET_VAL_ALPHA_12345 to endpoint"
    clean_log = secret_manager_service.mask_secrets(dirty_log)
    assert "[REDACTED_SECRET]" in clean_log
    assert "TEST_SECRET_VAL_ALPHA" not in clean_log


def test_reproducibility_engine_execution_snapshot_and_fidelity():
    snap_cfg = config_versioning_runtime.resolve_and_snapshot(
        environment=EnvironmentTier.STAGING,
        module_name="ocr_verification"
    )
    prompt = PromptTemplateVersion(
        name="ocr_eval_prompt",
        semantic_version="1.0.0",
        raw_prompt="Extract all invoice line items strictly as JSON."
    )

    # Capture execution snapshot A
    exec_a = config_versioning_runtime.create_execution_snapshot(
        verification_id="ver_2026_001",
        code_commit_sha="git_sha_abc123",
        config_snapshot=snap_cfg,
        dataset_id="ds_invoices_v1",
        dataset_version="1.0.0",
        dataset_hash="hash_ds_987",
        model_identifier="gemini-2.5-flash",
        model_version="2026-03-stable",
        prompt_version=prompt
    )
    assert len(exec_a.composite_execution_hash) == 64

    # Capture candidate replay snapshot B (identical)
    exec_b = reproducibility_engine.capture_execution_snapshot(
        verification_id="ver_2026_001_replay",
        code_commit_sha="git_sha_abc123",
        configuration_snapshot_id=snap_cfg.snapshot_id,
        configuration_hash=snap_cfg.configuration_hash,
        dataset_id="ds_invoices_v1",
        dataset_version="1.0.0",
        dataset_hash="hash_ds_987",
        model_identifier="gemini-2.5-flash",
        model_version="2026-03-stable",
        prompt_template_id=prompt.template_id,
        prompt_version=prompt.semantic_version,
        prompt_hash=prompt.prompt_hash,
        dependency_lock_hash=exec_a.dependency_lock_hash,
        sbom_manifest_id=exec_a.sbom_manifest_id,
        environment_tier=EnvironmentTier.STAGING,
        infrastructure_version="k8s-cluster-v2"
    )

    report = reproducibility_engine.verify_reproducibility_fidelity(exec_a, exec_b)
    assert report.is_exact_match is True
    assert report.fidelity_score == 1.0
    assert len(report.discrepancies) == 0
