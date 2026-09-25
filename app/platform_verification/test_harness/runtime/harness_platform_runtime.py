"""
Unified Enterprise Verification Test Harness Platform Runtime Facade.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.test_harness.domain.models import (
    VerificationTestSpec,
    HarnessExecutionReport,
    ExecutionMode,
)
from app.platform_verification.test_harness.core.execution_engine import HarnessExecutionEngine
from app.platform_verification.test_harness.core.worker_pool import WorkerPool
from app.platform_verification.test_harness.core.scheduler import TestScheduler
from app.platform_verification.test_harness.core.plugin_manager import PluginManager
from app.platform_verification.test_harness.cli.harness_cli import HarnessCLI
from app.platform_verification.test_harness.api.harness_api import HarnessAPI


class TestHarnessPlatformRuntime:
    """Top-level facade coordinating the Test Harness execution engine, workers, scheduler, CLI, and API."""
    __test__ = False

    def __init__(self) -> None:
        self.engine = HarnessExecutionEngine()
        self.worker_pool = WorkerPool()
        self.scheduler = TestScheduler()
        self.plugin_manager = PluginManager()
        self.cli = HarnessCLI(self.engine)
        self.api = HarnessAPI(self.engine)

    def execute_test_suite(
        self,
        specs: List[VerificationTestSpec],
        mode: ExecutionMode = ExecutionMode.SEQUENTIAL,
        context_overrides: Optional[Dict[str, Any]] = None,
    ) -> HarnessExecutionReport:
        """Runs a verification suite through the execution engine."""
        return self.engine.run_suite(specs, mode=mode, context_overrides=context_overrides)
