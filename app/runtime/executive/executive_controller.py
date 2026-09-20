"""
AMAEOP Pillar 2 - Executive Coordination Controller
Provides top-level strategic oversight, mission authorization, priority arbitration, and organizational synchronization.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import time
import uuid


@dataclass
class ExecutiveDecision:
    decision_id: str
    mission_id: str
    decision_type: str  # MISSION_INTAKE | PRIORITY_OVERRIDE | RESOURCE_REALLOCATION | CROSS_DEPT_ARBITRATION | EMERGENCY_HALT
    decision_title: str
    rationale: str
    affected_departments: List[str]
    authorized_by: str  # Chief Executive Agent
    approval_hash: str
    timestamp_utc: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ExecutiveController:
    """Strategic leadership controller orchestrating organization-wide autonomous task processing."""

    def __init__(self):
        self.decisions: List[ExecutiveDecision] = []
        self._seed_decisions()

    def _seed_decisions(self):
        d1 = ExecutiveDecision(
            decision_id="exec_dec_001",
            mission_id="mission_live_001",
            decision_type="MISSION_INTAKE",
            decision_title="Authorize Q3 Enterprise Invoices Multi-Department Processing",
            rationale="Approved high-priority invoice corpus execution with target SLA < 1000ms and budget ceiling $0.05.",
            affected_departments=["dept_executive", "dept_ocr", "dept_extraction", "dept_validation", "dept_governance"],
            authorized_by="Chief Executive Agent",
            approval_hash="sha256_exec_88a91f4c",
        )
        d2 = ExecutiveDecision(
            decision_id="exec_dec_002",
            mission_id="mission_live_001",
            decision_type="RESOURCE_REALLOCATION",
            decision_title="Grant Extraction Department Additional 4 Worker Threads",
            rationale="Pre-emptive capacity boost to meet P95 latency guarantees during high throughput burst.",
            affected_departments=["dept_extraction", "dept_research"],
            authorized_by="Chief Executive Agent",
            approval_hash="sha256_exec_31b0e9a2",
        )
        self.decisions.extend([d1, d2])

    def issue_decision(
        self,
        mission_id: str,
        decision_type: str,
        decision_title: str,
        rationale: str,
        affected_departments: List[str],
    ) -> ExecutiveDecision:
        dec_id = f"exec_dec_{uuid.uuid4().hex[:6]}"
        appr_hash = f"sha256_exec_{uuid.uuid4().hex[:8]}"
        decision = ExecutiveDecision(
            decision_id=dec_id,
            mission_id=mission_id,
            decision_type=decision_type,
            decision_title=decision_title,
            rationale=rationale,
            affected_departments=affected_departments,
            authorized_by="Chief Executive Agent",
            approval_hash=appr_hash,
        )
        self.decisions.insert(0, decision)
        return decision

    def list_executive_decisions(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [d.to_dict() for d in self.decisions[:limit]]


executive_controller = ExecutiveController()
