"""
Memory Consolidation & Multi-Tier Cognitive Memory Engine for Phase 13.16.
Converts working memory to long-term episodic/semantic/procedural memory with forgetting curve decay.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.world_model.events.world_model_events import (
    WorldModelEvent,
    WorldModelEventType,
    world_model_event_bus,
)


@dataclass
class ConsolidatedMemoryBlock:
    memory_id: str = field(default_factory=lambda: f"mem_{uuid.uuid4().hex[:8]}")
    tier: str = "long_term"  # short_term, working, long_term, semantic, episodic, procedural
    title: str = ""
    summary: str = ""
    key_facts: List[str] = field(default_factory=list)
    importance_score: float = 0.88  # 0.0 to 1.0
    stability_factor: float = 48.0  # Hours of retention stability
    replay_count: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_accessed: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def compute_retention_probability(self) -> float:
        """Ebbinghaus forgetting curve: R = e^(-t / S)."""
        now = datetime.now(timezone.utc)
        try:
            accessed = datetime.fromisoformat(self.last_accessed.replace("Z", "+00:00"))
            dt_hours = (now - accessed).total_seconds() / 3600.0
        except Exception:
            dt_hours = 0.0
        return math.exp(-dt_hours / max(1.0, self.stability_factor))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "tier": self.tier,
            "title": self.title,
            "summary": self.summary,
            "key_facts": self.key_facts,
            "importance_score": round(self.importance_score, 3),
            "stability_factor": self.stability_factor,
            "replay_count": self.replay_count,
            "retention_probability": round(self.compute_retention_probability(), 4),
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
        }


class MemoryConsolidationEngine:
    """Manages cognitive memory lifecycle, consolidation passes, and episodic replays."""

    def __init__(self):
        self._memories: Dict[str, ConsolidatedMemoryBlock] = {}
        self._initialize_seed_memories()

    def _initialize_seed_memories(self) -> None:
        seeds = [
            ConsolidatedMemoryBlock(
                memory_id="mem_canary_deployment_playbook",
                tier="procedural",
                title="Procedural Knowledge: Autonomous Canary Hotfix Protocol",
                summary="Standard procedure for spinning 4 replicas, testing health probes, verifying invariants and updating Slack channels.",
                key_facts=["Always verify P99 < 50ms before routing 100% traffic", "Execute Saga rollback if error rate > 0.5%"],
                importance_score=0.96,
                stability_factor=720.0,
                replay_count=14,
            ),
            ConsolidatedMemoryBlock(
                memory_id="mem_stripe_billing_thresholds",
                tier="semantic",
                title="Semantic Knowledge: Enterprise Financial Invoicing Limits",
                summary="Policy bounds requiring executive HITL sign-off for single transactions exceeding $1,000.",
                key_facts=["Stripe restricted API keys scoped to invoices:write only", "Monthly spend cap = $25,000"],
                importance_score=0.92,
                stability_factor=1440.0,
                replay_count=22,
            ),
        ]
        for m in seeds:
            self._memories[m.memory_id] = m

    def consolidate_memory(
        self,
        tier: str,
        title: str,
        summary: str,
        key_facts: List[str],
        importance_score: float = 0.85,
    ) -> ConsolidatedMemoryBlock:
        mid = f"mem_{uuid.uuid4().hex[:8]}"
        mem = ConsolidatedMemoryBlock(
            memory_id=mid,
            tier=tier,
            title=title,
            summary=summary,
            key_facts=key_facts,
            importance_score=importance_score,
            stability_factor=72.0 * importance_score,
        )
        self._memories[mid] = mem

        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.MEMORY_CONSOLIDATED,
                source="memory_consolidation_engine",
                payload=mem.to_dict(),
            )
        )
        return mem

    def list_memories(self, tier: Optional[str] = None) -> List[ConsolidatedMemoryBlock]:
        items = list(self._memories.values())
        if tier:
            items = [m for m in items if m.tier.lower() == tier.lower()]
        return items

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_memories": len(self._memories),
            "memories": [m.to_dict() for m in self._memories.values()],
        }


# Global Singleton
memory_consolidation_engine = MemoryConsolidationEngine()
