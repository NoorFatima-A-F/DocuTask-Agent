"""
AMRS-RSIP Phase 13.9 - Recursive Self-Improvement Engine
Coordinates end-to-end self-improvement cycles across observation, reflection, reasoning, experimentation, governance, and rollback checkpoints.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional
import uuid
from app.runtime.meta.events.meta_events import ImprovementStatus


@dataclass
class SelfImprovementCycle:
    cycle_id: str
    target_area: str
    reflection_tree_id: str
    hypothesis_description: str
    experiment_id: Optional[str]
    proposal_id: Optional[str]
    status: ImprovementStatus = ImprovementStatus.PROPOSED
    measured_gain_pct: float = 0.0
    checkpoint_merkle_root: str = ""
    governance_approved: bool = False
    initiated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None


class RecursiveSelfImprovementEngine:
    """
    Master coordinator closing the loop on continuous autonomous self-improvement.
    """

    def __init__(self):
        self._cycles: Dict[str, SelfImprovementCycle] = {}
        self._seed_default_cycle()

    def initiate_improvement_cycle(
        self,
        target_area: str,
        reflection_tree_id: str,
        hypothesis: str,
        experiment_id: Optional[str] = None,
        proposal_id: Optional[str] = None,
    ) -> SelfImprovementCycle:
        cid = f"sic-{uuid.uuid4().hex[:8]}"

        proof = f"{cid}:{target_area}:{reflection_tree_id}:{hypothesis}"
        merkle = hashlib.sha256(proof.encode()).hexdigest()

        cycle = SelfImprovementCycle(
            cycle_id=cid,
            target_area=target_area,
            reflection_tree_id=reflection_tree_id,
            hypothesis_description=hypothesis,
            experiment_id=experiment_id,
            proposal_id=proposal_id,
            status=ImprovementStatus.IN_EXPERIMENT,
            checkpoint_merkle_root=merkle,
        )

        self._cycles[cid] = cycle
        return cycle

    def verify_and_promote_cycle(self, cycle_id: str, measured_gain_pct: float) -> bool:
        cycle = self._cycles.get(cycle_id)
        if not cycle:
            return False

        cycle.measured_gain_pct = measured_gain_pct
        cycle.status = ImprovementStatus.GOVERNANCE_PENDING if measured_gain_pct > 0 else ImprovementStatus.REJECTED
        return True

    def mark_approved(self, cycle_id: str) -> bool:
        cycle = self._cycles.get(cycle_id)
        if not cycle:
            return False
        cycle.governance_approved = True
        cycle.status = ImprovementStatus.DEPLOYED
        cycle.completed_at = datetime.now(timezone.utc).isoformat()
        return True

    def rollback_cycle(self, cycle_id: str, reason: str = "Regression detected") -> bool:
        cycle = self._cycles.get(cycle_id)
        if not cycle:
            return False
        cycle.status = ImprovementStatus.ROLLED_BACK
        cycle.completed_at = datetime.now(timezone.utc).isoformat()
        return True

    def get_all_cycles(self) -> List[SelfImprovementCycle]:
        return list(self._cycles.values())

    def get_cycle(self, cycle_id: str) -> Optional[SelfImprovementCycle]:
        return self._cycles.get(cycle_id)

    def _seed_default_cycle(self):
        c1 = self.initiate_improvement_cycle(
            target_area="OCR_DAG_PARALLELIZATION",
            reflection_tree_id="rrt-seed-01",
            hypothesis="Parallel chunk fan-out in DAG execution reduces multi-page invoice extraction latency by >= 35%.",
            experiment_id="exp-seed-01",
            proposal_id="pol-prop-seed-01",
        )
        self.verify_and_promote_cycle(c1.cycle_id, measured_gain_pct=42.5)
        self.mark_approved(c1.cycle_id)
