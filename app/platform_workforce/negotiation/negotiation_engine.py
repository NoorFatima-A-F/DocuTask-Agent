"""
5. Negotiation Engine Subsystem
"""
from typing import Dict, List, Optional, Any
from app.platform_workforce.models.schemas import NegotiationSession

class NegotiationEngine:
    def __init__(self):
        self._sessions: Dict[str, Dict[str, NegotiationSession]] = {}
        self._seed_default_negotiations()

    def _seed_default_negotiations(self):
        tenant = "default-tenant"
        neg = NegotiationSession(
            id="neg-res-borrow-01",
            topic="GPU Cluster Borrowing for Batch Re-indexing",
            participant_employee_ids=["emp-eng-mgr", "emp-sec-dir", "emp-doc-spec-01"],
            proposals=[
                {"from": "emp-eng-mgr", "proposal": "Allocate 4x H100 GPUs for 2 hours during low traffic window."},
                {"from": "emp-sec-dir", "proposal": "Approved provided compliance redacting agent maintains 1 dedicated GPU."}
            ],
            consensus_reached=True,
            agreed_terms={"gpu_count": 3, "duration_hours": 2, "priority_lane": "BACKGROUND"},
            status="AGREED"
        )
        self._sessions[tenant] = {neg.id: neg}

    def get_sessions(self, tenant_id: str = "default-tenant") -> List[NegotiationSession]:
        return list(self._sessions.get(tenant_id, {}).values())

    def start_negotiation(self, topic: str, participant_ids: List[str], initial_proposal: str, tenant_id: str = "default-tenant") -> NegotiationSession:
        session = NegotiationSession(
            tenant_id=tenant_id,
            topic=topic,
            participant_employee_ids=participant_ids,
            proposals=[{"from": participant_ids[0] if participant_ids else "system", "proposal": initial_proposal}],
            status="IN_PROGRESS"
        )
        if tenant_id not in self._sessions:
            self._sessions[tenant_id] = {}
        self._sessions[tenant_id][session.id] = session
        return session

    def add_counter_proposal(self, session_id: str, employee_id: str, proposal: str, consensus_reached: bool = False, agreed_terms: Optional[Dict[str, Any]] = None, tenant_id: str = "default-tenant") -> Optional[NegotiationSession]:
        session = self._sessions.get(tenant_id, {}).get(session_id)
        if not session:
            return None
        session.proposals.append({"from": employee_id, "proposal": proposal})
        if consensus_reached:
            session.consensus_reached = True
            session.status = "AGREED"
            session.agreed_terms = agreed_terms or {"resolved": True}
        return session

negotiation_engine = NegotiationEngine()
