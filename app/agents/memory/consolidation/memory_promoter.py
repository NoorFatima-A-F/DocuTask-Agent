"""
Memory Promoter for Memory Consolidation Intelligence.
Promotes high-confidence distilled knowledge rules into permanent Semantic Memory facts.
"""

from __future__ import annotations

import logging
from typing import List, Optional

from app.agents.memory.consolidation.knowledge_extractor import ExtractedKnowledgeRule
from app.agents.memory.intelligence.semantic_memory import SemanticFact, SemanticMemory

logger = logging.getLogger(__name__)


class MemoryPromoter:
    """Promotes extracted declarative rules into permanent semantic memory facts."""

    def __init__(
        self,
        semantic_memory: SemanticMemory,
        min_promotion_confidence: float = 0.65,
    ) -> None:
        self.semantic_memory = semantic_memory
        self.min_promotion_confidence = min_promotion_confidence

    def promote_rules(self, rules: List[ExtractedKnowledgeRule]) -> List[SemanticFact]:
        """Filters rules by confidence threshold and stores them as permanent SemanticFacts."""
        promoted_facts: List[SemanticFact] = []

        for r in rules:
            if r.confidence >= self.min_promotion_confidence:
                fact = SemanticFact(
                    subject=r.subject,
                    predicate=r.predicate,
                    fact_value=r.rule_value,
                    domain=r.domain,
                    confidence=r.confidence,
                    importance=r.importance,
                    tags=list(r.tags) + ["consolidated", "auto_promoted"],
                    metadata={"source_rule_id": r.rule_id, "source_pattern_id": r.source_pattern_id},
                )
                self.semantic_memory.store_fact(fact)
                promoted_facts.append(fact)
                logger.info(
                    "MemoryPromoter: Promoted rule %s ('%s %s') to SemanticFact %s (conf: %.2f)",
                    r.rule_id,
                    r.subject,
                    r.predicate,
                    fact.fact_id,
                    r.confidence,
                )
            else:
                logger.debug(
                    "MemoryPromoter: Skipped rule %s (confidence %.2f < threshold %.2f)",
                    r.rule_id,
                    r.confidence,
                    self.min_promotion_confidence,
                )

        return promoted_facts
