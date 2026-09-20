"""
AMAEOP Pillar 2 - Mission Director
Directs multi-department mission lifecycle, stage handoffs, and organizational milestone execution.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import time


@dataclass
class MissionStage:
    stage_index: int
    stage_name: str
    owning_department_id: str
    assigned_head: str
    status: str  # PENDING | IN_PROGRESS | COMPLETED | ESCALATED
    duration_ms: float
    output_summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StrategicMission:
    mission_id: str
    title: str
    strategic_objective: str
    priority: str  # CRITICAL | HIGH | NORMAL
    status: str  # IN_PROGRESS | COMPLETED | PAUSED | REPLANNING
    budget_ceiling_usd: float
    budget_consumed_usd: float
    participating_departments: List[str]
    stages: List[MissionStage]
    initiated_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MissionDirector:
    """Manages strategic multi-department missions across the digital enterprise."""

    def __init__(self):
        self.missions: Dict[str, StrategicMission] = {}
        self._seed_active_missions()

    def _seed_active_missions(self):
        m1 = StrategicMission(
            mission_id="mission_live_001",
            title="Enterprise Financial Document Processing",
            strategic_objective="Zero-fabrication automated extraction and invariant validation of high-value vendor invoices.",
            priority="CRITICAL",
            status="IN_PROGRESS",
            budget_ceiling_usd=0.050,
            budget_consumed_usd=0.018,
            participating_departments=["dept_executive", "dept_ocr", "dept_extraction", "dept_validation", "dept_governance"],
            stages=[
                MissionStage(1, "Strategic Intake & Policy Check", "dept_executive", "Chief Executive Agent", "COMPLETED", 35.0, "Authorized under Standard Enterprise Policy"),
                MissionStage(2, "Optical Ingestion & Bounding Box Layout", "dept_ocr", "Lead Vision Agent", "COMPLETED", 180.0, "Extracted 4 pages with LayoutLM bounding boxes"),
                MissionStage(3, "Structured Semantic Extraction", "dept_extraction", "Lead Extraction Specialist", "IN_PROGRESS", 420.0, "Gemini 2.5 Flash parsing line-item table"),
                MissionStage(4, "Mathematical Cross-Field Invariant Check", "dept_validation", "Lead Verification Auditor", "PENDING", 0.0),
                MissionStage(5, "Cryptographic Sign-off & Audit Vault", "dept_governance", "Chief Governance Officer", "PENDING", 0.0),
            ]
        )
        self.missions[m1.mission_id] = m1

    def get_mission(self, mission_id: str) -> Optional[StrategicMission]:
        return self.missions.get(mission_id)

    def list_missions(self) -> List[Dict[str, Any]]:
        return [m.to_dict() for m in self.missions.values()]

    def advance_stage(self, mission_id: str, stage_index: int, duration_ms: float, summary: str):
        if mission_id in self.missions:
            m = self.missions[mission_id]
            for s in m.stages:
                if s.stage_index == stage_index:
                    s.status = "COMPLETED"
                    s.duration_ms = duration_ms
                    s.output_summary = summary
                elif s.stage_index == stage_index + 1:
                    s.status = "IN_PROGRESS"


mission_director = MissionDirector()
