"""
6. Collaboration Protocol Engine Subsystem
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.platform_workforce.models.schemas import CollaborationVote

class CollaborationProtocolEngine:
    def __init__(self):
        self._votes: Dict[str, Dict[str, CollaborationVote]] = {}
        self._seed_default_votes()

    def _seed_default_votes(self):
        tenant = "default-tenant"
        vote = CollaborationVote(
            id="vote-prod-deploy-88",
            proposal_title="Deploy FastV2 Parser to Production Pipeline",
            initiator_employee_id="emp-eng-mgr",
            voter_employee_ids=["emp-eng-mgr", "emp-sec-dir", "emp-qa-rev-01"],
            votes={"emp-eng-mgr": "YES", "emp-sec-dir": "YES", "emp-qa-rev-01": "YES"},
            required_quorum=0.66,
            status="APPROVED",
            decided_at=datetime.now(timezone.utc)
        )
        self._votes[tenant] = {vote.id: vote}

    def get_votes(self, tenant_id: str = "default-tenant") -> List[CollaborationVote]:
        return list(self._votes.get(tenant_id, {}).values())

    def create_proposal(self, title: str, initiator_id: str, voter_ids: List[str], required_quorum: float = 0.66, tenant_id: str = "default-tenant") -> CollaborationVote:
        vote = CollaborationVote(
            tenant_id=tenant_id,
            proposal_title=title,
            initiator_employee_id=initiator_id,
            voter_employee_ids=voter_ids,
            required_quorum=required_quorum,
            status="PENDING"
        )
        if tenant_id not in self._votes:
            self._votes[tenant_id] = {}
        self._votes[tenant_id][vote.id] = vote
        return vote

    def cast_vote(self, vote_id: str, employee_id: str, choice: str, tenant_id: str = "default-tenant") -> Optional[CollaborationVote]:
        vote = self._votes.get(tenant_id, {}).get(vote_id)
        if not vote or vote.status != "PENDING":
            return None
        vote.votes[employee_id] = choice.upper()
        
        # Check quorum and results
        total_voters = len(vote.voter_employee_ids)
        if len(vote.votes) >= total_voters or len(vote.votes) >= max(1, int(total_voters * vote.required_quorum)):
            yes_votes = sum(1 for v in vote.votes.values() if v == "YES")
            if (yes_votes / max(total_voters, 1)) >= vote.required_quorum:
                vote.status = "APPROVED"
                vote.decided_at = datetime.now(timezone.utc)
            elif (len(vote.votes) == total_voters):
                vote.status = "REJECTED"
                vote.decided_at = datetime.now(timezone.utc)
        return vote

collaboration_protocol_engine = CollaborationProtocolEngine()
