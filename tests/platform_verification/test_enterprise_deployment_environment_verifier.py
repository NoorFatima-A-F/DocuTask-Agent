"""
Comprehensive Test Suite for Part 3D: Enterprise Deployment & Environment Verification Framework.
"""
import pytest
from app.platform_verification.deployment_verification.runtime.deployment_verification_runtime import DeploymentVerificationRuntime
from app.platform_verification.deployment_verification.domain.models import (
    DeploymentCertificationTier,
)


@pytest.fixture
def deploy_runtime():
    return DeploymentVerificationRuntime()


def test_build_pipeline_and_lockfile_validator(deploy_runtime):
    """Verifies build reproducibility and detects unpinned/floating dependencies."""
    clean_meta = {
        "commit_sha": "git-1",
        "image_digest_1": "sha256:aaa",
        "image_digest_2": "sha256:aaa",
        "dependencies": [{"name": "fastapi", "version_spec": "=="}],
    }
    b_rep, l_rep = deploy_runtime.build_validator.validate_build_pipeline(clean_meta)
    assert b_rep.status == "PASS"
    assert b_rep.is_reproducible
    assert l_rep.status == "PASS"
    assert l_rep.is_strictly_pinned

    floating_meta = {
        "commit_sha": "git-2",
        "image_digest_1": "sha256:aaa",
        "image_digest_2": "sha256:bbb",
        "dependencies": [{"name": "fastapi", "version_spec": ">="}],
    }
    bad_b, bad_l = deploy_runtime.build_validator.validate_build_pipeline(floating_meta)
    assert bad_b.status == "FAIL"
    assert bad_l.status == "FAIL"
    assert len(bad_l.unpinned_dependencies) == 1


def test_environment_parity_and_drift_analyzer(deploy_runtime):
    """Verifies environment parity between staging and production and detects missing required variables."""
    good_envs = {
        "STAGING": {"DATABASE_URL": "pg", "REDIS_URL": "rd", "STORAGE_BUCKET": "s3", "ENVIRONMENT": "stg", "SECRET_KEY": "k"},
        "PRODUCTION": {"DATABASE_URL": "pg", "REDIS_URL": "rd", "STORAGE_BUCKET": "s3", "ENVIRONMENT": "prd", "SECRET_KEY": "k"},
    }
    drift_rep = deploy_runtime.parity_validator.validate_parity(good_envs)
    assert drift_rep.status == "PASS"
    assert drift_rep.parity_score == 100.0

    bad_envs = {
        "STAGING": {"DATABASE_URL": "pg", "EXTRA_KEY": "foo"},
        "PRODUCTION": {"DATABASE_URL": "pg"},
    }
    bad_drift = deploy_runtime.parity_validator.validate_parity(bad_envs)
    assert bad_drift.status == "FAIL"
    assert len(bad_drift.missing_variables) > 0
    assert len(bad_drift.drift_items) > 0


def test_iac_manifest_and_idempotency_validator(deploy_runtime):
    """Validates declarative IaC manifests and recreation idempotency."""
    good_iac = [{"framework": "compose", "has_networking": True, "has_healthcheck": True, "idempotent_recreation": True}]
    iac_rep = deploy_runtime.iac_validator.validate_iac(good_iac)
    assert iac_rep.status == "PASS"
    assert iac_rep.is_valid

    bad_iac = [{"framework": "compose", "has_networking": False, "has_healthcheck": False, "idempotent_recreation": False}]
    bad_rep = deploy_runtime.iac_validator.validate_iac(bad_iac)
    assert bad_rep.status == "FAIL"
    assert len(bad_rep.validation_issues) == 2


def test_deployment_automation_auditor(deploy_runtime):
    """Verifies 100% automated CI/CD steps and rejects manual operations."""
    auto_steps = [{"name": "build", "is_manual": False}, {"name": "deploy", "is_manual": False}]
    auto_rep = deploy_runtime.automation_validator.validate_automation(auto_steps)
    assert auto_rep.status == "PASS"
    assert auto_rep.automation_percentage == 100.0

    manual_steps = [{"name": "ssh_login", "action": "manual_ssh", "is_manual": True}]
    bad_auto = deploy_runtime.automation_validator.validate_automation(manual_steps)
    assert bad_auto.status == "FAIL"
    assert len(bad_auto.manual_steps_detected) == 1


def test_rollout_rollback_and_zero_downtime_simulator(deploy_runtime):
    """Tests rolling deployment, automated rollback on healthcheck failure, and zero-downtime SLA."""
    rollout_cfg = {
        "strategy": "ROLLING",
        "zero_dropped_requests": True,
        "canary_traffic_split_verified": True,
        "injected_failure": "HEALTH_CHECK_FAILURE",
        "rollback_recovered": True,
        "data_loss_detected": False,
        "total_traffic_requests": 1000,
        "failed_traffic_requests": 0,
    }
    rel, roll, zero = deploy_runtime.rollout_tester.test_rollout_and_rollback(rollout_cfg)
    assert rel.status == "PASS"
    assert roll.status == "PASS"
    assert roll.rollback_successful
    assert zero.status == "PASS"
    assert zero.availability_pct == 100.0


def test_secret_configuration_auditor(deploy_runtime):
    """Verifies secret scanning across codebase and build artifacts."""
    clean_targets = ["DATABASE_URL=os.environ['DATABASE_URL']"]
    clean_sec = deploy_runtime.secret_auditor.audit_secrets(clean_targets)
    assert clean_sec.status == "PASS"

    dirty_targets = ["password = 'supersecretproductionpassword123'"]
    dirty_sec = deploy_runtime.secret_auditor.audit_secrets(dirty_targets)
    assert dirty_sec.status == "FAIL"
    assert len(dirty_sec.secrets_in_codebase) == 1


def test_end_to_end_deployment_verification_and_api(deploy_runtime):
    """Tests end-to-end full execution, evidence sealing, and in-process REST API."""
    package = deploy_runtime.run_full_verification(commit_sha="git-commit-3d-88")
    assert package.scorecard.composite_score >= 90.0
    assert package.scorecard.tier in [DeploymentCertificationTier.ENTERPRISE_DEPLOYMENT_READY, DeploymentCertificationTier.PRODUCTION_READY]
    assert package.package_sha256 != ""

    api = deploy_runtime.api
    scan_res = api.post_scan({"commit_sha": "git-commit-3d-88"})
    assert scan_res["status"] == "COMPLETED"
    assert "package_id" in scan_res

    report_res = api.get_report(scan_res["package_id"])
    assert report_res is not None
    assert "scorecard" in report_res
    assert report_res["commit_sha"] == "git-commit-3d-88"

    metrics_res = api.get_metrics()
    assert "supported_stages" in metrics_res
