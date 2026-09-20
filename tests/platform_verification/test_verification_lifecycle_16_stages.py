"""
Unit and Integration Tests for Canonical 16-Stage Enterprise Verification Lifecycle.
"""
import pytest
from app.platform_verification.lifecycle.states import LifecycleState, LifecycleStateMachine
from app.platform_verification.lifecycle.context import VerificationExecutionContext
from app.platform_verification.lifecycle.pipeline import verification_pipeline
from app.platform_verification.lifecycle.orchestrator import canonical_lifecycle_orchestrator
from app.platform_verification.lifecycle.hooks import lifecycle_hooks

def test_formal_state_machine_valid_and_invalid_transitions():
    # Valid transition
    rec = LifecycleStateMachine.validate_transition(LifecycleState.CREATED, LifecycleState.REGISTERED)
    assert rec.is_valid is True
    assert rec.from_state == LifecycleState.CREATED
    assert rec.to_state == LifecycleState.REGISTERED

    # Invalid illegal transition (e.g. CREATED directly to CERTIFIED)
    with pytest.raises(ValueError, match="Illegal lifecycle state transition"):
        LifecycleStateMachine.validate_transition(LifecycleState.CREATED, LifecycleState.CERTIFIED)


def test_complete_15_stage_execution_pipeline():
    context = VerificationExecutionContext(
        definition_id="def_ocr_enterprise_suite",
        tenant_id="tenant-gold-master",
        initiator="Principal QA Architect"
    )

    # Execute full pipeline (Stages 1 through 15)
    final_context = verification_pipeline.execute_lifecycle(context)

    assert final_context.current_state == LifecycleState.ARCHIVED
    assert len(final_context.stage_results) == 15
    assert all(s.status == "PASSED" for s in final_context.stage_results)
    assert len(final_context.state_history) == 15
    assert len(final_context.config_fingerprint) == 64
    assert len(final_context.archival_bundle_hash or "") == 64
    assert final_context.certification_decision.get("level") == "ENTERPRISE_CERTIFIED"
    assert final_context.certification_decision.get("is_valid") is True


def test_stage_16_reproduction():
    context = VerificationExecutionContext(
        definition_id="def_rag_evaluation_suite",
        tenant_id="tenant-repro-test",
        initiator="Compliance Auditor"
    )
    # Execute through archival
    archived_context = verification_pipeline.execute_lifecycle(context)
    assert archived_context.current_state == LifecycleState.ARCHIVED

    # Reproduce from archived bundle (Stage 16)
    reproduced_context = verification_pipeline.reproduce_lifecycle(archived_context)
    assert reproduced_context.current_state == LifecycleState.REPRODUCED
    assert len(reproduced_context.stage_results) == 16
    assert reproduced_context.stage_results[-1].stage_name == "Reproduction"
    assert reproduced_context.stage_results[-1].produced_artifacts.get("reproduction_exact_match") is True


def test_lifecycle_hooks_interception():
    triggered_hooks = []

    def custom_pre_plan_hook(ctx):
        triggered_hooks.append("before_planning")

    def custom_post_cert_hook(ctx):
        triggered_hooks.append("after_certification")

    lifecycle_hooks.register_hook("before_planning", custom_pre_plan_hook)
    lifecycle_hooks.register_hook("after_certification", custom_post_cert_hook)

    context = VerificationExecutionContext(
        definition_id="def_hook_test_suite",
        tenant_id="tenant-hook"
    )
    verification_pipeline.execute_lifecycle(context)

    assert "before_planning" in triggered_hooks
    assert "after_certification" in triggered_hooks


def test_canonical_orchestrator_facade():
    run_ctx = canonical_lifecycle_orchestrator.start_verification(
        definition_id="def_e2e_canonical_test",
        tenant_id="tenant-enterprise"
    )
    assert run_ctx.current_state == LifecycleState.ARCHIVED
    assert canonical_lifecycle_orchestrator.get_execution(run_ctx.execution_id) is not None

    # Test reproduction via orchestrator
    repro_ctx = canonical_lifecycle_orchestrator.reproduce_verification(run_ctx.execution_id)
    assert repro_ctx is not None
    assert repro_ctx.current_state == LifecycleState.REPRODUCED
