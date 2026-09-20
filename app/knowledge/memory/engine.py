"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Memory Intelligence Platform.
Distinct from Knowledge ("What exists"), Memory tracks "What happened" across 8 multi-tiered stores.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
import logging
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MemoryTier(str, Enum):
    """Eight distinct enterprise memory storage tiers."""
    WORKING = "WORKING"            # In-flight task memory
    SHORT_TERM = "SHORT_TERM"      # Session context
    EPISODIC = "EPISODIC"          # Past executions and run events
    SEMANTIC = "SEMANTIC"          # Distilled domain concepts
    PROCEDURAL = "PROCEDURAL"      # Playbooks, recipes, execution patterns
    ORGANIZATION = "ORGANIZATION"  # Company policies and workspace rules
    WORKFLOW = "WORKFLOW"          # Workflow execution state
    AGENT = "AGENT"                # Agent identity and past decisions


class MemoryItem(BaseModel):
    """Atomic memory unit stored within a memory tier."""
    id: str
    tier: MemoryTier
    key: str
    value: Any
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    access_count: int = 0
    importance_score: float = 0.5
    ttl_seconds: Optional[int] = None
    expires_at: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemoryIntelligencePlatform:
    """
    Unified memory platform managing short-term session state, long-term episodic traces,
    and organizational memory across 8 partitioned tiers.
    """

    def __init__(self):
        # tier -> {key -> MemoryItem}
        self._stores: Dict[MemoryTier, Dict[str, MemoryItem]] = {tier: {} for tier in MemoryTier}

    def store(
        self,
        tier: MemoryTier | str,
        key: str,
        value: Any,
        importance_score: float = 0.5,
        ttl_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryItem:
        """Stores or updates a memory item in the designated tier."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        import uuid

        now = time.time()
        expires = (now + ttl_seconds) if ttl_seconds else None

        item = MemoryItem(
            id=f"mem-{uuid.uuid4().hex[:8]}",
            tier=m_tier,
            key=key,
            value=value,
            importance_score=importance_score,
            ttl_seconds=ttl_seconds,
            expires_at=expires,
            metadata=metadata or {},
        )

        self._stores[m_tier][key] = item
        logger.debug(f"Stored memory item '{key}' in tier '{m_tier.value}'")
        return item

    def retrieve(self, tier: MemoryTier | str, key: str) -> Optional[Any]:
        """Retrieves and updates access telemetry for a memory item."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        item = self._stores[m_tier].get(key)

        if not item:
            return None

        # Check expiration
        if item.expires_at and time.time() > item.expires_at:
            del self._stores[m_tier][key]
            return None

        item.access_count += 1
        item.updated_at = datetime.now(timezone.utc)
        return item.value

    def get_item(self, tier: MemoryTier | str, key: str) -> Optional[MemoryItem]:
        """Returns the full MemoryItem descriptor."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        return self._stores[m_tier].get(key)

    def forget(self, tier: MemoryTier | str, key: str) -> bool:
        """Removes a memory item from a tier."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        if key in self._stores[m_tier]:
            del self._stores[m_tier][key]
            return True
        return False

    def promote(self, from_tier: MemoryTier | str, to_tier: MemoryTier | str, key: str) -> Optional[MemoryItem]:
        """Promotes a memory item from one tier (e.g. WORKING) to another (e.g. EPISODIC)."""
        f_tier = from_tier if isinstance(from_tier, MemoryTier) else MemoryTier(from_tier)
        t_tier = to_tier if isinstance(to_tier, MemoryTier) else MemoryTier(to_tier)

        item = self._stores[f_tier].pop(key, None)
        if not item:
            return None

        item.tier = t_tier
        item.importance_score = min(1.0, item.importance_score + 0.2)
        item.updated_at = datetime.now(timezone.utc)
        self._stores[t_tier][key] = item
        logger.info(f"Promoted memory '{key}' from {f_tier.value} to {t_tier.value}")
        return item

    def list_tier(self, tier: MemoryTier | str) -> List[MemoryItem]:
        """Returns all non-expired items in a memory tier."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        now = time.time()
        active: List[MemoryItem] = []
        expired_keys: List[str] = []

        for k, item in self._stores[m_tier].items():
            if item.expires_at and now > item.expires_at:
                expired_keys.append(k)
            else:
                active.append(item)

        for k in expired_keys:
            del self._stores[m_tier][k]

        return active
