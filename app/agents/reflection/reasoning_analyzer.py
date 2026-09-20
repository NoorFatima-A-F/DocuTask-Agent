"""
Reasoning Analyzer.
Evaluates cognitive steps, assumptions, evidence linkage, and logical coherence.
"""

from typing import Any, Dict, List
from app.agents.reflection.interfaces import IReasoningAnalyzer
from app.agents.reflection.reflection_context import ReasoningStepTrace


class ReasoningAnalyzer(IReasoningAnalyzer):
    """Analyzes reasoning steps for evidence support, confidence, and cognitive rigor."""

    def analyze_reasoning(self, reasoning_trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes dictionary representation of reasoning traces."""
        total_steps = len(reasoning_trace)
        if total_steps == 0:
            return {
                "total_reasoning_steps": 0,
                "average_confidence": 1.0,
                "unsupported_assertions_count": 0,
                "assumptions_count": 0,
                "reasoning_rigor_score": 1.0
            }

        confidences = [float(s.get("confidence_score", 1.0)) for s in reasoning_trace]
        avg_confidence = sum(confidences) / total_steps if confidences else 1.0

        unsupported = 0
        total_assumptions = 0
        for step in reasoning_trace:
            evidence = step.get("evidence", [])
            assumptions = step.get("assumptions", [])
            total_assumptions += len(assumptions)
            if not evidence and assumptions:
                unsupported += 1

        rigor_score = avg_confidence
        if unsupported > 0:
            rigor_score -= min(0.4, unsupported * 0.1)
        rigor_score = max(0.0, min(1.0, rigor_score))

        return {
            "total_reasoning_steps": total_steps,
            "average_confidence": avg_confidence,
            "unsupported_assertions_count": unsupported,
            "assumptions_count": total_assumptions,
            "reasoning_rigor_score": rigor_score
        }
