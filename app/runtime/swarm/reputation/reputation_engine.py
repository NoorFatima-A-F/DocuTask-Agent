"""
AMCN-SIP Phase 13.8 - Reputation & Trust Intelligence
Multi-dimensional reputation scoring, pairwise trust networks, and adaptive inactivity decay.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class AgentReputationRecord:
    agent_id: str
    composite_reputation: float  # 0.0 - 1.0
    accuracy_score: float
    sla_adherence_score: float
    collaboration_quality: float
    governance_compliance: float
    total_evaluations: int = 1
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ReputationDecayEngine:
    """
    Applies mathematical decay for inactive or regressing agents.
    """

    def apply_decay(self, current_score: float, days_inactive: float) -> float:
        decay_factor = max(0.0, days_inactive * 0.01)
        return round(max(0.1, current_score - decay_factor), 3)


class TrustEngine:
    """
    Maintains pairwise and global trust graph edges between collaborating agents.
    """

    def __init__(self):
        self._trust_matrix: Dict[str, Dict[str, float]] = {}

    def update_pairwise_trust(self, source_agent_id: str, target_agent_id: str, delta: float):
        if source_agent_id not in self._trust_matrix:
            self._trust_matrix[source_agent_id] = {}

        current = self._trust_matrix[source_agent_id].get(target_agent_id, 0.85)
        new_val = round(max(0.0, min(1.0, current + delta)), 3)
        self._trust_matrix[source_agent_id][target_agent_id] = new_val

    def get_trust_score(self, source_agent_id: str, target_agent_id: str) -> float:
        return self._trust_matrix.get(source_agent_id, {}).get(target_agent_id, 0.85)

    def get_all_edges(self) -> List[Dict[str, Any]]:
        edges = []
        for src, targets in self._trust_matrix.items():
            for tgt, val in targets.items():
                edges.append({"source": src, "target": tgt, "trust_score": val})
        return edges


class ReputationEngine:
    """
    Master coordinator for agent society reputation and trust analytics.
    """

    def __init__(self):
        self.decay_engine = ReputationDecayEngine()
        self.trust_engine = TrustEngine()
        self._reputations: Dict[str, AgentReputationRecord] = {}
        self._seed_default_reputations()

    def record_performance(
        self,
        agent_id: str,
        task_success: bool,
        sla_met: bool,
        governance_clean: bool = True,
    ):
        rec = self._reputations.get(agent_id)
        if not rec:
            rec = AgentReputationRecord(
                agent_id=agent_id,
                composite_reputation=0.95,
                accuracy_score=0.98,
                sla_adherence_score=0.95,
                collaboration_quality=0.95,
                governance_compliance=1.0,
            )
            self._reputations[agent_id] = rec

        acc_delta = 0.01 if task_success else -0.05
        sla_delta = 0.01 if sla_met else -0.04
        gov_delta = 0.00 if governance_clean else -0.10

        rec.accuracy_score = round(max(0.0, min(1.0, rec.accuracy_score + acc_delta)), 3)
        rec.sla_adherence_score = round(max(0.0, min(1.0, rec.sla_adherence_score + sla_delta)), 3)
        rec.governance_compliance = round(max(0.0, min(1.0, rec.governance_compliance + gov_delta)), 3)

        rec.composite_reputation = round(
            (rec.accuracy_score * 0.35)
            + (rec.sla_adherence_score * 0.30)
            + (rec.collaboration_quality * 0.20)
            + (rec.governance_compliance * 0.15),
            3,
        )
        rec.total_evaluations += 1
        rec.last_updated = datetime.now(timezone.utc).isoformat()

    def get_agent_reputation(self, agent_id: str) -> Optional[AgentReputationRecord]:
        return self._reputations.get(agent_id)

    def get_reputation(self, agent_id: str) -> Optional[AgentReputationRecord]:
        return self.get_agent_reputation(agent_id)

    def get_all_reputations(self) -> List[AgentReputationRecord]:
        return list(self._reputations.values())

    def _seed_default_reputations(self):
        agents = [
            ("agent-exec-01", 0.99, 0.99, 0.98, 1.0),
            ("agent-plan-01", 0.98, 0.97, 0.96, 1.0),
            ("agent-coord-01", 0.97, 0.98, 0.97, 1.0),
            ("agent-spec-ocr", 0.98, 0.97, 0.96, 1.0),
            ("agent-val-sec", 0.99, 0.99, 0.99, 1.0),
            ("agent-res-opt", 0.96, 0.95, 0.97, 1.0),
            ("agt-exec-01", 0.99, 0.99, 0.98, 1.0),
            ("agt-doc-extract", 0.98, 0.97, 0.96, 1.0),
            ("agt-fin-validator", 0.99, 0.99, 0.99, 1.0),
            ("agt-peer-reviewer", 0.96, 0.95, 0.97, 1.0),
            ("agt-recovery-agent", 0.97, 0.98, 0.96, 1.0),
        ]
        for aid, acc, sla, col, gov in agents:
            self._reputations[aid] = AgentReputationRecord(
                agent_id=aid,
                composite_reputation=round((acc * 0.35) + (sla * 0.30) + (col * 0.20) + (gov * 0.15), 3),
                accuracy_score=acc,
                sla_adherence_score=sla,
                collaboration_quality=col,
                governance_compliance=gov,
            )
            # Seed pairwise trust
            self.trust_engine.update_pairwise_trust(aid, "agent-spec-ocr", 0.05)
            self.trust_engine.update_pairwise_trust(aid, "agent-val-sec", 0.08)
