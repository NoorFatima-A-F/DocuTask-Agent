"""
AMAEOP Pillar 3 - Inter-Department Resource Negotiation Engine
Handles bilateral resource trading, quota loaning, and mutual SLA commitments between departments.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import time
import uuid


@dataclass
class ResourceTradeProposal:
    proposal_id: str
    initiator_dept_id: str
    target_dept_id: str
    offered_resource: str
    offered_quantity: float
    requested_resource: str
    requested_quantity: float
    duration_seconds: float
    status: str  # PROPOSED | ACCEPTED | REJECTED | EXPIRED
    rationale: str
    proposed_at: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ResourceNegotiator:
    """Manages bilateral resource exchanges and mutual capacity balancing."""

    def __init__(self):
        self.proposals: Dict[str, ResourceTradeProposal] = {}
        self._seed_proposals()

    def _seed_proposals(self):
        p1 = ResourceTradeProposal(
            proposal_id="prop_trade_001",
            initiator_dept_id="dept_ocr",
            target_dept_id="dept_research",
            offered_resource="OCR_WORKER_THREAD",
            offered_quantity=2.0,
            requested_resource="GEMINI_PRO_TOKENS",
            requested_quantity=50000.0,
            duration_seconds=300.0,
            status="ACCEPTED",
            rationale="OCR department trades idle night worker threads for research token quota to parse multi-page dense ledger.",
            proposed_at=time.time() - 120.0,
        )
        self.proposals[p1.proposal_id] = p1

    def propose_trade(
        self,
        initiator_dept_id: str,
        target_dept_id: str,
        offered_resource: str,
        offered_quantity: float,
        requested_resource: str,
        requested_quantity: float,
        duration_seconds: float,
        rationale: str,
    ) -> ResourceTradeProposal:
        prop_id = f"prop_{uuid.uuid4().hex[:6]}"
        proposal = ResourceTradeProposal(
            proposal_id=prop_id,
            initiator_dept_id=initiator_dept_id,
            target_dept_id=target_dept_id,
            offered_resource=offered_resource,
            offered_quantity=offered_quantity,
            requested_resource=requested_resource,
            requested_quantity=requested_quantity,
            duration_seconds=duration_seconds,
            status="PROPOSED",
            rationale=rationale,
            proposed_at=time.time(),
        )
        self.proposals[prop_id] = proposal
        return proposal

    def accept_trade(self, proposal_id: str) -> bool:
        if proposal_id in self.proposals:
            self.proposals[proposal_id].status = "ACCEPTED"
            return True
        return False

    def list_trades(self) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in self.proposals.values()]


resource_negotiator = ResourceNegotiator()
