"""
Enterprise Decision Intelligence
Records and tracks decision objects (reasoning, alternatives, risk, confidence, expected vs. actual outcomes).
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from ..models.schemas import DecisionRecord

class EnterpriseDecisionIntelligence:
    def __init__(self):
        self._decisions: Dict[str, DecisionRecord] = {}

    def record_decision(
        self,
        tenant_id: str,
        topic: str,
        chosen_action: str,
        alternatives: List[str],
        rationale: str,
        confidence: float,
        expected_outcome: Dict[str, Any]
    ) -> DecisionRecord:
        rec = DecisionRecord(
            tenant_id=tenant_id,
            decision_topic=topic,
            chosen_action=chosen_action,
            alternatives_considered=alternatives,
            reasoning_rationale=rationale,
            confidence_score=confidence,
            expected_outcome=expected_outcome
        )
        self._decisions[rec.id] = rec
        return rec

    def resolve_actual_outcome(
        self,
        decision_id: str,
        tenant_id: str,
        actual_outcome: Dict[str, Any],
        matched: bool
    ) -> Optional[DecisionRecord]:
        rec = self._decisions.get(decision_id)
        if rec and rec.tenant_id == tenant_id:
            rec.actual_outcome = actual_outcome
            rec.outcome_matched = matched
            rec.resolved_at = datetime.now(timezone.utc)
            return rec
        return None

    def list_decisions(self, tenant_id: str) -> List[DecisionRecord]:
        return [d for d in self._decisions.values() if d.tenant_id == tenant_id]
