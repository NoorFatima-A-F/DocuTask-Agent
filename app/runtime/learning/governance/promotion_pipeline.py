"""
Promotion Pipeline Manager for Phase 13.5 (ARLP-KIP).
Safely orchestrates promotion of approved candidate policies into active production runtime.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field

from app.runtime.learning.policy.policy_engine import policy_engine
from app.runtime.learning.policy.policy_registry import evolution_policy_registry, ActivePolicyEntry


class PromotionRecord(BaseModel):
    promotion_id: str = Field(default_factory=lambda: f"prom_{uuid.uuid4().hex[:8]}")
    candidate_id: str
    target_component: str
    promoted_policy_id: str
    status: str = "PROMOTED"  # PROMOTED | REJECTED
    promoter_id: str = "governance-pipeline"
    promoted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PromotionPipelineManager:
    """
    Manages atomic policy promotions from candidate stage to active execution.
    """

    def __init__(self):
        self._promotions: List[PromotionRecord] = []

    def promote(self, candidate_id: str, promoter_id: str = "governance-pipeline") -> PromotionRecord:
        cand = policy_engine.get_candidate(candidate_id)
        target_component = cand.target_component if cand else "planner"
        policy_name = cand.policy_name if cand else "Promoted Policy"
        params = cand.parameters if cand else {"max_retries": 3, "concurrency_limit": 8}

        active_entry = ActivePolicyEntry(
            policy_id=f"pol-active-{uuid.uuid4().hex[:6]}",
            target_component=target_component,
            policy_name=policy_name,
            version="1.1.0",
            parameters=params,
            promoter_id=promoter_id,
        )
        evolution_policy_registry.set_active_policy(active_entry)

        if cand:
            cand.status = "PROMOTED"

        rec = PromotionRecord(
            candidate_id=candidate_id,
            target_component=target_component,
            promoted_policy_id=active_entry.policy_id,
            status="PROMOTED",
            promoter_id=promoter_id,
        )
        self._promotions.append(rec)
        return rec

    def list_promotions(self) -> List[PromotionRecord]:
        return self._promotions


promotion_pipeline_manager = PromotionPipelineManager()
