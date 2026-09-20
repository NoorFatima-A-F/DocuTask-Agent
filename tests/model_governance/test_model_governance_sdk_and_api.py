"""Tests for Model Governance Developer SDK and FastAPI Endpoints (Phase 8C)."""

import pytest
from app.model_governance.sdk.client import ModelGovernanceSDK
from app.model_governance.registry.models import (
    Model,
    ModelCategory,
    ModelLifecycleState,
    ModelProvider,
    RiskLevel,
)
from app.model_governance.api.routes import (
    register_model,
    get_model,
    capture_snapshot,
    verify_snapshot,
)
from app.model_governance.api.schemas import (
    ModelRegisterRequestDTO,
    SnapshotCaptureRequestDTO,
)


def test_model_governance_sdk_end_to_end_flow():
    sdk = ModelGovernanceSDK()

    # 1. Register model
    model = Model(
        model_id="gemini-1-5-pro",
        model_name="Gemini 1.5 Pro",
        organization_id="org_sdk_test",
        family_id="gemini-1-5",
        version="002",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.GOOGLE,
        capabilities={"text_generation", "structured_output", "vision"},
        input_token_cost_per_1k=0.00125,
        output_token_cost_per_1k=0.005,
    )
    sdk.register_model(model)

    # 2. Advance lifecycle
    sdk.lifecycle.transition(
        model_id="gemini-1-5-pro",
        target_state=ModelLifecycleState.EVALUATING,
        actor="dev@test.com",
        reason="Testing",
        organization_id="org_sdk_test",
    )
    sdk.lifecycle.transition(
        model_id="gemini-1-5-pro",
        target_state=ModelLifecycleState.REVIEW,
        actor="dev@test.com",
        reason="Submitting",
        organization_id="org_sdk_test",
    )

    # 3. Approvals
    sdk.submit_for_approval("gemini-1-5-pro", "org_sdk_test")
    for stage in [
        "TECHNICAL_VALIDATION",
        "SECURITY_REVIEW",
        "COMPLIANCE_AUDIT",
        "BUSINESS_APPROVAL",
        "FINAL_GATE",
    ]:
        sdk.approve_stage(
            model_id="gemini-1-5-pro",
            stage_name=stage,
            reviewer="approver@test.com",
            organization_id="org_sdk_test",
        )

    # Activate
    sdk.lifecycle.transition(
        model_id="gemini-1-5-pro",
        target_state=ModelLifecycleState.ACTIVE,
        actor="ops@test.com",
        reason="Activated for production",
        organization_id="org_sdk_test",
    )

    # 4. Selection
    selection = sdk.select_model(
        task_name="document_ocr_and_parse",
        organization_id="org_sdk_test",
        required_capabilities={"vision"},
    )
    assert selection.selected_model.model_id == "gemini-1-5-pro"

    # 5. Execute with routing & fallback
    result, record = sdk.execute_task(
        task_name="document_ocr_and_parse",
        organization_id="org_sdk_test",
        executor_fn=lambda m: f"Extracted via {m.model_name}",
        required_capabilities={"vision"},
    )
    assert "Extracted via Gemini 1.5 Pro" in result
    assert record.status == "SUCCESS"


def test_fastapi_endpoints_governance():
    req = ModelRegisterRequestDTO(
        model_id="claude-3-5-sonnet",
        model_name="Claude Sonnet 3.5",
        organization_id="org_rest",
        family_id="claude-3-5",
        version="2024-10-22",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.ANTHROPIC,
        capabilities={"text_generation", "vision"},
    )
    res = register_model(req, organization_id="org_rest")
    assert res.model_id == "claude-3-5-sonnet"
    assert res.lifecycle_state == ModelLifecycleState.REGISTERED

    # Get model
    get_res = get_model("claude-3-5-sonnet", organization_id="org_rest")
    assert get_res.model_name == "Claude Sonnet 3.5"

    # Capture Snapshot
    snap_req = SnapshotCaptureRequestDTO(
        snapshot_id="snap-api-1",
        task_name="summarize",
        model_id="claude-3-5-sonnet",
        model_version="2024-10-22",
        provider="ANTHROPIC",
        prompt_text="Summarize document",
        system_prompt="You are helpful",
        input_data={"doc_id": "123"},
    )
    snap_res = capture_snapshot(snap_req, organization_id="org_rest")
    assert snap_res.snapshot_id == "snap-api-1"

    # Verify Snapshot
    verify_res = verify_snapshot("snap-api-1")
    assert verify_res["is_valid"] is True
