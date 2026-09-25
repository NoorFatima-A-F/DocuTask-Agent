"""
In-process REST API Router for Test Harness Management, Execution, Evidence, and Metrics.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.test_harness.domain.models import (
    VerificationTestSpec,
    HarnessExecutionReport,
    ExecutionMode,
)
from app.platform_verification.test_harness.core.execution_engine import HarnessExecutionEngine


class HarnessAPI:
    """In-process API endpoints for test harness operations."""

    def __init__(self, engine: HarnessExecutionEngine) -> None:
        self.engine = engine
        self._test_store: Dict[str, VerificationTestSpec] = {}
        self._execution_store: Dict[str, HarnessExecutionReport] = {}

    def post_test(self, spec: VerificationTestSpec) -> Dict[str, Any]:
        """POST /tests"""
        self._test_store[spec.id] = spec
        return {"status": "CREATED", "test_id": spec.id}

    def get_tests(self) -> List[Dict[str, Any]]:
        """GET /tests"""
        return [{"id": s.id, "name": s.name, "category": s.category.value} for s in self._test_store.values()]

    def get_test(self, test_id: str) -> Optional[Dict[str, Any]]:
        """GET /tests/{id}"""
        if test_id not in self._test_store:
            return None
        s = self._test_store[test_id]
        return {"id": s.id, "name": s.name, "category": s.category.value, "environment": s.environment}

    def post_execution(self, test_ids: List[str], mode: str = "SEQUENTIAL") -> Dict[str, Any]:
        """POST /executions"""
        specs = [self._test_store[tid] for tid in test_ids if tid in self._test_store]
        exec_mode = ExecutionMode.PARALLEL if mode.upper() == "PARALLEL" else ExecutionMode.SEQUENTIAL
        report = self.engine.run_suite(specs, mode=exec_mode)
        self._execution_store[report.report_id] = report
        return {"execution_id": report.report_id, "status": "COMPLETED", "passed": report.failed_jobs == 0}

    def get_execution(self, report_id: str) -> Optional[Dict[str, Any]]:
        """GET /executions/{id}"""
        if report_id not in self._execution_store:
            return None
        r = self._execution_store[report_id]
        return {
            "report_id": r.report_id,
            "total_jobs": r.total_jobs,
            "passed_jobs": r.passed_jobs,
            "failed_jobs": r.failed_jobs,
            "duration_ms": r.duration_ms,
        }

    def get_execution_evidence(self, report_id: str) -> Optional[List[str]]:
        """GET /executions/{id}/evidence"""
        if report_id not in self._execution_store:
            return None
        r = self._execution_store[report_id]
        evidence: List[str] = []
        for res in r.results:
            evidence.extend(res.evidence_paths)
        return evidence

    def get_execution_metrics(self, report_id: str) -> Optional[Dict[str, float]]:
        """GET /executions/{id}/metrics"""
        if report_id not in self._execution_store:
            return None
        r = self._execution_store[report_id]
        metrics: Dict[str, float] = {}
        for res in r.results:
            metrics.update(res.metrics_collected)
        return metrics
