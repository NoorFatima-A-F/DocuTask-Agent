"""
Budget Allocator for Phase 13.6 (ARIA-EOP).
Manages dynamic budget reservations, spending caps, and multi-mission financial envelopes.
"""

from typing import Dict
import uuid
from pydantic import BaseModel, Field


class BudgetReservation(BaseModel):
    reservation_id: str = Field(default_factory=lambda: f"res_{uuid.uuid4().hex[:8]}")
    mission_id: str
    reserved_amount_usd: float
    total_budget_usd: float
    remaining_balance_usd: float
    status: str = "RESERVED"


class BudgetAllocator:
    """
    Allocates and monitors operational monetary envelopes.
    """

    def __init__(self, global_cap_usd: float = 100.0):
        self.global_cap_usd = global_cap_usd
        self._reservations: Dict[str, BudgetReservation] = {}

    def reserve_budget(self, mission_id: str, requested_usd: float, total_budget_usd: float = 1.0) -> BudgetReservation:
        remaining = max(0.0, total_budget_usd - requested_usd)
        status = "RESERVED" if requested_usd <= total_budget_usd else "EXCEEDED"

        res = BudgetReservation(
            mission_id=mission_id,
            reserved_amount_usd=requested_usd,
            total_budget_usd=total_budget_usd,
            remaining_balance_usd=remaining,
            status=status,
        )
        self._reservations[res.reservation_id] = res
        return res


budget_allocator = BudgetAllocator()
