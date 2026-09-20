"""
Phase 13.17: Evaluation Metrics & Automated Scoring
Calculates Task Success, Grounding, Hallucination Index, Tool Efficiency, Safety, and LLM Judge Scores.
"""

from __future__ import annotations
import math
import random
from typing import Dict, List, Optional, Any
from app.runtime.ai_operations.models.schemas import MetricScore, EvaluationResult


class EvaluationMetricsCalculator:
    """Calculates granular evaluation metrics and composite quality indices."""

    @staticmethod
    def calculate_grounding_score(facts_stated: List[str], facts_supported: List[str]) -> float:
        if not facts_stated:
            return 1.0
        return max(0.0, min(1.0, len(facts_supported) / len(facts_stated)))

    @staticmethod
    def calculate_hallucination_index(grounding_score: float) -> float:
        return max(0.0, min(1.0, 1.0 - grounding_score))

    @staticmethod
    def calculate_tool_efficiency(tool_calls_count: int, expected_min_calls: int = 1) -> float:
        if tool_calls_count <= 0:
            return 1.0
        if tool_calls_count <= expected_min_calls:
            return 1.0
        # Exponential penalty for excessive/redundant tool calls
        penalty = (tool_calls_count - expected_min_calls) * 0.15
        return max(0.2, 1.0 - penalty)

    @staticmethod
    def calculate_cost_efficiency(tokens_used: int, max_budget_tokens: int = 4000) -> float:
        if tokens_used <= 0:
            return 1.0
        ratio = tokens_used / max(1, max_budget_tokens)
        if ratio <= 0.5:
            return 1.0
        elif ratio <= 1.0:
            return 0.9
        else:
            return max(0.1, 1.0 - (ratio - 1.0) * 0.5)

    @staticmethod
    def calculate_composite_score(
        task_success: float,
        accuracy: float,
        grounding: float,
        safety: float,
        tool_efficiency: float,
        llm_judge: float,
    ) -> float:
        # Weighted composite score
        composite = (
            (task_success * 0.25)
            + (accuracy * 0.20)
            + (grounding * 0.20)
            + (safety * 0.15)
            + (tool_efficiency * 0.10)
            + (llm_judge * 0.10)
        )
        return round(max(0.0, min(1.0, composite)), 4)
