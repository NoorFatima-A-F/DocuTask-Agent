"""
Standardized interfaces for Enterprise Verification Test Harness.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.platform_verification.test_harness.domain.models import (
    VerificationTestSpec,
    VerificationContext,
    ExecutionJob,
    HarnessExecutionResult,
    HarnessExecutionReport,
    WorkerNode,
    ExecutionMode,
    TestLifecycleState,
)


class ITestHarnessRunner(ABC):
    """Executes a test specification inside an isolated verification context."""
    @abstractmethod
    def execute_test(
        self, spec: VerificationTestSpec, context: VerificationContext
    ) -> HarnessExecutionResult:
        pass


class ITestOrchestrator(ABC):
    """Orchestrates multi-test verification jobs through execution DAGs."""
    @abstractmethod
    def run_suite(
        self,
        specs: List[VerificationTestSpec],
        mode: ExecutionMode = ExecutionMode.SEQUENTIAL,
        context_overrides: Optional[Dict[str, Any]] = None,
    ) -> HarnessExecutionReport:
        pass


class IWorkerPool(ABC):
    """Manages worker node registration, heartbeat, and task dispatch."""
    @abstractmethod
    def register_worker(self, worker_id: str, capabilities: List[Any]) -> WorkerNode:
        pass

    @abstractmethod
    def heartbeat(self, worker_id: str) -> bool:
        pass

    @abstractmethod
    def allocate_worker(self, category: Any) -> Optional[WorkerNode]:
        pass

    @abstractmethod
    def release_worker(self, worker_id: str) -> None:
        pass


class IVerificationPlugin(ABC):
    """Standardized plugin extension contract for custom runners/evaluators/reporters."""
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def validate(self, spec: VerificationTestSpec) -> bool:
        pass

    @abstractmethod
    def execute(self, spec: VerificationTestSpec, context: VerificationContext) -> Dict[str, Any]:
        pass

    @abstractmethod
    def collect_results(self, context: VerificationContext) -> Dict[str, Any]:
        pass

    @abstractmethod
    def cleanup(self, context: VerificationContext) -> None:
        pass
