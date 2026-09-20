"""
Consolidation Agent for Memory Consolidation Intelligence.
Coordinates episodic mining, rule distillation, and semantic memory promotion,
powering continuous agent learning across batches of document processing executions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.agents.memory.consolidation.knowledge_extractor import KnowledgeExtractor
from app.agents.memory.consolidation.memory_promoter import MemoryPromoter
from app.agents.memory.consolidation.pattern_miner import PatternMiner
from app.agents.memory.intelligence.episodic_memory import EpisodicMemory
from app.agents.memory.intelligence.semantic_memory import SemanticFact, SemanticMemory

logger = logging.getLogger(__name__)


@dataclass
class ConsolidationCycleReport:
    """Summary of a single memory consolidation cycle."""

    cycle_id: str
    episodes_analyzed: int
    patterns_mined: int
    rules_extracted: int
    facts_promoted: int
    promoted_fact_ids: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "episodes_analyzed": self.episodes_analyzed,
            "patterns_mined": self.patterns_mined,
            "rules_extracted": self.rules_extracted,
            "facts_promoted": self.facts_promoted,
            "promoted_fact_ids": self.promoted_fact_ids,
            "timestamp": self.timestamp.isoformat(),
        }


class MemoryConsolidationAgent:
    """Autonomous background service consolidating episodic traces into long-term domain facts."""

    def __init__(
        self,
        episodic_memory: EpisodicMemory,
        semantic_memory: SemanticMemory,
        pattern_miner: Optional[PatternMiner] = None,
        knowledge_extractor: Optional[KnowledgeExtractor] = None,
        memory_promoter: Optional[MemoryPromoter] = None,
    ) -> None:
        self.episodic_memory = episodic_memory
        self.semantic_memory = semantic_memory
        self.pattern_miner = pattern_miner or PatternMiner(min_support=2)
        self.knowledge_extractor = knowledge_extractor or KnowledgeExtractor()
        self.memory_promoter = memory_promoter or MemoryPromoter(semantic_memory=semantic_memory)
        self._cycle_history: List[ConsolidationCycleReport] = []

    def run_consolidation(self, cycle_id: str = "") -> ConsolidationCycleReport:
        """Executes a full consolidation pass across all recorded episodes."""
        all_episodes = list(self.episodic_memory._episodes.values())
        cid = cycle_id or f"cycle_{len(self._cycle_history) + 1}"

        # 1. Mine patterns
        patterns = self.pattern_miner.mine_patterns(all_episodes)

        # 2. Extract declarative rules
        rules = self.knowledge_extractor.extract_rules(patterns)

        # 3. Promote to SemanticMemory
        promoted = self.memory_promoter.promote_rules(rules)

        report = ConsolidationCycleReport(
            cycle_id=cid,
            episodes_analyzed=len(all_episodes),
            patterns_mined=len(patterns),
            rules_extracted=len(rules),
            facts_promoted=len(promoted),
            promoted_fact_ids=[f.fact_id for f in promoted],
        )

        self._cycle_history.append(report)
        logger.info(
            "Consolidation cycle '%s' complete: %d episodes -> %d patterns -> %d rules -> %d facts promoted",
            cid,
            len(all_episodes),
            len(patterns),
            len(rules),
            len(promoted),
        )
        return report

    def get_history(self) -> List[ConsolidationCycleReport]:
        return list(self._cycle_history)
