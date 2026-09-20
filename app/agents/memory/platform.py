"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Enterprise Memory Platform.
Implements the 8-tier hierarchical memory architecture:
1. Working Memory (Execution task scope)
2. Short Term Memory (Active session context)
3. Long Term Memory (Cross-session durable storage)
4. Semantic Memory (Concept, fact, and entity embeddings)
5. Procedural Memory (Learned workflows, routines, tool patterns)
6. Episodic Memory (Historical case studies and experience)
7. Knowledge Memory (Enterprise reference documentation and knowledge base)
8. Organization Memory (Tenant-wide policies, compliance conventions)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
import logging

from app.agents.memory.lifecycle import MemoryLifecycleState

logger = logging.getLogger(__name__)


class MemoryTier(str, Enum):
    """The 8 hierarchical tiers of enterprise agent memory."""
    WORKING = "WORKING"
    SHORT_TERM = "SHORT_TERM"
    LONG_TERM = "LONG_TERM"
    SEMANTIC = "SEMANTIC"
    PROCEDURAL = "PROCEDURAL"
    EPISODIC = "EPISODIC"
    KNOWLEDGE = "KNOWLEDGE"
    ORGANIZATION = "ORGANIZATION"


@dataclass
class EnterpriseMemoryRecord:
    """A governed memory record within the enterprise memory platform."""
    id: str = field(default_factory=lambda: f"mem-{uuid.uuid4().hex[:12]}")
    tier: MemoryTier = MemoryTier.WORKING
    namespace: str = "default"
    key: str = ""
    value: Any = None
    importance: float = 0.5
    access_count: int = 0
    state: MemoryLifecycleState = MemoryLifecycleState.ACTIVE
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tier": self.tier.value if isinstance(self.tier, Enum) else str(self.tier),
            "namespace": self.namespace,
            "key": self.key,
            "value": self.value,
            "importance": self.importance,
            "access_count": self.access_count,
            "state": self.state.value if isinstance(self.state, Enum) else str(self.state),
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }


class EnterpriseMemoryPlatform:
    """
    Unified orchestrator managing all 8 hierarchical memory tiers,
    memory promotion/demotion, consolidation, compression, and lifecycle expiration.
    """

    def __init__(self):
        # Tiered storage: tier -> key -> EnterpriseMemoryRecord
        self._stores: Dict[MemoryTier, Dict[str, EnterpriseMemoryRecord]] = {
            t: {} for t in MemoryTier
        }

    def store(
        self,
        key: str,
        value: Any,
        tier: MemoryTier | str = MemoryTier.WORKING,
        namespace: str = "default",
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
        expires_at: Optional[datetime] = None,
    ) -> EnterpriseMemoryRecord:
        """Stores a record in the specified memory tier."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        record = EnterpriseMemoryRecord(
            id=f"mem-{uuid.uuid4().hex[:12]}",
            tier=m_tier,
            namespace=namespace,
            key=key,
            value=value,
            importance=importance,
            state=MemoryLifecycleState.ACTIVE,
            metadata=metadata or {},
            expires_at=expires_at,
        )
        self._stores[m_tier][key] = record
        logger.info(f"Stored record '{key}' in memory tier {m_tier.value} [Namespace: {namespace}]")
        return record

    def retrieve(
        self,
        key: str,
        tier: Optional[MemoryTier | str] = None,
        namespace: Optional[str] = None
    ) -> Optional[EnterpriseMemoryRecord]:
        """
        Retrieves a record by key, searching across the specified tier or
        hierarchically from WORKING up to ORGANIZATION.
        """
        if tier:
            m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
            record = self._stores[m_tier].get(key)
            if record and record.state not in [MemoryLifecycleState.DELETED, MemoryLifecycleState.EXPIRED]:
                record.access_count += 1
                record.updated_at = datetime.now(timezone.utc)
                return record
            return None

        # Hierarchical lookup order
        lookup_order = [
            MemoryTier.WORKING,
            MemoryTier.SHORT_TERM,
            MemoryTier.EPISODIC,
            MemoryTier.SEMANTIC,
            MemoryTier.PROCEDURAL,
            MemoryTier.LONG_TERM,
            MemoryTier.KNOWLEDGE,
            MemoryTier.ORGANIZATION,
        ]
        for t in lookup_order:
            record = self._stores[t].get(key)
            if record and record.state not in [MemoryLifecycleState.DELETED, MemoryLifecycleState.EXPIRED]:
                if namespace and record.namespace != namespace:
                    continue
                record.access_count += 1
                record.updated_at = datetime.now(timezone.utc)
                return record

        return None

    def search(
        self,
        query: str,
        tier: Optional[MemoryTier | str] = None,
        namespace: Optional[str] = None,
        limit: int = 10
    ) -> List[EnterpriseMemoryRecord]:
        """Performs search across memory tiers."""
        results: List[EnterpriseMemoryRecord] = []
        q_lower = query.lower()

        tiers_to_search = [tier if isinstance(tier, MemoryTier) else MemoryTier(tier)] if tier else list(MemoryTier)

        for t in tiers_to_search:
            for rec in self._stores[t].values():
                if rec.state in [MemoryLifecycleState.DELETED, MemoryLifecycleState.EXPIRED]:
                    continue
                if namespace and rec.namespace != namespace:
                    continue
                # Simple keyword search on key, value, metadata
                content_str = f"{rec.key} {str(rec.value)} {str(rec.metadata)}".lower()
                if q_lower in content_str:
                    results.append(rec)

        # Sort by importance and access count
        results.sort(key=lambda r: (r.importance, r.access_count), reverse=True)
        return results[:limit]

    def promote(self, key: str, from_tier: MemoryTier | str, to_tier: MemoryTier | str) -> Optional[EnterpriseMemoryRecord]:
        """Promotes a memory record from a lower tier (e.g. WORKING) to a higher tier (e.g. LONG_TERM)."""
        f_tier = from_tier if isinstance(from_tier, MemoryTier) else MemoryTier(from_tier)
        t_tier = to_tier if isinstance(to_tier, MemoryTier) else MemoryTier(to_tier)

        record = self._stores[f_tier].pop(key, None)
        if not record:
            return None

        record.tier = t_tier
        record.state = MemoryLifecycleState.PROMOTED
        record.importance = min(1.0, record.importance + 0.2)
        record.updated_at = datetime.now(timezone.utc)
        self._stores[t_tier][key] = record

        logger.info(f"Promoted memory '{key}': {f_tier.value} -> {t_tier.value}")
        return record

    def demote(self, key: str, from_tier: MemoryTier | str, to_tier: MemoryTier | str) -> Optional[EnterpriseMemoryRecord]:
        """Demotes a memory record to a lower tier or marks it summarized."""
        f_tier = from_tier if isinstance(from_tier, MemoryTier) else MemoryTier(from_tier)
        t_tier = to_tier if isinstance(to_tier, MemoryTier) else MemoryTier(to_tier)

        record = self._stores[f_tier].pop(key, None)
        if not record:
            return None

        record.tier = t_tier
        record.state = MemoryLifecycleState.DEMOTED
        record.importance = max(0.0, record.importance - 0.2)
        record.updated_at = datetime.now(timezone.utc)
        self._stores[t_tier][key] = record

        logger.info(f"Demoted memory '{key}': {f_tier.value} -> {t_tier.value}")
        return record

    def compress(self, tier: MemoryTier | str, max_items: int = 50) -> int:
        """Compresses / summarizes low-importance records in a given tier."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        store = self._stores[m_tier]
        if len(store) <= max_items:
            return 0

        # Sort by importance ascending
        sorted_records = sorted(store.values(), key=lambda r: (r.importance, r.access_count))
        to_compress_count = len(store) - max_items

        for rec in sorted_records[:to_compress_count]:
            rec.state = MemoryLifecycleState.COMPRESSED
            rec.value = f"[COMPRESSED SUMMARY: {str(rec.value)[:50]}...]"

        logger.info(f"Compressed {to_compress_count} records in tier {m_tier.value}")
        return to_compress_count

    def merge(self, target_key: str, source_keys: List[str], tier: MemoryTier | str) -> Optional[EnterpriseMemoryRecord]:
        """Merges multiple related memory records into a consolidated target record."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        store = self._stores[m_tier]

        merged_values: List[Any] = []
        max_imp = 0.0

        for sk in source_keys:
            if sk in store:
                rec = store.pop(sk)
                merged_values.append(rec.value)
                max_imp = max(max_imp, rec.importance)

        if not merged_values:
            return None

        merged_record = EnterpriseMemoryRecord(
            id=f"mem-{uuid.uuid4().hex[:12]}",
            tier=m_tier,
            key=target_key,
            value={"merged_entries": merged_values},
            importance=max_imp,
            state=MemoryLifecycleState.SUMMARIZED,
        )
        store[target_key] = merged_record
        logger.info(f"Merged {len(source_keys)} records into '{target_key}' in tier {m_tier.value}")
        return merged_record

    def expire_records(self, now: Optional[datetime] = None) -> int:
        """Scans and marks expired records across all tiers."""
        current_time = now or datetime.now(timezone.utc)
        expired_count = 0

        for tier_store in self._stores.values():
            for rec in list(tier_store.values()):
                if rec.expires_at and rec.expires_at <= current_time:
                    rec.state = MemoryLifecycleState.EXPIRED
                    expired_count += 1

        if expired_count > 0:
            logger.info(f"Expired {expired_count} memory records across platform tiers")
        return expired_count

    def list_tier(self, tier: MemoryTier | str) -> List[EnterpriseMemoryRecord]:
        """Lists all records currently stored in a given tier."""
        m_tier = tier if isinstance(tier, MemoryTier) else MemoryTier(tier)
        return list(self._stores[m_tier].values())
