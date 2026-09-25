"""
Resource and Worker Reservation.
"""

from pydantic import BaseModel, Field


class WorkerReservation(BaseModel):
    """Temporary reservation of worker slot prior to dispatching."""
    reservation_id: str
    worker_id: str
    node_id: str
    is_active: bool = Field(default=True)
    model_config = {"frozen": True}
