"""Tests for CI/CD Pipeline Engine, Stages, and Runners."""

from app.infrastructure.deployment.pipelines import (
    StageType,
    StageStatus,
    PipelineStageConfig,
    StageRunner,
    PipelineEngine,
)


def test_pipeline_stage_runner_and_retries() -> None:
    runner = StageRunner()
    attempts_counted = 0

    def flaky_handler(ctx: dict) -> dict:
        nonlocal attempts_counted
        attempts_counted += 1
        if attempts_counted < 2:
            raise RuntimeError("Transient compiler error")
        return {"status": "ok", "artifacts": ["dist/worker.whl"]}

    stage = PipelineStageConfig(
        name="Compile",
        stage_type=StageType.BUILD,
        retry_count=3,
        handler=flaky_handler,
    )

    context = {}
    res = runner.run_stage(stage, context)
    assert res.status == StageStatus.PASSED
    assert attempts_counted == 2
    assert "dist/worker.whl" in res.output_artifacts


def test_pipeline_engine_standard_run() -> None:
    engine = PipelineEngine()
    stages = engine.build_standard_ci_pipeline("workflow-orchestrator")

    run = engine.execute_pipeline(
        pipeline_name="workflow-orchestrator-ci",
        commit_sha="a1b2c3d4e5f6",
        stages=stages,
    )

    assert run.status == StageStatus.PASSED
    assert len(run.stages) == 8
    assert run.total_duration_ms >= 0.0
    assert engine.get_run(run.run_id) is not None
