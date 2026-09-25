"""
AMAEOP Pillar 2 - Inter-Department Coordination Engine
Manages barrier synchronizations, cross-team data contracts, and dependency resolution between departments.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import time


@dataclass
class CoordinationBarrier:
    barrier_id: str
    mission_id: str
    participating_departments: List[str]
    arrived_departments: List[str]
    is_released: bool
    created_at: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CoordinationEngine:
    """Coordinates barrier synchronizations and handoffs across departments."""

    def __init__(self):
        self.barriers: Dict[str, CoordinationBarrier] = {}
        self._seed_barriers()

    def _seed_barriers(self):
        b1 = CoordinationBarrier(
            barrier_id="bar_ocr_extraction_01",
            mission_id="mission_live_001",
            participating_departments=["dept_ocr", "dept_memory"],
            arrived_departments=["dept_ocr", "dept_memory"],
            is_released=True,
            created_at=time.time() - 10.0,
        )
        b2 = CoordinationBarrier(
            barrier_id="bar_val_gov_02",
            mission_id="mission_live_001",
            participating_departments=["dept_validation", "dept_qa"],
            arrived_departments=["dept_validation"],
            is_released=False,
            created_at=time.time() - 2.0,
        )
        self.barriers[b1.barrier_id] = b1
        self.barriers[b2.barrier_id] = b2

    def create_barrier(self, barrier_id: str, mission_id: str, departments: List[str]) -> CoordinationBarrier:
        barrier = CoordinationBarrier(
            barrier_id=barrier_id,
            mission_id=mission_id,
            participating_departments=departments,
            arrived_departments=[],
            is_released=False,
            created_at=time.time(),
        )
        self.barriers[barrier_id] = barrier
        return barrier

    def arrive_at_barrier(self, barrier_id: str, department_id: str) -> bool:
        if barrier_id not in self.barriers:
            return False
        b = self.barriers[barrier_id]
        if department_id not in b.arrived_departments and department_id in b.participating_departments:
            b.arrived_departments.append(department_id)
        if len(b.arrived_departments) >= len(b.participating_departments):
            b.is_released = True
        return b.is_released

    def list_barriers(self) -> List[Dict[str, Any]]:
        return [b.to_dict() for b in self.barriers.values()]


coordination_engine = CoordinationEngine()
