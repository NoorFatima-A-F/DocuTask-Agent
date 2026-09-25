"""
Cognitive Memory Evolution Engine for Enterprise AAOS.
Implements temporal memory decay, confidence recalibration, semantic deduplication,
contradiction detection across facts, and cross-session knowledge consolidation.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from app.agents.memory.intelligence.semantic_memory import SemanticFact, SemanticMemory

logger = logging.getLogger(__name__)


@dataclass
class ContradictionReport:
    """Audit report for detected cognitive contradictions between memory facts."""

    fact_a_id: str
    fact_b_id: str
    subject: str
    predicate: str
    value_a: Any
    value_b: Any
    confidence_a: float
    confidence_b: float
    resolution_applied: str  # "PREFER_HIGHER_CONFIDENCE", "PREFER_NEWER", "FLAG_FOR_REVIEW"
    resolved_value: Any


@dataclass
class MemoryRecalibrationSummary:
    """Outcome of a memory maintenance and evolution cycle."""

    decayed_facts_count: int = 0
    contradictions_detected: List[ContradictionReport] = field(default_factory=list)
    deduplicated_count: int = 0
    compressed_count: int = 0
    cycle_duration_ms: float = 0.0


class CognitiveMemoryEvolutionEngine:
    """
    Advanced memory maintenance engine for autonomous agents.
    Ensures memory store does not become stale, contradictory, or bloated over time.
    """

    def __init__(
        self,
        decay_half_life_days: float = 30.0,
        min_retention_confidence: float = 0.20,
        contradiction_threshold: float = 0.15,
    ) -> None:
        self.decay_lambda = math.log(2.0) / (decay_half_life_days * 86400.0)
        self.min_retention_confidence = min_retention_confidence
        self.contradiction_threshold = contradiction_threshold
        self.history: List[MemoryRecalibrationSummary] = []

    def apply_temporal_decay(self, semantic_memory: SemanticMemory, current_time: Optional[float] = None) -> int:
        """
        Applies exponential temporal decay to non-ground-truth facts:
        C(t) = C_0 * e^(-lambda * dt)
        Facts with confidence=1.0 (verified ground truth/HITL) are exempt.
        """
        now = current_time or time.time()
        decayed_count = 0
        facts_to_remove: List[str] = []

        for fact_id, fact in list(semantic_memory._facts.items()):
            # Ground truth / HITL verified facts (confidence >= 0.999) do not decay
            if fact.confidence >= 0.999:
                continue

            dt = max(0.0, now - fact.created_at)
            decay_factor = math.exp(-self.decay_lambda * dt)
            new_confidence = fact.confidence * decay_factor

            if new_confidence < self.min_retention_confidence:
                facts_to_remove.append(fact_id)
            else:
                if abs(fact.confidence - new_confidence) > 0.001:
                    fact.confidence = round(new_confidence, 4)
                    decayed_count += 1

        for fid in facts_to_remove:
            del semantic_memory._facts[fid]
            logger.debug("Pruned decayed fact %s below retention threshold", fid)

        return decayed_count

    def detect_and_resolve_contradictions(self, semantic_memory: SemanticMemory) -> List[ContradictionReport]:
        """
        Detects conflicting facts sharing the same (subject, predicate) tuple
        with different values, and automatically resolves them.
        """
        reports: List[ContradictionReport] = []
        fact_groups: Dict[Tuple[str, str], List[SemanticFact]] = {}

        for fact in semantic_memory._facts.values():
            key = (fact.subject.strip().lower(), fact.predicate.strip().lower())
            if key not in fact_groups:
                fact_groups[key] = []
            fact_groups[key].append(fact)

        for (subj, pred), group in fact_groups.items():
            if len(group) <= 1:
                continue

            # Compare all pairs in group
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    fa, fb = group[i], group[j]
                    if fa.fact_value != fb.fact_value:
                        # Contradiction detected
                        if fa.confidence > fb.confidence + self.contradiction_threshold:
                            resolution = "PREFER_HIGHER_CONFIDENCE"
                            resolved_val = fa.fact_value
                            # Demote or remove lower confidence fact
                            fb.confidence = max(0.0, fb.confidence * 0.5)
                        elif fb.confidence > fa.confidence + self.contradiction_threshold:
                            resolution = "PREFER_HIGHER_CONFIDENCE"
                            resolved_val = fb.fact_value
                            fa.confidence = max(0.0, fa.confidence * 0.5)
                        else:
                            # Prefer newer fact if confidence is comparable
                            if fa.created_at >= fb.created_at:
                                resolution = "PREFER_NEWER"
                                resolved_val = fa.fact_value
                                fb.confidence = max(0.0, fb.confidence * 0.5)
                            else:
                                resolution = "PREFER_NEWER"
                                resolved_val = fb.fact_value
                                fa.confidence = max(0.0, fa.confidence * 0.5)

                        report = ContradictionReport(
                            fact_a_id=fa.fact_id,
                            fact_b_id=fb.fact_id,
                            subject=subj,
                            predicate=pred,
                            value_a=fa.fact_value,
                            value_b=fb.fact_value,
                            confidence_a=fa.confidence,
                            confidence_b=fb.confidence,
                            resolution_applied=resolution,
                            resolved_value=resolved_val,
                        )
                        reports.append(report)
                        logger.warning(
                            "Contradiction resolved for (%s, %s): %s -> %s",
                            subj,
                            pred,
                            resolution,
                            resolved_val,
                        )

        return reports

    def deduplicate_facts(self, semantic_memory: SemanticMemory) -> int:
        """Merges duplicate facts that have identical subject, predicate, and value."""
        seen: Dict[Tuple[str, str, str], SemanticFact] = {}
        duplicates_removed = 0
        to_delete: List[str] = []

        for fid, fact in semantic_memory._facts.items():
            key = (fact.subject.strip().lower(), fact.predicate.strip().lower(), str(fact.fact_value).strip().lower())
            if key in seen:
                existing = seen[key]
                # Merge tags and take maximum confidence
                existing.confidence = max(existing.confidence, fact.confidence)
                existing.importance = max(existing.importance, fact.importance)
                merged_tags = list(set(existing.tags + fact.tags))
                existing.tags = merged_tags
                to_delete.append(fid)
                duplicates_removed += 1
            else:
                seen[key] = fact

        for fid in to_delete:
            del semantic_memory._facts[fid]

        return duplicates_removed

    def run_evolution_cycle(
        self,
        semantic_memory: SemanticMemory,
        current_time: Optional[float] = None,
    ) -> MemoryRecalibrationSummary:
        """Executes full maintenance and cognitive evolution cycle."""
        start = time.perf_counter()

        dedup_count = self.deduplicate_facts(semantic_memory)
        contra_reports = self.detect_and_resolve_contradictions(semantic_memory)
        decay_count = self.apply_temporal_decay(semantic_memory, current_time)

        duration = (time.perf_counter() - start) * 1000.0

        summary = MemoryRecalibrationSummary(
            decayed_facts_count=decay_count,
            contradictions_detected=contra_reports,
            deduplicated_count=dedup_count,
            compressed_count=dedup_count + len(contra_reports),
            cycle_duration_ms=duration,
        )
        self.history.append(summary)
        logger.info(
            "Memory Evolution Cycle completed in %.2fms: %d deduped, %d contradictions resolved, %d decayed",
            duration,
            dedup_count,
            len(contra_reports),
            decay_count,
        )
        return summary
