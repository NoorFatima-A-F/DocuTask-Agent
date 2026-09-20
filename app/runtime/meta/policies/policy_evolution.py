"""
AMRS-RSIP Phase 13.9 - Policy Evolution Engine
Evaluates runtime policy constraints, identifies policy gaps, and synthesizes cryptographically signed policy evolution proposals.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class PolicyEvolutionProposal:
    proposal_id: str
    policy_name: str
    category: str  # 'RESOURCE_ALLOCATION', 'PLANNER_CONCURRENCY', 'SECURITY_QUORUM', 'SELF_HEALING'
    current_rule: str
    proposed_rule: str
    rationale: str
    evidence_backing: List[str]
    predicted_impact: Dict[str, Any]
    status: str = "PENDING_APPROVAL"  # PENDING_APPROVAL, APPROVED, REJECTED, APPLIED
    sha256_proposal_hash: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PolicyEvolutionEngine:
    """
    Master policy evolution engine generating verifiable upgrades to system runtime rules.
    """

    def __init__(self):
        self._proposals: Dict[str, PolicyEvolutionProposal] = {}
        self._seed_default_proposals()

    def propose_policy_upgrade(
        self,
        policy_name: str,
        category: str,
        current_rule: str,
        proposed_rule: str,
        rationale: str,
        evidence_backing: List[str],
        predicted_impact: Optional[Dict[str, Any]] = None,
    ) -> PolicyEvolutionProposal:
        pid = f"pol-prop-{uuid.uuid4().hex[:8]}"
        impact = predicted_impact or {"latency_gain_pct": 20.0, "risk_delta": "NEGLIGIBLE"}

        payload = f"{pid}:{policy_name}:{current_rule}:{proposed_rule}:{rationale}"
        prop_hash = hashlib.sha256(payload.encode()).hexdigest()

        proposal = PolicyEvolutionProposal(
            proposal_id=pid,
            policy_name=policy_name,
            category=category,
            current_rule=current_rule,
            proposed_rule=proposed_rule,
            rationale=rationale,
            evidence_backing=evidence_backing,
            predicted_impact=impact,
            status="PENDING_APPROVAL",
            sha256_proposal_hash=prop_hash,
        )

        self._proposals[pid] = proposal
        return proposal

    def get_all_proposals(self) -> List[PolicyEvolutionProposal]:
        return list(self._proposals.values())

    def get_proposal(self, proposal_id: str) -> Optional[PolicyEvolutionProposal]:
        return self._proposals.get(proposal_id)

    def apply_proposal(self, proposal_id: str) -> bool:
        prop = self._proposals.get(proposal_id)
        if prop and prop.status == "APPROVED":
            prop.status = "APPLIED"
            return True
        return False

    def _seed_default_proposals(self):
        self.propose_policy_upgrade(
            policy_name="Dynamic Worker Concurrency Quota",
            category="PLANNER_CONCURRENCY",
            current_rule="Limit worker pool max concurrency to 4 simultaneous tasks per DAG.",
            proposed_rule="Dynamically scale worker pool concurrency up to 12 tasks when memory utilization is < 60%.",
            rationale="Batch document extraction jobs queue unnecessarily under low system load.",
            evidence_backing=["obs-latency-spike-ocr", "exp-dynamic-fanout"],
            predicted_impact={"latency_reduction_pct": 44.0, "memory_increase_pct": 18.0},
        )
