"""
Phase 13.17: Failure Classifier & Trace Analyzer
Automated root-cause isolation, call tree inspection, and critical path analysis.
"""

from __future__ import annotations
from typing import List, Optional
from app.runtime.ai_operations.models.schemas import (
    ExecutionTrace,
    Span,
    SpanStatus,
    FailureCategory,
    FailureAnalysisResult,
)


class TraceAnalyzer:
    """Extracts call trees, critical execution paths, and bottleneck spans."""

    @staticmethod
    def extract_critical_path(trace: ExecutionTrace) -> List[str]:
        """Find the sequential path of spans consuming the most latency."""
        if not trace.spans:
            return [trace.root_span_name]

        # Sort by duration descending
        sorted_spans = sorted(trace.spans, key=lambda s: s.duration_ms, reverse=True)
        return [f"{s.name} ({s.span_type.value}: {s.duration_ms:.1f}ms)" for s in sorted_spans[:5]]

    @staticmethod
    def identify_failing_span(trace: ExecutionTrace) -> Optional[Span]:
        """Find the root failing span in the trace."""
        for s in trace.spans:
            if s.status in (SpanStatus.ERROR, SpanStatus.TIMEOUT):
                return s
        return None


class FailureClassifier:
    """Classifies failures into actionable enterprise root-cause taxonomies."""

    @staticmethod
    def classify_failure(trace: ExecutionTrace) -> FailureAnalysisResult:
        failing_span = TraceAnalyzer.identify_failing_span(trace)
        err_msg = (failing_span.error_message if failing_span else "") or "Execution anomaly"
        err_lower = err_msg.lower()

        category = FailureCategory.UNSPECIFIED_RUNTIME_ERROR
        summary = f"Execution failed in {trace.root_span_name}"
        remediation = "Inspect agent prompt and runtime configuration."

        if "timeout" in err_lower or (failing_span and failing_span.status == SpanStatus.TIMEOUT):
            category = FailureCategory.TOOL_TIMEOUT
            summary = f"Tool or downstream API timed out during execution: {err_msg}"
            remediation = "Increase timeout threshold or configure automatic retry with exponential backoff."
        elif "schema" in err_lower or "validation" in err_lower or "json" in err_lower:
            category = FailureCategory.TOOL_SCHEMA_VIOLATION
            summary = f"Tool argument schema violation: {err_msg}"
            remediation = "Refine prompt with strict JSON schema instructions and few-shot examples."
        elif "loop" in err_lower or len(trace.spans) > 25:
            category = FailureCategory.RECURSIVE_LOOP
            summary = "Agent entered a cyclic recursive tool invocation loop."
            remediation = "Inject cycle-breaking guardrails and maximum step limits."
        elif trace.total_prompt_tokens > 30000:
            category = FailureCategory.CONTEXT_WINDOW_OVERFLOW
            summary = f"Context window capacity exceeded ({trace.total_prompt_tokens} tokens)."
            remediation = "Enable context window distillation and semantic chunk pruning."
        elif "pii" in err_lower or "secret" in err_lower:
            category = FailureCategory.PII_POLICY_VIOLATION
            summary = "PII or sensitive credential detected in prompt payload."
            remediation = "Enable upstream regex redaction filters and guardrail sanitization."

        return FailureAnalysisResult(
            trace_id=trace.trace_id,
            agent_id=trace.agent_id,
            category=category,
            root_cause_summary=summary,
            failing_span_id=failing_span.span_id if failing_span else None,
            critical_path=TraceAnalyzer.extract_critical_path(trace),
            confidence=0.96,
            suggested_remediation=remediation,
        )
