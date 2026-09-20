"""Unit tests for Infrastructure Pipeline Engine."""
import pytest
from app.deployment.core.exceptions import ApprovalGateException
from app.deployment.pipelines.approvals import ApprovalGate
from app.deployment.pipelines.engine import PipelineEngine, PipelineRunStatus
from app.deployment.pipelines.stages import PipelineStage, PipelineStageType


def test_approval_gate_satisfaction():
    gate = ApprovalGate("prod-gate", required_roles=["lead", "sec"])
    assert gate.is_satisfied is False

    gate.approve("alice", "lead")
    assert gate.is_satisfied is False

    gate.approve("bob", "sec")
    assert gate.is_satisfied is True
    assert gate.verify_gate() is True


def test_approval_gate_emergency_bypass():
    gate = ApprovalGate("prod-gate", required_roles=["lead", "sec"])
    gate.emergency_bypass("admin", "P0 Incident hotfix deployment override")
    assert gate.is_satisfied is True
    assert gate.verify_gate() is True


def test_pipeline_engine_execution():
    pipeline = PipelineEngine("docutask-delivery-pipeline")
    pipeline.add_stage(PipelineStage(
        name="lint",
        stage_type=PipelineStageType.LINT,
        action_fn=lambda ctx: {"lint_passed": True},
    ))
    pipeline.add_stage(PipelineStage(
        name="unit_tests",
        stage_type=PipelineStageType.UNIT_TEST,
        action_fn=lambda ctx: {"tests_passed": 150},
    ))

    run = pipeline.execute()
    assert run.status == PipelineRunStatus.SUCCESS
    assert len(run.stage_results) == 2
    assert run.context["lint_passed"] is True
    assert run.context["tests_passed"] == 150


def test_pipeline_engine_failure_stop():
    pipeline = PipelineEngine("failing-pipeline")
    def fail_action(ctx):
        raise ValueError("Critical test failure")

    pipeline.add_stage(PipelineStage(
        name="failing_stage",
        stage_type=PipelineStageType.UNIT_TEST,
        action_fn=fail_action,
        critical=True,
    ))

    run = pipeline.execute()
    assert run.status == PipelineRunStatus.FAILED
    assert "Critical test failure" in (run.error or "")
