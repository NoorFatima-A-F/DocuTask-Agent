"""
Unit and Integration tests for Enterprise Continuous Verification CI/CD Pipeline (PART 7).
"""
import pytest
from app.platform_verification.cicd_pipeline import (
    ChangeRiskLevel,
    EnterpriseCICDPlatformRuntime,
    PipelineChangeType,
    PipelineExecutionStatus,
    PipelineStageType,
    PromotionStatus,
    RollbackTriggerReason,
    StageExecutionStatus,
    TargetEnvironment,
)


@pytest.fixture
def runtime():
    return EnterpriseCICDPlatformRuntime()


def test_change_detector_adaptive_classification(runtime):
    """Test intelligent change classification and dynamic stage selection."""
    # 1. Model update change -> Critical Risk, AI + Security + Perf stages
    model_ctx = runtime.change_detector.analyze_changes(
        change_id="CHG-001",
        commit_sha="a1b2c3d4",
        branch="feature/model-update",
        author="ml-engineer@docutask.internal",
        changed_paths=["models/gemini_extractor_weights.bin", "configs/inference.yaml"],
    )
    assert model_ctx.primary_change_type == PipelineChangeType.MODEL
    assert model_ctx.risk_level == ChangeRiskLevel.CRITICAL
    assert PipelineStageType.STAGE_6_AI_EVALUATION in model_ctx.required_stages
    assert PipelineStageType.STAGE_7_SECURITY_VERIFICATION in model_ctx.required_stages

    # 2. Prompt update change -> High Risk, AI Evaluation included
    prompt_ctx = runtime.change_detector.analyze_changes(
        change_id="CHG-002",
        commit_sha="b2c3d4e5",
        branch="feature/prompt-tuning",
        author="prompt-engineer@docutask.internal",
        changed_paths=["prompts/invoice_extraction_v3.jinja2"],
    )
    assert prompt_ctx.primary_change_type == PipelineChangeType.PROMPT
    assert prompt_ctx.risk_level == ChangeRiskLevel.HIGH
    assert PipelineStageType.STAGE_6_AI_EVALUATION in prompt_ctx.required_stages

    # 3. Documentation only change -> Low Risk, lightweight linting only
    doc_ctx = runtime.change_detector.analyze_changes(
        change_id="CHG-003",
        commit_sha="c3d4e5f6",
        branch="docs/architecture-update",
        author="tech-writer@docutask.internal",
        changed_paths=["docs/verification_architecture.md", "README.md"],
    )
    assert doc_ctx.primary_change_type == PipelineChangeType.DOCUMENTATION
    assert doc_ctx.risk_level == ChangeRiskLevel.LOW
    assert len(doc_ctx.required_stages) == 1
    assert doc_ctx.required_stages[0] == PipelineStageType.STAGE_1_SOURCE_VALIDATION


def test_pipeline_orchestration_successful_run(runtime):
    """Test full pipeline lifecycle execution with passing stages."""
    ctx = runtime.change_detector.analyze_changes(
        change_id="CHG-CODE-001",
        commit_sha="fedcba98",
        branch="main",
        author="backend-dev@docutask.internal",
        changed_paths=["app/services/document_service.py", "app/api/endpoints.py"],
    )

    record = runtime.orchestrator.trigger_pipeline(
        change_context=ctx,
        target_env=TargetEnvironment.STAGING,
    )

    assert record.status == PipelineExecutionStatus.PASSED
    assert record.deployment_decision == "APPROVED"
    assert record.certification_id is not None
    assert len(record.stage_records) == len(ctx.required_stages)
    assert all(s.status == StageExecutionStatus.PASSED for s in record.stage_records)


def test_environment_promotion_gate_enforcement(runtime):
    """Test promotion gate validation from Staging to Production."""
    ctx = runtime.change_detector.analyze_changes(
        change_id="CHG-CODE-002",
        commit_sha="11223344",
        branch="main",
        author="release-manager@docutask.internal",
        changed_paths=["app/core/engine.py"],
    )

    record = runtime.orchestrator.trigger_pipeline(
        change_context=ctx,
        target_env=TargetEnvironment.STAGING,
    )

    # Promote to Production
    promo = runtime.promotion_engine.evaluate_and_promote(
        pipeline_record=record,
        target_env=TargetEnvironment.PRODUCTION,
        approved_by="LeadReleaseArchitect",
    )

    assert promo.status == PromotionStatus.PROMOTED
    assert promo.target_env == TargetEnvironment.PRODUCTION
    assert promo.actual_certification_level == "LEVEL_5_PRODUCTION_CERTIFIED"


def test_automated_rollback_execution(runtime):
    """Test automated rollback upon incident and certificate invalidation."""
    rollback = runtime.rollback_engine.execute_rollback(
        pipeline_id="PIPE-FAULTY-01",
        target_env=TargetEnvironment.PRODUCTION,
        reason=RollbackTriggerReason.ERROR_SPIKE,
        failed_version="v2.4.1",
        previous_stable_version="v2.4.0",
    )

    assert rollback.rollback_id.startswith("RLBK-")
    assert rollback.trigger_reason == RollbackTriggerReason.ERROR_SPIKE
    assert rollback.invalidated_certification_id == "CERT-PIPE-FAULTY-01"
    assert rollback.status == "COMPLETED"


def test_artifact_registry_and_supply_chain_verification(runtime):
    """Test artifact registration, SHA-256 integrity, and supply chain scanning."""
    content = b"DocuTask Agent Binary Build Payload v2.4.0"
    art = runtime.artifact_registry.register_artifact(
        name="docutask-agent",
        version="v2.4.0",
        artifact_type="CONTAINER",
        content_bytes=content,
    )

    assert art.verified is True
    assert runtime.artifact_registry.verify_artifact_integrity(art.artifact_id) is True

    scan_report = runtime.supply_chain_verifier.scan_pipeline_artifacts(
        pipeline_id="PIPE-TEST-SCAN",
        artifacts=[art],
    )
    assert scan_report.passed is True
    assert scan_report.sbom_signature_valid is True
    assert scan_report.dependency_vulnerabilities_count == 0


def test_pipeline_observability_metrics_aggregation(runtime):
    """Test recording pipeline executions and retrieving aggregated DORA metrics."""
    ctx = runtime.change_detector.analyze_changes(
        change_id="CHG-TEST-009",
        commit_sha="aabbccdd",
        branch="main",
        author="sre@docutask.internal",
        changed_paths=["app/services/extractor.py"],
    )
    rec = runtime.orchestrator.trigger_pipeline(ctx, TargetEnvironment.STAGING)
    runtime.observability.record_pipeline_run(rec)

    metrics = runtime.observability.get_metrics()
    assert metrics.total_pipeline_runs >= 1
    assert metrics.successful_runs >= 1
    assert metrics.change_failure_rate == 0.0
