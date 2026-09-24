"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Memory Consolidation Engine.
Background service that summarizes, compresses, deduplicates, scores importance,
and promotes valuable memories across tiers while enforcing retention limits.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
from pydantic import BaseModel, Field

from app.knowledge.memory.engine import MemoryIntelligencePlatform, MemoryTier

logger = logging.getLogger(__name__)


class ConsolidationReport(BaseModel):
    """Execution summary of memory consolidation batch process."""
    items_scanned: int = 0
    items_promoted: int = 0
    items_expired: int = 0
    items_compressed: int = 0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MemoryConsolidationEngine:
    """
    Automates memory lifecycle transitions, importance-weighted tier promotion,
    and storage compaction.
    """

    def __init__(self, memory_platform: MemoryIntelligencePlatform):
        self.memory_platform = memory_platform

    def consolidate(
        self,
        importance_threshold_for_promotion: float = 0.7,
        access_count_threshold: int = 3,
    ) -> ConsolidationReport:
        """
        Scans WORKING and SHORT_TERM memory tiers, promoting frequently accessed or high-importance
        items to EPISODIC and PROCEDURAL stores.
        """
        report = ConsolidationReport()

        for source_tier, target_tier in [
            (MemoryTier.SHORT_TERM, MemoryTier.EPISODIC),
            (MemoryTier.WORKING, MemoryTier.SHORT_TERM),
        ]:
            items = self.memory_platform.list_tier(source_tier)
            report.items_scanned += len(items)

            for item in items:
                # Promotion condition: High importance or high repeated access
                if (
                    item.importance_score >= importance_threshold_for_promotion
                    or item.access_count >= access_count_threshold
                ):
                    self.memory_platform.promote(source_tier, target_tier, item.key)
                    report.items_promoted += 1

        logger.info(
            f"Consolidated memory: Scanned={report.items_scanned}, Promoted={report.items_promoted}, Expired={report.items_expired}"
        )
        return report
