"""
AMCN-SIP Phase 13.8 - Coalition Formation & Team Optimization
Dynamic team formation, merge, split, dissolve, synergy optimization, and historical coalition memory.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class AgentCoalition:
    coalition_id: str
    name: str
    objective: str
    member_agent_ids: List[str]
    lead_agent_id: str
    mission_id: str = "mission-default"
    synergy_score: float = 0.85  # 0.0 - 1.0
    capability_diversity_pct: float = 80.0
    status: str = "ACTIVE"  # ACTIVE, MERGED, SPLIT, DISSOLVED
    tasks_completed: int = 0
    formed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TeamOptimizer:
    """
    Evaluates team composition synergy, capability coverage, and communication overhead.
    """

    def calculate_synergy(self, member_count: int, capability_count: int) -> float:
        if member_count == 0:
            return 0.0
        coverage = min(1.0, capability_count / 5.0)
        overhead = max(0.0, (member_count - 3) * 0.05)
        return round(max(0.1, min(1.0, coverage - overhead + 0.2)), 2)

    def optimize_team(self, all_agents: List[Any], required_skills: List[str]) -> List[Any]:
        selected: List[Any] = []
        covered_skills = set()

        for skill in required_skills:
            if skill in covered_skills:
                continue
            for agent in all_agents:
                agent_caps = getattr(agent, "capabilities", [])
                if any(skill.lower() in cap.lower() for cap in agent_caps) and agent not in selected:
                    selected.append(agent)
                    for cap in agent_caps:
                        covered_skills.add(cap.lower())
                    break

        if not selected and all_agents:
            selected = all_agents[:min(3, len(all_agents))]

        return selected


class CoalitionMemory:
    """
    Stores historical team performance and inter-agent collaboration compatibility.
    """

    def __init__(self):
        self._history: List[AgentCoalition] = []

    def record_coalition(self, coalition: AgentCoalition):
        self._history.append(coalition)

    def get_all_coalitions(self) -> List[AgentCoalition]:
        return self._history


class CoalitionManager:
    """
    Master coordinator for dynamic coalition formation, merging, splitting, and dissolution.
    """

    def __init__(self):
        self.optimizer = TeamOptimizer()
        self.memory = CoalitionMemory()
        self._coalitions: Dict[str, AgentCoalition] = {}
        self._seed_default_coalitions()

    def create_coalition(
        self,
        name_or_id: Optional[str] = None,
        name: Optional[str] = None,
        objective: str = "Collaborative Execution",
        member_ids: Optional[List[str]] = None,
        lead_id: Optional[str] = None,
        **kwargs,
    ) -> AgentCoalition:
        if "coalition_id" in kwargs:
            cid = kwargs["coalition_id"]
            c_name = kwargs.get("name", name_or_id or "Coalition")
            c_obj = kwargs.get("objective", objective)
            m_ids = kwargs.get("member_agent_ids", member_ids or [])
            l_id = kwargs.get("lead_agent_id", lead_id or (m_ids[0] if m_ids else "agent-exec-01"))
            mission_id = kwargs.get("mission_id", "mission-default")
        elif name is not None:
            cid = name_or_id
            c_name = name
            c_obj = objective
            m_ids = member_ids or []
            l_id = lead_id or (m_ids[0] if m_ids else "agent-exec-01")
            mission_id = kwargs.get("mission_id", "mission-default")
        else:
            cid = f"coal-{uuid.uuid4().hex[:8]}"
            c_name = name_or_id
            c_obj = objective
            m_ids = member_ids or []
            l_id = lead_id or (m_ids[0] if m_ids else "agent-exec-01")
            mission_id = kwargs.get("mission_id", "mission-default")

        synergy = self.optimizer.calculate_synergy(len(m_ids), len(m_ids) * 2)

        coalition = AgentCoalition(
            coalition_id=cid,
            name=c_name,
            objective=c_obj,
            member_agent_ids=m_ids,
            lead_agent_id=l_id,
            mission_id=mission_id,
            synergy_score=synergy,
            capability_diversity_pct=round(min(100.0, len(m_ids) * 25.0), 1),
            status="ACTIVE",
        )

        self._coalitions[cid] = coalition
        self.memory.record_coalition(coalition)
        return coalition

    def dissolve_coalition(self, coalition_id: str, reason: str = "OBJECTIVE_ACCOMPLISHED"):
        coal = self._coalitions.get(coalition_id)
        if coal:
            coal.status = "DISSOLVED"

    def list_coalitions(self, active_only: bool = False) -> List[AgentCoalition]:
        coalitions = list(self._coalitions.values())
        if active_only:
            coalitions = [c for c in coalitions if c.status == "ACTIVE"]
        return coalitions

    def get_coalition(self, coalition_id: str) -> Optional[AgentCoalition]:
        return self._coalitions.get(coalition_id)

    def _seed_default_coalitions(self):
        self.create_coalition(
            name_or_id="coalition-alpha",
            name="Alpha Extraction & Validation Coalition",
            objective="High-throughput parallel OCR document processing and verification",
            member_ids=["agent-spec-ocr", "agent-val-sec", "agent-res-opt"],
            lead_id="agent-exec-01",
            mission_id="mission-9482",
        )
