"""Tool Selector Engine for Autonomous Tool Reasoning.

Reasoning engine that selects the best tool for an operation by assessing
document modality, degradation level, handwriting, table complexity, and SLA/cost goals.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.agents.tools.reasoning.tool_definition import Modality, ToolDefinition
from app.agents.tools.reasoning.tool_registry import ToolReasoningRegistry

logger = logging.getLogger(__name__)


@dataclass
class ToolSelectionResult:
    """Outcome of tool selection reasoning with detailed justification."""

    selected_tool: ToolDefinition
    selection_score: float
    reasoning: str
    fallback_tool: Optional[ToolDefinition] = None
    evaluated_candidates: List[str] = field(default_factory=list)


class ToolSelector:
    """Reasoning engine dynamically matching tools to document contexts."""

    def __init__(self, registry: ToolReasoningRegistry) -> None:
        self.registry = registry

    def select_tool(
        self,
        category: str,
        document_modality: Modality = Modality.IMAGE,
        has_handwriting: bool = False,
        has_complex_tables: bool = False,
        min_accuracy: float = 0.90,
        cost_sensitive: bool = False,
        max_latency_ms: Optional[float] = None,
    ) -> ToolSelectionResult:
        """Select the most suitable tool via multi-factor reasoning."""
        candidates = self.registry.find_by_category(category)
        if not candidates:
            raise KeyError(f"No tools registered for category: {category}")

        # Filter by modality support
        eligible: List[ToolDefinition] = []
        for cand in candidates:
            if cand.supports_modality(document_modality):
                eligible.append(cand)

        if not eligible:
            eligible = candidates  # Fallback to category candidates

        # If handwriting or complex tables, require multimodal vision
        if has_handwriting or has_complex_tables:
            vision_tools = [
                t for t in eligible
                if t.supports_modality(Modality.HANDWRITING) or t.supports_modality(Modality.TABLE)
            ]
            if vision_tools:
                eligible = vision_tools

        candidate_ids = [t.tool_id for t in eligible]

        effective_min_acc = 0.80 if cost_sensitive and min_accuracy == 0.90 else min_accuracy

        # Multi-factor utility function
        def evaluate_tool(tool: ToolDefinition) -> float:
            score = tool.accuracy_score * 50.0

            # Penalty if below requested min_accuracy
            if tool.accuracy_score < effective_min_acc:
                score -= 35.0

            # Cost penalty if cost sensitive: 25%
            if cost_sensitive:
                cost_score = max(0.0, 25.0 - (tool.cost_per_call * 5000.0))
            else:
                cost_score = max(0.0, 15.0 - (tool.cost_per_call * 1000.0))
            score += cost_score

            # Latency score: 25%
            if max_latency_ms and tool.latency_ms_avg > max_latency_ms:
                score -= 30.0  # Heavy penalty for SLA violation
            lat_score = max(0.0, 25.0 - (tool.latency_ms_avg / 20.0))
            score += lat_score

            return score

        sorted_tools = sorted(eligible, key=evaluate_tool, reverse=True)
        top_tool = sorted_tools[0]
        fallback = sorted_tools[1] if len(sorted_tools) > 1 else None

        reasoning_parts: List[str] = [
            f"Selected {top_tool.name} ({top_tool.tool_id}) for category {category}.",
            f"Modality: {document_modality.value}.",
        ]
        if has_handwriting:
            reasoning_parts.append("Document exhibits handwriting; specialized vision model prioritized.")
        if has_complex_tables:
            reasoning_parts.append("Complex tabular structure detected; tabular-aware tool chosen.")
        if top_tool.accuracy_score >= min_accuracy:
            reasoning_parts.append(f"Satisfies target accuracy ({top_tool.accuracy_score:.2f} >= {min_accuracy:.2f}).")
        if fallback:
            reasoning_parts.append(f"Configured fallback tool: {fallback.name} ({fallback.tool_id}).")

        return ToolSelectionResult(
            selected_tool=top_tool,
            selection_score=round(evaluate_tool(top_tool), 2),
            reasoning=" ".join(reasoning_parts),
            fallback_tool=fallback,
            evaluated_candidates=candidate_ids,
        )
