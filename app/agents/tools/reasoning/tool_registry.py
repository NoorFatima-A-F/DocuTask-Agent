"""Tool Reasoning Registry for Autonomous Agent OS.

Maintains registered tools, default implementations, and modality-based indexes.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from app.agents.tools.reasoning.tool_definition import Modality, ToolDefinition

logger = logging.getLogger(__name__)


class ToolReasoningRegistry:
    """Central registry cataloging tools for multimodal reasoning selection."""

    def __init__(self) -> None:
        self._tools: Dict[str, ToolDefinition] = {}
        self._register_defaults()

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.tool_id] = tool
        logger.info("Registered reasoning tool: %s (%s)", tool.tool_id, tool.category)

    def get(self, tool_id: str) -> Optional[ToolDefinition]:
        return self._tools.get(tool_id)

    def list_all(self) -> List[ToolDefinition]:
        return list(self._tools.values())

    def find_by_category(self, category: str) -> List[ToolDefinition]:
        return [t for t in self._tools.values() if t.category.upper() == category.upper()]

    def find_by_modality(self, modality: Modality) -> List[ToolDefinition]:
        return [t for t in self._tools.values() if t.supports_modality(modality)]

    def _register_defaults(self) -> None:
        # Default OCR tools
        self.register(
            ToolDefinition(
                tool_id="tool_tesseract_ocr",
                name="Tesseract Local OCR",
                category="OCR",
                description="Fast lightweight local OCR for clean printed documents",
                supported_modalities=[Modality.IMAGE, Modality.PDF, Modality.TEXT],
                cost_per_call=0.0001,
                latency_ms_avg=100.0,
                accuracy_score=0.91,
            )
        )
        self.register(
            ToolDefinition(
                tool_id="tool_gemini_vision",
                name="Gemini Multimodal Vision",
                category="OCR",
                description="State-of-the-art vision LLM for complex tables, degraded scans, and handwriting",
                supported_modalities=[Modality.IMAGE, Modality.PDF, Modality.HANDWRITING, Modality.TABLE],
                cost_per_call=0.0025,
                latency_ms_avg=350.0,
                accuracy_score=0.992,
            )
        )

        # Default Extraction tools
        self.register(
            ToolDefinition(
                tool_id="tool_regex_extractor",
                name="Deterministic Pattern Extractor",
                category="EXTRACTION",
                description="Sub-millisecond regex entity extraction for standard invoice templates",
                supported_modalities=[Modality.TEXT, Modality.JSON],
                cost_per_call=0.0,
                latency_ms_avg=2.0,
                accuracy_score=0.88,
            )
        )
        self.register(
            ToolDefinition(
                tool_id="tool_llm_json_extractor",
                name="LLM Structured JSON Extractor",
                category="EXTRACTION",
                description="Zero-shot LLM structured extraction conforming to JSON schemas",
                supported_modalities=[Modality.TEXT, Modality.JSON, Modality.TABLE],
                cost_per_call=0.0015,
                latency_ms_avg=220.0,
                accuracy_score=0.985,
            )
        )

        # Default Validation tools
        self.register(
            ToolDefinition(
                tool_id="tool_math_verifier",
                name="Financial Arithmetic Verifier",
                category="VALIDATION",
                description="100% precise arithmetic verification for invoices, subtotals, and taxes",
                supported_modalities=[Modality.JSON, Modality.TABLE],
                cost_per_call=0.0,
                latency_ms_avg=1.0,
                accuracy_score=1.0,
            )
        )
        self.register(
            ToolDefinition(
                tool_id="tool_compliance_evaluator",
                name="Regulatory Rules Evaluator",
                category="COMPLIANCE",
                description="Evaluates document fields against SOX, GDPR, and enterprise policies",
                supported_modalities=[Modality.JSON, Modality.TEXT],
                cost_per_call=0.0005,
                latency_ms_avg=20.0,
                accuracy_score=0.99,
            )
        )
