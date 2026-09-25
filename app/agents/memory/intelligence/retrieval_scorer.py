"""Multi-Factor Memory Retrieval Scoring Engine.

Implements the multi-factor memory retrieval ranking formula:
Score = w1 * Similarity + w2 * Importance + w3 * Recency + w4 * TaskRelevance
"""

from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class RetrievalScoringConfig:
    """Weights and parameters for multi-factor retrieval scoring."""

    w_similarity: float = 0.35
    w_importance: float = 0.25
    w_recency: float = 0.20
    w_task_relevance: float = 0.20
    recency_decay_lambda: float = 0.0001  # half-life parameter in seconds


class RetrievalScorer:
    """Calculates unified memory relevance score."""

    def __init__(self, config: Optional[RetrievalScoringConfig] = None) -> None:
        self.config = config or RetrievalScoringConfig()

    def tokenize(self, text: str) -> Set[str]:
        words = re.findall(r"\w+", text.lower())
        return set(words)

    def compute_similarity(self, query: str, document_text: str) -> float:
        """Token-based Jaccard similarity between query and memory content."""
        q_tokens = self.tokenize(query)
        d_tokens = self.tokenize(document_text)
        if not q_tokens or not d_tokens:
            return 0.0
        intersection = len(q_tokens & d_tokens)
        union = len(q_tokens | d_tokens)
        return intersection / float(union)

    def compute_recency(self, timestamp: float, current_time: Optional[float] = None) -> float:
        """Exponential decay based on age in seconds."""
        now = current_time or time.time()
        delta_seconds = max(0.0, now - timestamp)
        return math.exp(-self.config.recency_decay_lambda * delta_seconds)

    def compute_task_relevance(self, memory_tags: List[str], current_task_tags: List[str]) -> float:
        """Relevance score based on tag overlap with active task."""
        if not memory_tags or not current_task_tags:
            return 0.2  # baseline relevance
        m_set = {t.lower() for t in memory_tags}
        c_set = {t.lower() for t in current_task_tags}
        overlap = len(m_set & c_set)
        return min(1.0, overlap / float(len(c_set)))

    def calculate_score(
        self,
        query: str,
        memory_content: str,
        importance: float,
        timestamp: float,
        memory_tags: List[str],
        current_task_tags: List[str],
        current_time: Optional[float] = None,
    ) -> float:
        """Compute the weighted multi-factor retrieval score."""
        sim = self.compute_similarity(query, memory_content)
        rec = self.compute_recency(timestamp, current_time)
        rel = self.compute_task_relevance(memory_tags, current_task_tags)
        imp = max(0.0, min(1.0, importance))

        score = (
            self.config.w_similarity * sim
            + self.config.w_importance * imp
            + self.config.w_recency * rec
            + self.config.w_task_relevance * rel
        )
        return round(score, 4)
