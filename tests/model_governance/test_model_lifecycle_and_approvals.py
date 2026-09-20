"""Tests for Model Lifecycle FSM and Approval Workflows (Phase 8C)."""

import pytest
from app.model_governance.registry.models import (
    ApprovalStatus,
    Model,
    ModelCategory,
    ModelLifecycleState,
    ModelProvider,
)
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.lifecycle.manager import ModelLifecycleManager
from app.model_governance.approval.workflow import ModelApprovalWorkflowEngine
from app.model_governance.approval.approvals import StageStatus


def test_model_lifecycle_valid_transitions():
    repo = ModelRegistryRepository()
    manager = ModelLifecycleManager(repo)

    model = Model(
        model_id="gemini-1-5-pro",
        model_name="Gemini 1.5 Pro",
        organization_id="org_test",
        family_id="gemini-1-5",
        version="002",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.GOOGLE,
    )
    repo.save_model(model)

    # REGISTERED -> EVALUATING
    res1 = manager.transition(
        model_id="gemini-1-5-pro",
        target_state=ModelLifecycleState.EVALUATING,
        actor="engineer@test.com",
        reason="Initiating benchmark evaluation",
        organization_id="org_test",
    )
    assert res1.to_state == ModelLifecycleState.EVALUATING

    # EVALUATING -> REVIEW
    res2 = manager.transition(
        model_id="gemini-1-5-pro",
        target_state=ModelLifecycleState.REVIEW,
        actor="mlops@test.com",
        reason="Evaluation complete, submitting for review",
        organization_id="org_test",
    )
    assert res2.to_state == ModelLifecycleState.REVIEW


def test_model_lifecycle_invalid_transition():
    repo = ModelRegistryRepository()
    manager = ModelLifecycleManager(repo)

    model = Model(
        model_id="mistral-large",
        model_name="Mistral Large",
        organization_id="org_test",
        family_id="mistral",
        version="2407",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.MISTRAL,
        lifecycle_state=ModelLifecycleState.REGISTERED,
    )
    repo.save_model(model)

    # Cannot jump directly from REGISTERED to ACTIVE
    with pytest.raises(ValueError, match="Invalid lifecycle state transition"):
        manager.transition(
            model_id="mistral-large",
            target_state=ModelLifecycleState.ACTIVE,
            actor="engineer@test.com",
            reason="Illegal shortcut",
            organization_id="org_test",
        )


def test_five_stage_approval_workflow_completion():
    repo = ModelRegistryRepository()
    lifecycle_manager = ModelLifecycleManager(repo)
    approval_engine = ModelApprovalWorkflowEngine(repo, lifecycle_manager)

    model = Model(
        model_id="deepseek-r1-gov",
        model_name="DeepSeek R1",
        organization_id="org_test",
        family_id="deepseek-r1",
        version="v1",
        category=ModelCategory.REASONING_LLM,
        provider=ModelProvider.SELF_HOSTED,
        lifecycle_state=ModelLifecycleState.REVIEW,
    )
    repo.save_model(model)

    # Initiate workflow
    wf = approval_engine.initiate_workflow("deepseek-r1-gov", "org_test")
    assert len(wf.stages) == 5

    # 1. Technical
    wf = approval_engine.review_stage(
        model_id="deepseek-r1-gov",
        stage_name="TECHNICAL_VALIDATION",
        reviewer="lead_dev@test.com",
        decision=StageStatus.APPROVED,
        organization_id="org_test",
    )

    # 2. Security
    wf = approval_engine.review_stage(
        model_id="deepseek-r1-gov",
        stage_name="SECURITY_REVIEW",
        reviewer="secops@test.com",
        decision=StageStatus.APPROVED,
        organization_id="org_test",
    )

    # 3. Compliance
    wf = approval_engine.review_stage(
        model_id="deepseek-r1-gov",
        stage_name="COMPLIANCE_AUDIT",
        reviewer="legal@test.com",
        decision=StageStatus.APPROVED,
        organization_id="org_test",
    )

    # 4. Business
    wf = approval_engine.review_stage(
        model_id="deepseek-r1-gov",
        stage_name="BUSINESS_APPROVAL",
        reviewer="product@test.com",
        decision=StageStatus.APPROVED,
        organization_id="org_test",
    )

    # 5. Final Gate
    wf = approval_engine.review_stage(
        model_id="deepseek-r1-gov",
        stage_name="FINAL_GATE",
        reviewer="cto@test.com",
        decision=StageStatus.APPROVED,
        organization_id="org_test",
    )

    assert wf.status == ApprovalStatus.APPROVED

    # Check that model transitioned to APPROVED state
    updated_model = repo.get_model("deepseek-r1-gov", "org_test")
    assert updated_model.approval_status == ApprovalStatus.APPROVED
    assert updated_model.lifecycle_state == ModelLifecycleState.APPROVED
