"""
Scientific Memory Consolidation (Phase 84C)
===========================================
Periodically distills episodic traces, failures, and successes into long-term invariants.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

from research_validation.memory.episodic_memory import EpisodicMemoryStore
from research_validation.memory.failure_memory import FailureMemoryStore
from research_validation.memory.success_memory import SuccessMemoryStore
from research_validation.memory.long_term_memory import LongTermMemoryStore


@dataclass(frozen=True)
class ConsolidationReport:
    """Summary of memory consolidation process."""
    episodes_processed: int
    new_invariants_stored: int
    pruned_memories: int
    consolidated_concepts: List[str]


class ScientificMemoryConsolidator:
    """
    Consolidates episodic observations into long-term invariants and prunes obsolete traces.
    """

    def __init__(
        self,
        episodic_store: EpisodicMemoryStore,
        failure_store: FailureMemoryStore,
        success_store: SuccessMemoryStore,
        long_term_store: LongTermMemoryStore,
    ):
        self.episodic_store = episodic_store
        self.failure_store = failure_store
        self.success_store = success_store
        self.long_term_store = long_term_store

    def consolidate(self, current_time: float = None) -> ConsolidationReport:
        """Executes a consolidation pass across memory stores."""
        new_invariants = 0
        concepts: List[str] = []

        # 1. Distill recurrent failures into invariant failure rules
        failure_patterns: Dict[str, int] = {}
        for f in self.failure_store.failures.values():
            cat = f.category.value
            failure_patterns[cat] = failure_patterns.get(cat, 0) + 1

        for cat, count in failure_patterns.items():
            if count >= 2:
                concept = f"FAILURE_RULE_{cat}"
                self.long_term_store.store_invariant(
                    concept=concept,
                    assertion=f"Configuration pattern triggering {cat} should be avoided (observed {count} times).",
                    evidence_weight=min(1.0, 0.5 + count * 0.1),
                    half_life_days=60.0,
                    current_time=current_time,
                )
                new_invariants += 1
                concepts.append(concept)

        # 2. Distill confirmed successes into invariant rules
        for s in self.success_store.successes.values():
            if s.reproducibility_verified and s.confidence_score >= 0.90:
                concept = f"OPTIMAL_CONFIG_{s.experiment_id}"
                self.long_term_store.store_invariant(
                    concept=concept,
                    assertion=f"Verified optimal parameter set with confidence {s.confidence_score:.2f}.",
                    evidence_weight=s.confidence_score,
                    half_life_days=90.0,
                    current_time=current_time,
                )
                new_invariants += 1
                concepts.append(concept)

        # 3. Prune decayed memories
        pruned = self.long_term_store.prune_decayed_memories(current_time)

        return ConsolidationReport(
            episodes_processed=len(self.episodic_store.episodes),
            new_invariants_stored=new_invariants,
            pruned_memories=pruned,
            consolidated_concepts=concepts,
        )
