"""
Enterprise Multi-Tier Memory System
Short-Term (working), Long-Term (episodic), Organizational (company-wide), and Procedural (SOPs).
"""
from typing import Dict, List, Optional
from ..models.schemas import MemoryEntry, MemoryTier

class EnterpriseMemorySystem:
    def __init__(self):
        self._memories: Dict[str, MemoryEntry] = {}

    def store_memory(
        self,
        tenant_id: str,
        key: str,
        content: str,
        tier: MemoryTier = MemoryTier.SHORT_TERM,
        agent_id: Optional[str] = None,
        importance_score: float = 1.0,
        metadata: Optional[Dict] = None
    ) -> MemoryEntry:
        mem = MemoryEntry(
            tenant_id=tenant_id,
            key=key,
            content=content,
            tier=tier,
            agent_id=agent_id,
            importance_score=importance_score,
            metadata=metadata or {}
        )
        self._memories[mem.id] = mem
        return mem

    def retrieve_memory(
        self,
        tenant_id: str,
        query: str,
        tier: Optional[MemoryTier] = None,
        agent_id: Optional[str] = None,
        limit: int = 5
    ) -> List[MemoryEntry]:
        results = [m for m in self._memories.values() if m.tenant_id == tenant_id]
        if tier:
            results = [m for m in results if m.tier == tier]
        if agent_id:
            results = [m for m in results if m.agent_id == agent_id]
            
        # Keyword relevance ranking
        query_words = set(query.lower().split())
        scored = []
        for m in results:
            content_words = set(f"{m.key} {m.content}".lower().split())
            overlap = len(query_words.intersection(content_words))
            score = (overlap * 2.0 + m.importance_score)
            scored.append((score, m))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    def list_all_memories(self, tenant_id: str) -> List[MemoryEntry]:
        return [m for m in self._memories.values() if m.tenant_id == tenant_id]

    def delete_memory(self, memory_id: str, tenant_id: str) -> bool:
        mem = self._memories.get(memory_id)
        if mem and mem.tenant_id == tenant_id:
            del self._memories[memory_id]
            return True
        return False
