"""
Knowledge Extractor for Memory Consolidation Intelligence.
Transforms raw mined patterns into actionable domain rules, vendor layout hints, and schema constraints.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, List

from app.agents.memory.consolidation.pattern_miner import MinedPattern

logger = logging.getLogger(__name__)


@dataclass
class ExtractedKnowledgeRule:
    """A clean, structured domain heuristic distilled from execution experience."""

    rule_id: str
    subject: str
    predicate: str
    rule_value: Any
    confidence: float
    importance: float = 0.8
    source_pattern_id: str = ""
    domain: str = "FINANCIAL"
    tags: List[str] = field(default_factory=list)


class KnowledgeExtractor:
    """Extracts formal declarative knowledge rules from discovered patterns."""

    def extract_rules(self, patterns: List[MinedPattern]) -> List[ExtractedKnowledgeRule]:
        """Synthesizes structured knowledge rules from mined patterns."""
        rules: List[ExtractedKnowledgeRule] = []

        for p in patterns:
            if p.pattern_type == "VENDOR_HEURISTIC":
                vendor = p.attributes.get("vendor", "GenericVendor")
                rule = ExtractedKnowledgeRule(
                    rule_id=f"rule_{p.pattern_id}",
                    subject=vendor,
                    predicate="layout_special_case",
                    rule_value={
                        "description": p.description,
                        "preferred_engine": "hybrid_ocr_llm",
                        "custom_regex": True,
                    },
                    confidence=p.confidence,
                    importance=0.85,
                    source_pattern_id=p.pattern_id,
                    domain="DOCUMENT_LAYOUT",
                    tags=["vendor", "layout_hint", vendor.lower()],
                )
                rules.append(rule)

            elif p.pattern_type == "TOOL_INEFFICIENCY":
                tool = p.attributes.get("tool", "unknown_tool")
                task = p.attributes.get("task", "unknown_task")
                rule = ExtractedKnowledgeRule(
                    rule_id=f"rule_{p.pattern_id}",
                    subject=tool,
                    predicate="avoid_on_task",
                    rule_value={
                        "task": task,
                        "reason": p.description,
                        "recommended_fallback": "vision_llm",
                    },
                    confidence=p.confidence,
                    importance=0.9,
                    source_pattern_id=p.pattern_id,
                    domain="TOOL_GOVERNANCE",
                    tags=["tool_rule", tool.lower(), "avoid"],
                )
                rules.append(rule)

            elif p.pattern_type == "FAILURE_CORRELATION":
                rule = ExtractedKnowledgeRule(
                    rule_id=f"rule_{p.pattern_id}",
                    subject="RecoveryPattern",
                    predicate="auto_correction_trajectory",
                    rule_value={
                        "notes": p.attributes.get("notes", ""),
                        "frequency": p.frequency,
                    },
                    confidence=p.confidence,
                    importance=0.75,
                    source_pattern_id=p.pattern_id,
                    domain="RECOVERY",
                    tags=["recovery", "self_correction"],
                )
                rules.append(rule)

        logger.info("KnowledgeExtractor: Distilled %d formal rules from %d patterns", len(rules), len(patterns))
        return rules
