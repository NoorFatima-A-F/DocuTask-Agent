"""
Comprehensive test suite for Enterprise Verification Test Harness & Execution Framework (PART 3).
"""
import pytest
from app.platform_verification.test_harness import (
    TestLifecycleState,
    TestCategory,
    TestHarnessLevel,
    ExecutionMode,
    WorkerStatus,
    VerificationTestSpec,
    TestSpecParser,
    TestLifecycleManager,
    VerificationContextManager,
    TestHarnessPlatformRuntime,
)


def test_spec_parser_and_declarative_definition():
    raw_spec = {
        "id": "OCR-001",
        "name": "Invoice OCR Accuracy Test",
        "description": "Validates invoice field extraction correctness",
        "category": "functional",
        "level": "component",
        "environment": "staging",
        "dataset": {"id": "invoice_dataset_v2", "version": "2.1.0"},
        "metrics": ["accuracy", "latency", "confidence"],
        "evidence": ["logs", "traces", "extracted_json"],
        "timeout_ms": 3000,
        "retry_policy": {"max_retries": 2, "initial_delay_ms": 20.0},
    }

    spec = TestSpecParser.parse_dict(raw_spec)
    assert spec.id == "OCR-001"
    assert spec.category == TestCategory.FUNCTIONAL
    assert spec.level == TestHarnessLevel.COMPONENT
    assert spec.retry_policy.max_retries == 2


def test_lifecycle_state_machine():
    manager = TestLifecycleManager()
    assert manager.current_state == TestLifecycleState.CREATED

    manager.transition_to(TestLifecycleState.VALIDATED, "Spec valid")
    manager.transition_to(TestLifecycleState.SCHEDULED, "Scheduled")
    manager.transition_to(TestLifecycleState.EXECUTING, "Running")
    manager.transition_to(TestLifecycleState.COLLECTING_EVIDENCE, "Gathering logs")
    manager.transition_to(TestLifecycleState.EVALUATING, "Evaluating assertions")
    manager.transition_to(TestLifecycleState.COMPLETED, "Done")
    manager.transition_to(TestLifecycleState.ARCHIVED, "Archived")

    assert manager.current_state == TestLifecycleState.ARCHIVED
    assert len(manager.get_history()) == 7

    # Disallowed transition should raise ValueError
    with pytest.raises(ValueError):
        manager.transition_to(TestLifecycleState.EXECUTING)


def test_context_isolation_sandbox():
    ctx = VerificationContextManager.create_context(test_id="OCR-001", environment="staging")
    assert ctx.workspace_root.exists()
    assert ctx.input_dir.exists()
    assert ctx.output_dir.exists()
    assert ctx.logs_dir.exists()
    assert ctx.evidence_dir.exists()

    VerificationContextManager.cleanup_context(ctx)
    assert not ctx.workspace_root.exists()


def test_sequential_parallel_and_conditional_execution():
    runtime = TestHarnessPlatformRuntime()

    spec1 = VerificationTestSpec(
        id="FUNC-01",
        name="Functional Extract",
        description="Extract fields",
        category=TestCategory.FUNCTIONAL,
        level=TestHarnessLevel.COMPONENT,
        environment="staging",
        dataset={"id": "ds1", "version": "v1.0"},
    )
    spec2 = VerificationTestSpec(
        id="AI-01",
        name="AI Grounding",
        description="Verify grounding",
        category=TestCategory.AI_QUALITY,
        level=TestHarnessLevel.SYSTEM,
        environment="staging",
        dataset={"id": "ds1", "version": "v1.0"},
    )
    spec3 = VerificationTestSpec(
        id="SEC-01",
        name="Security Scan",
        description="Verify prompt injection",
        category=TestCategory.SECURITY,
        level=TestHarnessLevel.ADVERSARIAL,
        environment="staging",
        dataset={"id": "ds1", "version": "v1.0"},
    )

    # 1. Sequential Mode
    seq_report = runtime.execute_test_suite([spec1, spec2, spec3], mode=ExecutionMode.SEQUENTIAL)
    assert seq_report.total_jobs == 3
    assert seq_report.passed_jobs == 3

    # 2. Parallel Mode
    par_report = runtime.execute_test_suite([spec1, spec2, spec3], mode=ExecutionMode.PARALLEL)
    assert par_report.total_jobs == 3
    assert par_report.passed_jobs == 3

    # 3. Conditional Mode with Failure
    failing_spec = VerificationTestSpec(
        id="FAIL-01",
        name="Failing Check",
        description="Simulated fail",
        category=TestCategory.FUNCTIONAL,
        level=TestHarnessLevel.COMPONENT,
        environment="staging",
        dataset={"id": "ds1", "version": "v1.0"},
        execution={"simulate_failure": True},
    )
    cond_report = runtime.execute_test_suite([failing_spec, spec2, spec3], mode=ExecutionMode.CONDITIONAL)
    assert cond_report.total_jobs == 1
    assert cond_report.failed_jobs == 1


def test_worker_pool_and_scheduling():
    runtime = TestHarnessPlatformRuntime()
    workers = runtime.worker_pool.list_workers()
    assert len(workers) >= 3

    worker = runtime.worker_pool.allocate_worker(TestCategory.AI_QUALITY)
    assert worker is not None
    assert worker.status == WorkerStatus.BUSY

    runtime.worker_pool.release_worker(worker.worker_id)
    assert worker.status == WorkerStatus.IDLE

    # Test Scheduler
    runtime.scheduler.schedule_cron("nightly_01", "0 2 * * *", [])
    runtime.scheduler.schedule_event("git_commit_01", "push:main", [])
    assert len(runtime.scheduler.list_schedules()) == 2


def test_cli_and_api_integration():
    runtime = TestHarnessPlatformRuntime()
    spec = VerificationTestSpec(
        id="CLI-01",
        name="CLI Test",
        description="Verify CLI",
        category=TestCategory.FUNCTIONAL,
        level=TestHarnessLevel.UNIT,
        environment="dev",
        dataset={"id": "ds_cli", "version": "v1.0"},
    )

    # Test CLI
    cli_res = runtime.cli.run_test(spec)
    assert cli_res["test_id"] == "CLI-01"
    assert cli_res["passed"] is True

    # Test API
    create_resp = runtime.api.post_test(spec)
    assert create_resp["status"] == "CREATED"

    exec_resp = runtime.api.post_execution(["CLI-01"])
    assert exec_resp["status"] == "COMPLETED"
    assert exec_resp["passed"] is True

    report_id = exec_resp["execution_id"]
    metrics = runtime.api.get_execution_metrics(report_id)
    assert metrics is not None
    assert "accuracy" in metrics
