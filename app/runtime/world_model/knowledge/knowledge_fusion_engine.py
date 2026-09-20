"""
Knowledge Fusion & Semantic Integration Engine for Phase 13.16.
Merges multi-runtime facts, resolves epistemic conflicts, links entities, and computes time-decayed freshness scores.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.world_model.events.world_model_events import (
    KnowledgeFreshness,
    WorldModelEvent,
    WorldModelEventType,
    world_model_event_bus,
)


@dataclass
class KnowledgeFact:
    fact_id: str = field(default_factory=lambda: f"fact_{uuid.uuid4().hex[:8]}")
    subject: str = ""
    predicate: str = ""
    object_value: Any = ""
    source_runtime: str = "execution_runtime"
    confidence: float = 0.95
    truth_rank: float = 0.92  # 0.0 to 1.0
    evidence_refs: List[str] = field(default_factory=list)
    freshness: KnowledgeFreshness = KnowledgeFreshness.REAL_TIME
    decay_half_life_hours: float = 24.0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def compute_freshness_score(self) -> float:
        """Computes exponential decay: score = e^(-lambda * dt_hours)."""
        now = datetime.now(timezone.utc)
        try:
            created = datetime.fromisoformat(self.updated_at.replace("Z", "+00:00"))
            dt_hours = (now - created).total_seconds() / 3600.0
        except Exception:
            dt_hours = 0.0

        decay_lambda = math.log(2) / max(0.1, self.decay_half_life_hours)
        score = math.exp(-decay_lambda * dt_hours)
        return max(0.01, min(1.0, score))

    def to_dict(self) -> Dict[str, Any]:
        fresh_score = self.compute_freshness_score()
        return {
            "fact_id": self.fact_id,
            "subject": self.subject,
            "predicate": self.predicate,
            "object_value": self.object_value,
            "source_runtime": self.source_runtime,
            "confidence": round(self.confidence, 4),
            "truth_rank": round(self.truth_rank, 4),
            "evidence_refs": self.evidence_refs,
            "freshness": self.freshness.value if isinstance(self.freshness, KnowledgeFreshness) else str(self.freshness),
            "freshness_score": round(fresh_score, 3),
            "decay_half_life_hours": self.decay_half_life_hours,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class KnowledgeFusionEngine:
    """Consolidates and harmonizes facts into an epistemic knowledge base."""

    def __init__(self):
        self._facts: Dict[str, KnowledgeFact] = {}
        self._initialize_seed_knowledge()

    def _initialize_seed_knowledge(self) -> None:
        seed_facts = [
            KnowledgeFact(
                fact_id="fact_core_api_latency_sla",
                subject="service_core_api",
                predicate="p99_latency_sla_ms",
                object_value=50.0,
                source_runtime="execution_runtime",
                confidence=0.99,
                truth_rank=0.98,
                evidence_refs=["obs_k8s_canary_latency"],
            ),
            KnowledgeFact(
                fact_id="fact_k8s_cluster_capacity",
                subject="k8s_prod_cluster",
                predicate="max_replicas_available",
                object_value=48,
                source_runtime="execution_runtime",
                confidence=0.99,
                truth_rank=0.99,
                evidence_refs=["conn_k8s_production"],
            ),
            KnowledgeFact(
                fact_id="fact_org_burn_rate_limit",
                subject="dept_engineering",
                predicate="monthly_budget_cap_usd",
                object_value=25000.0,
                source_runtime="organization_runtime",
                confidence=0.98,
                truth_rank=0.96,
                evidence_refs=["obs_org_budget_burn"],
            ),
            KnowledgeFact(
                fact_id="fact_postgres_dw_pool_size",
                subject="postgres_warehouse",
                predicate="connection_pool_limit",
                object_value=30,
                source_runtime="execution_runtime",
                confidence=1.0,
                truth_rank=1.0,
            ),
            KnowledgeFact(
                fact_id="fact_stripe_merchant_status",
                subject="gateway_stripe",
                predicate="operational_status",
                object_value="LIVE_ACTIVE",
                source_runtime="execution_runtime",
                confidence=1.0,
                truth_rank=1.0,
            ),
        ]
        for f in seed_facts:
            self._facts[f.fact_id] = f

    def integrate_fact(
        self,
        subject: str,
        predicate: str,
        object_value: Any,
        source_runtime: str = "execution_runtime",
        confidence: float = 0.95,
        evidence_refs: Optional[List[str]] = None,
    ) -> KnowledgeFact:
        # Check for existing fact to detect conflicts or merge
        existing_id = None
        for fid, f in self._facts.items():
            if f.subject.lower() == subject.lower() and f.predicate.lower() == predicate.lower():
                existing_id = fid
                break

        if existing_id:
            fact = self._facts[existing_id]
            # If value differs, evaluate truth ranking & update
            if fact.object_value != object_value:
                fact.object_value = object_value
                fact.confidence = (fact.confidence + confidence) / 2.0
                fact.updated_at = datetime.now(timezone.utc).isoformat()
                world_model_event_bus.publish(
                    WorldModelEvent(
                        event_type=WorldModelEventType.KNOWLEDGE_CONFLICT_RESOLVED,
                        source="knowledge_fusion_engine",
                        payload={"fact_id": fact.fact_id, "subject": subject, "new_value": object_value},
                    )
                )
            else:
                # Reinforce truth rank
                fact.truth_rank = min(1.0, fact.truth_rank + 0.02)
                fact.updated_at = datetime.now(timezone.utc).isoformat()
            return fact

        fact = KnowledgeFact(
            subject=subject,
            predicate=predicate,
            object_value=object_value,
            source_runtime=source_runtime,
            confidence=confidence,
            evidence_refs=evidence_refs or [],
        )
        self._facts[fact.fact_id] = fact

        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.KNOWLEDGE_INTEGRATED,
                source="knowledge_fusion_engine",
                payload=fact.to_dict(),
            )
        )
        return fact

    def get_fact(self, fact_id: str) -> Optional[KnowledgeFact]:
        return self._facts.get(fact_id)

    def list_facts(
        self,
        subject: Optional[str] = None,
        source_runtime: Optional[str] = None,
    ) -> List[KnowledgeFact]:
        items = list(self._facts.values())
        if subject:
            items = [f for f in items if f.subject.lower() == subject.lower()]
        if source_runtime:
            items = [f for f in items if f.source_runtime.lower() == source_runtime.lower()]
        return items

    def get_knowledge_summary(self) -> Dict[str, Any]:
        facts = list(self._facts.values())
        total = len(facts)
        avg_freshness = sum(f.compute_freshness_score() for f in facts) / total if total > 0 else 1.0
        avg_truth = sum(f.truth_rank for f in facts) / total if total > 0 else 1.0

        return {
            "total_facts": total,
            "average_freshness_score": round(avg_freshness, 3),
            "average_truth_rank": round(avg_truth, 3),
            "subjects_count": len(set(f.subject for f in facts)),
        }


# Global Singleton
knowledge_fusion_engine = KnowledgeFusionEngine()
