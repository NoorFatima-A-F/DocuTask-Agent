"""
Verification Pyramid Orchestration Engine handling multi-level test runs, dependency gating, and reports.
"""
from __future__ import annotations
import uuid
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from app.platform_verification.pyramid_engine.domain.models import (
    VerificationLevel,
    ContinuousTrigger,
    TestDefinition,
    LevelExecutionSummary,
    PyramidExecutionStatus,
    PyramidExecutionReport,
    DefectRecord,
)
from app.platform_verification.pyramid_engine.domain.interfaces import ITestOrchestrator
from app.platform_verification.pyramid_engine.core.dependency_graph import DependencyGate
from app.platform_verification.pyramid_engine.core.failure_manager import FailureManager
from app.platform_verification.pyramid_engine.core.continuous_verification import ContinuousVerificationManager
from app.platform_verification.pyramid_engine.core.pyramid_runners import (
    UnitVerificationRunner,
    ComponentVerificationRunner,
    IntegrationVerificationRunner,
    SystemVerificationRunner,
    ProductionVerificationRunner,
    AdversarialVerificationRunner,
    EnterpriseCertificationRunner,
)


class PyramidOrchestrator(ITestOrchestrator):
    """Executes verification tests progressively through the pyramid with strict dependency gating."""

    def __init__(
        self,
        gate: Optional[DependencyGate] = None,
        failure_manager: Optional[FailureManager] = None,
    ):
        self.gate = gate or DependencyGate()
        self.failure_manager = failure_manager or FailureManager()
        self.runners = {
            VerificationLevel.L1_UNIT: UnitVerificationRunner(),
            VerificationLevel.L2_COMPONENT: ComponentVerificationRunner(),
            VerificationLevel.L3_INTEGRATION: IntegrationVerificationRunner(),
            VerificationLevel.L4_SYSTEM: SystemVerificationRunner(),
            VerificationLevel.L5_PRODUCTION: ProductionVerificationRunner(),
            VerificationLevel.L6_ADVERSARIAL: AdversarialVerificationRunner(),
            VerificationLevel.L7_ENTERPRISE_CERTIFICATION: EnterpriseCertificationRunner(),
        }

    def execute_pyramid(
        self,
        system_version: str,
        trigger: ContinuousTrigger,
        tests: List[TestDefinition],
        context: Optional[Dict[str, Any]] = None,
    ) -> PyramidExecutionReport:
        ctx = context or {}
        ctx["version"] = system_version
        target_levels = ContinuousVerificationManager.get_levels_for_trigger(trigger)

        # Group tests by level
        grouped_tests: Dict[VerificationLevel, List[TestDefinition]] = {}
        for t in tests:
            grouped_tests.setdefault(t.level, []).append(t)

        level_summaries: Dict[VerificationLevel, LevelExecutionSummary] = {}
        blocking_failures: List[str] = []
        defects_created: List[DefectRecord] = []
        overall_status = PyramidExecutionStatus.PASSED
        start_time = time.time()

        for level in target_levels:
            # Check dependency gate
            can_run = self.gate.can_execute_level(level, level_summaries)
            if not can_run:
                # Mark level as BLOCKED
                level_tests = grouped_tests.get(level, [])
                summary = LevelExecutionSummary(
                    level=level,
                    total_tests=len(level_tests),
                    passed_tests=0,
                    failed_tests=0,
                    blocked_tests=len(level_tests),
                    duration_ms=0.0,
                    status=PyramidExecutionStatus.BLOCKED,
                    pass_rate=0.0,
                )
                level_summaries[level] = summary
                blocking_failures.append(f"Level '{level.value}' was BLOCKED due to failure in prerequisite levels.")
                overall_status = PyramidExecutionStatus.FAILED
                break

            # Execute level
            runner = self.runners[level]
            current_tests = grouped_tests.get(level, [])
            if not current_tests:
                # Synthesize a default pass test for the level if not provided
                current_tests = [
                    TestDefinition(
                        id=f"auto_{level.name.lower()}",
                        name=f"StandardVerification_{level.name}",
                        level=level,
                        classification=self._default_class(level),
                        description=f"Automated verification for {level.value}",
                        target_component="platform_core",
                    )
                ]

            summary = runner.run_tests(current_tests, ctx)
            level_summaries[level] = summary

            # Process any failures
            for record in summary.records:
                if record.status == PyramidExecutionStatus.FAILED:
                    defect = self.failure_manager.classify_failure(record)
                    defects_created.append(defect)
                    blocking_failures.append(
                        f"[{defect.severity.value}] {defect.title}: {defect.original_failure}"
                    )

            if summary.status == PyramidExecutionStatus.FAILED:
                overall_status = PyramidExecutionStatus.FAILED
                # Mark all remaining levels as BLOCKED
                curr_idx = target_levels.index(level)
                for rem_level in target_levels[curr_idx + 1:]:
                    rem_tests = grouped_tests.get(rem_level, [])
                    level_summaries[rem_level] = LevelExecutionSummary(
                        level=rem_level,
                        total_tests=len(rem_tests),
                        passed_tests=0,
                        failed_tests=0,
                        blocked_tests=len(rem_tests),
                        duration_ms=0.0,
                        status=PyramidExecutionStatus.BLOCKED,
                        pass_rate=0.0,
                    )
                    blocking_failures.append(f"Level '{rem_level.value}' was BLOCKED due to failure in '{level.value}'.")
                break

        total_duration = (time.time() - start_time) * 1000.0
        certification_achieved = (
            overall_status == PyramidExecutionStatus.PASSED
            and VerificationLevel.L7_ENTERPRISE_CERTIFICATION in level_summaries
            and level_summaries[VerificationLevel.L7_ENTERPRISE_CERTIFICATION].status == PyramidExecutionStatus.PASSED
        )

        return PyramidExecutionReport(
            report_id=f"pyr_{uuid.uuid4().hex[:10]}",
            execution_id=ctx.get("execution_id", f"exec_{uuid.uuid4().hex[:8]}"),
            system_version=system_version,
            trigger=trigger,
            timestamp=datetime.now(timezone.utc).isoformat(),
            level_summaries=level_summaries,
            overall_status=overall_status,
            certification_achieved=certification_achieved,
            blocking_failures=blocking_failures,
            defects_created=defects_created,
            duration_ms=round(total_duration, 2),
        )

    def _default_class(self, level: VerificationLevel):
        from app.platform_verification.pyramid_engine.domain.models import TestClassification
        if level == VerificationLevel.L6_ADVERSARIAL:
            return TestClassification.SECURITY
        elif level == VerificationLevel.L5_PRODUCTION:
            return TestClassification.PERFORMANCE
        return TestClassification.FUNCTIONAL
