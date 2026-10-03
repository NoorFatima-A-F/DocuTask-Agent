"""Tests for Environment Management, Policy Enforcement, and Multi-Stage Promotion."""

from app.infrastructure.deployment.environments import (
    EnvironmentManager,
    EnvironmentPromotionManager,
)
from app.infrastructure.deployment.artifacts import ArtifactRegistry, ArtifactType


def test_environment_promotion_pipeline() -> None:
    env_mgr = EnvironmentManager()
    art_registry = ArtifactRegistry()
    promo_mgr = EnvironmentPromotionManager(env_manager=env_mgr, artifact_registry=art_registry)

    art = art_registry.register_artifact(
        name="agent-kernel",
        version="1.5.0",
        artifact_type=ArtifactType.CONTAINER_IMAGE,
        commit_sha="commit-99",
        auto_sign=True,
    )

    # 1. Dev -> Staging promotion (requires 1 approval)
    chk_staging = promo_mgr.evaluate_promotion(
        from_env="dev",
        to_env="staging",
        release_id="rel-150",
        artifact=art,
        tests_passed=True,
        approvers=["lead-dev"],
    )
    assert chk_staging.is_eligible is True
    assert chk_staging.promoted_at is not None

    # 2. Staging -> Prod promotion (requires 2 approvals, fails with only 1)
    chk_prod_fail = promo_mgr.evaluate_promotion(
        from_env="staging",
        to_env="prod",
        release_id="rel-150",
        artifact=art,
        tests_passed=True,
        approvers=["lead-dev"],  # missing 2nd approval
    )
    assert chk_prod_fail.is_eligible is False

    # Staging -> Prod with 2 approvals succeeds
    chk_prod_success = promo_mgr.evaluate_promotion(
        from_env="staging",
        to_env="prod",
        release_id="rel-150",
        artifact=art,
        tests_passed=True,
        approvers=["lead-dev", "security-officer"],
    )
    assert chk_prod_success.is_eligible is True
    assert chk_prod_success.promoted_at is not None
