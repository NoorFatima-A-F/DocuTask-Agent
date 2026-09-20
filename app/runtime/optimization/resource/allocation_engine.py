"""
Allocation Engine & Resource Health for Phase 13.6 (ARIA-EOP).
Handles atomic resource allocations, reservations, releases, and health degradation monitoring.
"""

from typing import Dict, Any, List, Optional
import uuid
from pydantic import BaseModel, Field


class AllocationTicket(BaseModel):
    ticket_id: str = Field(default_factory=lambda: f"tkt_{uuid.uuid4().hex[:8]}")
    mission_id: str
    resource_id: str
    units_allocated: int
    status: str = "ALLOCATED"  # ALLOCATED | RELEASED


class AllocationEngine:
    """
    Manages atomic resource unit reservations and releases.
    """

    def __init__(self):
        self._tickets: Dict[str, AllocationTicket] = {}

    def allocate(self, mission_id: str, resource_id: str, units: int) -> AllocationTicket:
        ticket = AllocationTicket(
            mission_id=mission_id,
            resource_id=resource_id,
            units_allocated=units,
            status="ALLOCATED",
        )
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def release(self, ticket_id: str) -> Optional[AllocationTicket]:
        ticket = self._tickets.get(ticket_id)
        if ticket:
            ticket.status = "RELEASED"
        return ticket


allocation_engine = AllocationEngine()
