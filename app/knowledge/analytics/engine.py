"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Knowledge Analytics.
Provides operational metrics, query volume tracking, retrieval latency percentiles, and knowledge gap detection.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class KnowledgeAnalyticsReport(BaseModel):
    """Aggregated analytical report on platform knowledge usage and search effectiveness."""
    total_queries: int = 0
    successful_queries: int = 0
    zero_hit_queries: int = 0
    avg_latency_ms: float = 0.0
    total_chunks_indexed: int = 0
    knowledge_gaps: List[str] = Field(default_factory=list)
    top_queried_terms: List[Dict[str, Any]] = Field(default_factory=list)


class KnowledgeAnalytics:
    """
    Central telemetry collector and gap analysis engine for knowledge operations.
    """

    def __init__(self):
        self._total_queries = 0
        self._successful_queries = 0
        self._zero_hit_queries = 0
        self._latencies: List[float] = []
        self._knowledge_gaps: Dict[str, int] = {}  # query_text -> count
        self._query_frequencies: Dict[str, int] = {}
        self._total_chunks = 0

    def record_query(self, query: str, results_count: int, latency_ms: float) -> None:
        """Records a search query event and its outcome."""
        self._total_queries += 1
        self._latencies.append(latency_ms)
        if len(self._latencies) > 200:
            self._latencies.pop(0)

        # Track query term frequency
        self._query_frequencies[query] = self._query_frequencies.get(query, 0) + 1

        if results_count > 0:
            self._successful_queries += 1
        else:
            self._zero_hit_queries += 1
            self._knowledge_gaps[query] = self._knowledge_gaps.get(query, 0) + 1

    def record_indexed_chunks(self, count: int) -> None:
        """Increments indexed chunk counter."""
        self._total_chunks += count

    def generate_report(self) -> KnowledgeAnalyticsReport:
        """Generates operational metrics report."""
        avg_lat = sum(self._latencies) / len(self._latencies) if self._latencies else 0.0

        # Top gaps (queries with 0 results)
        gaps = sorted(
            self._knowledge_gaps.keys(),
            key=lambda q: self._knowledge_gaps[q],
            reverse=True,
        )[:10]

        # Top terms
        top_terms = sorted(
            [{"query": q, "count": c} for q, c in self._query_frequencies.items()],
            key=lambda x: x["count"],
            reverse=True,
        )[:10]

        return KnowledgeAnalyticsReport(
            total_queries=self._total_queries,
            successful_queries=self._successful_queries,
            zero_hit_queries=self._zero_hit_queries,
            avg_latency_ms=avg_lat,
            total_chunks_indexed=self._total_chunks,
            knowledge_gaps=gaps,
            top_queried_terms=top_terms,
        )
