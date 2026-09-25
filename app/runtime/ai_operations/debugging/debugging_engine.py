"""
Phase 13.17: Debugging & Root Cause Analysis Engine
Manages execution failure diagnostics, anomaly reports, and remediation recommendations.
"""

from __future__ import annotations
from typing import List, Optional
from app.runtime.ai_operations.models.schemas import (
    ExecutionTrace,
    FailureAnalysisResult,
    FailureCategory,
)
from app.runtime.ai_operations.debugging.trace_analyzer import (
    FailureClassifier,
)


class DebuggingEngine:
    """Master debugging and root-cause analysis engine."""

    def __init__(self):
        self._failure_logs: List[FailureAnalysisResult] = []
        self._seed_diagnostics()

    def _seed_diagnostics(self):
        sample_failures = [
            {
                "trace_id": "trace_seed_001",
                "agent_id": "agent_doc_extractor",
                "category": FailureCategory.TOOL_TIMEOUT,
                "summary": "Downstream OCR endpoint timeout after 3500ms.",
                "remediation": "Increase timeout threshold or enable secondary OCR fallback.",
            },
            {
                "trace_id": "trace_seed_002",
                "agent_id": "agent_scientist",
                "category": FailureCategory.TOOL_SCHEMA_VIOLATION,
                "summary": "Hypothesis validator returned unparseable malformed JSON output.",
                "remediation": "Enforce strict Pydantic JSON schema mode on model output.",
            },
            {
                "trace_id": "trace_seed_003",
                "agent_id": "agent_chief_architect",
                "category": FailureCategory.RECURSIVE_LOOP,
                "summary": "Agent repeated identical dependency lookup 6 times consecutively.",
                "remediation": "Implement memoization and loop prevention guardrail.",
            },
        ]
        for f in sample_failures:
            res = FailureAnalysisResult(
                trace_id=f["trace_id"],
                agent_id=f["agent_id"],
                category=f["category"],
                root_cause_summary=f["summary"],
                critical_path=["Context Preparation (50ms)", "Tool Execution (3500ms)", "Output Aggregation (12ms)"],
                suggested_remediation=f["remediation"],
            )
            self._failure_logs.append(res)

    def diagnose_trace(self, trace: ExecutionTrace) -> FailureAnalysisResult:
        result = FailureClassifier.classify_failure(trace)
        self._failure_logs.append(result)
        return result

    def get_failure_logs(self, limit: int = 50, agent_id: Optional[str] = None) -> List[FailureAnalysisResult]:
        logs = self._failure_logs
        if agent_id:
            logs = [l for l in logs if l.agent_id == agent_id]
        return logs[-limit:]
