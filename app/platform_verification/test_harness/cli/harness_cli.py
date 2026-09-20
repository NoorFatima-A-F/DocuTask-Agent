"""
Developer CLI Interface for Test Harness Operations.
"""
from __future__ import annotations
from typing import Any, Dict, List
from app.platform_verification.test_harness.domain.models import (
    VerificationTestSpec,
    ExecutionMode,
    HarnessExecutionReport,
)
from app.platform_verification.test_harness.core.execution_engine import HarnessExecutionEngine


class HarnessCLI:
    """Command-line interface commands: verify run, suite, status, report."""

    def __init__(self, engine: HarnessExecutionEngine) -> None:
        self.engine = engine

    def run_test(self, spec: VerificationTestSpec) -> Dict[str, Any]:
        """Runs a single test: 'verify run <id>'."""
        report = self.engine.run_suite([spec], mode=ExecutionMode.SEQUENTIAL)
        res = report.results[0] if report.results else None
        return {
            "test_id": spec.id,
            "passed": res.passed if res else False,
            "duration_ms": res.duration_ms if res else 0.0,
            "error": res.error_message if res else None,
        }

    def run_suite(self, specs: List[VerificationTestSpec], mode: str = "SEQUENTIAL") -> Dict[str, Any]:
        """Runs a test suite: 'verify suite <name>'."""
        exec_mode = ExecutionMode.PARALLEL if mode.upper() == "PARALLEL" else ExecutionMode.SEQUENTIAL
        report = self.engine.run_suite(specs, mode=exec_mode)
        return {
            "report_id": report.report_id,
            "total_jobs": report.total_jobs,
            "passed_jobs": report.passed_jobs,
            "failed_jobs": report.failed_jobs,
            "duration_ms": report.duration_ms,
        }
