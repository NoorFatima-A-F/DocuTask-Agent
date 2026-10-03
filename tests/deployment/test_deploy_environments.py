"""Unit tests for Environment Promotion and Validation."""
import pytest
from app.deployment.core.controller import DeploymentController
from app.deployment.core.exceptions import PromotionBlockedException
from app.deployment.environments.policies import PromotionPolicy
from app.deployment.environments.promotion import PromotionManager, PromotionStatus
from app.deployment.environments.validation import EnvironmentValidator


def test_environment_validator():
    validator = EnvironmentValidator()
    report = validator.validate_environment("prod")
    assert report.overall_passed is True
    assert len(report.checks) >= 4


def test_promotion_policy_violations():
    policy = PromotionPolicy()

    # Skip tiers (dev -> prod forbidden)
    with pytest.raises(PromotionBlockedException, match="forbidden"):
        policy.validate_promotion(
            source_env="dev",
            target_env="prod",
            soak_time_seconds=60,
            test_pass_rate=1.0,
            approvals=["release_manager", "security_lead"],
        )

    # Missing approval
    with pytest.raises(PromotionBlockedException, match="Missing required approver"):
        policy.validate_promotion(
            source_env="staging",
            target_env="prod",
            soak_time_seconds=60,
            test_pass_rate=1.0,
            approvals=["release_manager"],  # missing security_lead
        )


def test_promotion_manager_flow():
    controller = DeploymentController()
    rel = controller.create_release("1.5.0", "Release 1.5", "sha15", ["art-15"])
    rel.publish()

    prom_mgr = PromotionManager()
    record = prom_mgr.request_promotion(
        release_id=rel.release_id,
        target_env="staging",
        source_env="testing",
    )
    assert record.status == PromotionStatus.PENDING_APPROVAL

    # Approve
    prom_mgr.approve_promotion(record.promotion_id, role="qa_lead", approver_identity="qa_lead_user")
    
    dep = prom_mgr.execute_promotion(
        promotion_id=record.promotion_id,
        controller=controller,
        soak_time_seconds=10,
        test_pass_rate=1.0,
    )
    assert dep.status.value == "ACTIVE"
    assert record.status == PromotionStatus.EXECUTED
