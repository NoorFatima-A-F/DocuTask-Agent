"""
Workflow Execution Engine supporting Sequential, Parallel, and Conditional execution DAGs.
"""
from __future__ import annotations
import uuid
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional
from app.platform_verification.test_harness.domain.models import (
    VerificationTestSpec,
    VerificationContext,
    HarnessExecutionResult,
    HarnessExecutionReport,
    ExecutionMode,
    TestCategory,
    TestLifecycleState,
)
from app.platform_verification.test_harness.domain.interfaces import ITestOrchestrator
from app.platform_verification.test_harness.core.context_manager import VerificationContextManager
from app.platform_verification.test_harness.core.lifecycle import TestLifecycleManager
from app.platform_verification.test_harness.core.retry_handler import RetryHandler
from app.platform_verification.test_harness.core.runners import (
    FunctionalHarnessRunner,
    AiEvaluationHarnessRunner,
    PerformanceHarnessRunner,
    SecurityHarnessRunner,
    ChaosHarnessRunner,
)


class HarnessExecutionEngine(ITestOrchestrator):
    """Executes verification test suites across sequential, parallel, and conditional modes."""

    def __init__(self) -> None:
        self.runners = {
            TestCategory.FUNCTIONAL: FunctionalHarnessRunner(),
            TestCategory.REGRESSION: FunctionalHarnessRunner(),
            TestCategory.COMPLIANCE: FunctionalHarnessRunner(),
            TestCategory.AI_QUALITY: AiEvaluationHarnessRunner(),
            TestCategory.PERFORMANCE: PerformanceHarnessRunner(),
            TestCategory.SECURITY: SecurityHarnessRunner(),
            TestCategory.CHAOS: ChaosHarnessRunner(),
        }

    def run_suite(
        self,
        specs: List[VerificationTestSpec],
        mode: ExecutionMode = ExecutionMode.SEQUENTIAL,
        context_overrides: Optional[Dict[str, Any]] = None,
    ) -> HarnessExecutionReport:
        start_time = time.time()
        results: List[HarnessExecutionResult] = []

        if mode == ExecutionMode.SEQUENTIAL:
            for spec in specs:
                res = self._execute_single_spec(spec, context_overrides)
                results.append(res)
        elif mode == ExecutionMode.PARALLEL:
            with ThreadPoolExecutor(max_workers=min(8, max(1, len(specs)))) as executor:
                futures = {executor.submit(self._execute_single_spec, spec, context_overrides): spec for spec in specs}
                for f in as_completed(futures):
                    results.append(f.result())
        elif mode == ExecutionMode.CONDITIONAL:
            for spec in specs:
                res = self._execute_single_spec(spec, context_overrides)
                results.append(res)
                if not res.passed:
                    # Conditional stop: if critical test fails, abort remaining pipeline
                    break

        total_duration = (time.time() - start_time) * 1000.0
        passed_cnt = sum(1 for r in results if r.passed)
        failed_cnt = len(results) - passed_cnt

        return HarnessExecutionReport(
            report_id=f"rep_{uuid.uuid4().hex[:10]}",
            execution_mode=mode,
            total_jobs=len(results),
            passed_jobs=passed_cnt,
            failed_jobs=failed_cnt,
            results=results,
            duration_ms=round(total_duration, 2),
        )

    def _execute_single_spec(
        self, spec: VerificationTestSpec, context_overrides: Optional[Dict[str, Any]] = None
    ) -> HarnessExecutionResult:
        ctx = VerificationContextManager.create_context(
            test_id=spec.id,
            environment=spec.environment,
            dataset_version=spec.dataset.get("version", "v1.0"),
        )
        lifecycle = TestLifecycleManager()
        lifecycle.transition_to(TestLifecycleState.VALIDATED, "Spec validated")
        lifecycle.transition_to(TestLifecycleState.SCHEDULED, "Scheduled for execution")
        lifecycle.transition_to(TestLifecycleState.EXECUTING, "Executing test")

        runner = self.runners.get(spec.category, FunctionalHarnessRunner())
        result = RetryHandler.execute_with_retry(runner.execute_test, spec, ctx)

        lifecycle.transition_to(TestLifecycleState.COLLECTING_EVIDENCE, "Evidence gathered")
        lifecycle.transition_to(TestLifecycleState.EVALUATING, "Evaluating assertions")
        lifecycle.transition_to(TestLifecycleState.COMPLETED, "Completed test execution")

        return result
